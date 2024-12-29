from typing import List, Optional
from datetime import timedelta
import asyncio
from rich.console import Console

from .state.interface import WorldState, Event
from .agent import Agent
from .simulation import SimulationBase
from .metrics import MetricsTracker, MetricDefinition
from .llm import analyze_simulation_metrics

console = Console()

class WorldSimulation(SimulationBase):
    def __init__(
        self, 
        world_id: str, 
        state: WorldState, 
        config=None, 
        duration: Optional[timedelta] = None,
        time_scale: float = 1.0,
        metrics: Optional[list[MetricDefinition]] = None
    ):
        # Initialize base simulation
        super().__init__(
            duration=duration,
            time_scale=time_scale,
            metrics=metrics
        )
        
        console.print(f"[cyan]Initializing world {world_id}[/cyan]")
        self.world_id = world_id
        self.state = state
        self.config = config
        self.agents: List[Agent] = []
        self.running = False
        self.agent_tasks: List[asyncio.Task] = []
        
        # Initialize world state
        asyncio.create_task(self.state.update("world_state", {
            "world_id": world_id,
            "status": "initialized",
            "agent_count": 0,
            "simulation_time": str(self.clock.current_time)
        }))
    
    async def spawn_agent(self, agent_id: str) -> Agent:
        """Create a new agent in this world"""
        console.print(f"[yellow]Spawning agent: {agent_id}[/yellow]")
        
        # Create agent
        agent = Agent(agent_id, self.state, self.config)
        self.agents.append(agent)
        
        # Update state
        await self.state.update(f"agent_{agent_id}", {
            "id": agent_id,
            "active": True,
            "last_action": "Agent initialized",
            "status": "ready"
        })
        
        # Log agent creation
        self.logger.log_event(
            "agent_spawned",
            self.world_id,
            {"agent_id": agent_id}
        )
        
        # Notify about new agent
        await self.state.publish_event(Event(
            type="agent_spawned",
            data={
                "agent_id": agent_id,
                "world_id": self.world_id,
                "status": "spawned"
            },
            source=self.world_id
        ))
        
        return agent
    
    async def start_agents(self):
        """Start all agents"""
        console.print(f"[green]Starting {len(self.agents)} agents...[/green]")
        
        # Create tasks for each agent
        self.agent_tasks = [
            asyncio.create_task(
                agent.run(),
                name=f"agent_{agent.agent_id}"
            )
            for agent in self.agents
        ]
        
        # Wait for all agents to start
        await asyncio.gather(*self.agent_tasks, return_exceptions=True)
    
    async def update(self):
        """Update world state"""
        # Update simulation time
        await self.state.update("world_state", {
            "world_id": self.world_id,
            "status": "running",
            "agent_count": len(self.agents),
            "simulation_time": str(self.clock.current_time)
        })
        
        # Update metrics
        await self.update_metrics()
    
    async def update_metrics(self):
        """Update simulation metrics"""
        if not self.metrics:
            return
            
        # Example metric updates based on agent states
        agent_states = await self.state.get_agents()
        
        if "employee_satisfaction" in self.metrics.definitions:
            satisfaction = self._calculate_satisfaction(agent_states)
            self.metrics.record_metric("employee_satisfaction", satisfaction)
            
        if "productivity" in self.metrics.definitions:
            productivity = self._calculate_productivity(agent_states)
            self.metrics.record_metric("productivity", productivity)
    
    def _calculate_satisfaction(self, agent_states: dict) -> float:
        """Calculate employee satisfaction from agent states"""
        # This would be implemented based on specific simulation needs
        return 75.0  # Example value
        
    def _calculate_productivity(self, agent_states: dict) -> float:
        """Calculate productivity from agent states"""
        # This would be implemented based on specific simulation needs
        return 100.0  # Example value
    
    async def run(self):
        """Run the world simulation"""
        console.print(f"[green]Starting world {self.world_id}[/green]")
        self.running = True
        
        try:
            # Start agents in the background
            agent_runner = asyncio.create_task(self.start_agents())
            
            # Run simulation loop
            await super().run()
            
            # Wait for agents to finish
            await agent_runner
            
        except asyncio.CancelledError:
            console.print("[yellow]World simulation cancelled[/yellow]")
        except Exception as e:
            console.print(f"[red]Error in world simulation: {str(e)}[/red]")
            raise
        finally:
            # Stop all agents
            await self.stop()
            # Generate final report
            await self.generate_report()
    
    async def generate_report(self):
        """Generate final simulation report"""
        if self.metrics:
            # Get metrics data
            metrics_data = {
                name: {
                    "final_value": self.metrics.get_current_value(name),
                    "trend": self.metrics.get_trend(name)
                }
                for name in self.metrics.definitions
            }
            
            # Get analysis from Claude
            analysis = await analyze_simulation_metrics(
                metrics_data,
                self.config.world_description if self.config else "No description"
            )
            
            # Save everything
            self.metrics.save_to_file(f"metrics_{self.world_id}.json")
            
            # Print report
            console.print("\n[bold cyan]Simulation Report[/bold cyan]")
            console.print(analysis)
    
    async def stop(self):
        """Stop the world simulation"""
        console.print(f"[yellow]Stopping world {self.world_id}[/yellow]")
        self.running = False
        
        # Cancel all agent tasks
        for task in self.agent_tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        # Stop all agents
        for agent in self.agents:
            await agent.stop()
        
        # Update state
        await self.state.update("world_state", {
            "world_id": self.world_id,
            "status": "stopped",
            "agent_count": len(self.agents),
            "simulation_time": str(self.clock.current_time)
        })