from typing import List
import asyncio
from rich.console import Console
from .state.interface import WorldState, Event
from .agent import Agent

console = Console()

class WorldSimulation:
    def __init__(self, world_id: str, state: WorldState, config=None):
        console.print(f"[cyan]Initializing world {world_id}[/cyan]")
        self.world_id = world_id
        self.state = state
        self.config = config
        self.agents: List[Agent] = []
        self.running = False
        
        # Initialize world state
        asyncio.create_task(self.state.update("world_state", {
            "world_id": world_id,
            "status": "initialized",
            "agent_count": 0
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
    
    async def run(self):
        """Run the world simulation"""
        console.print(f"[green]Starting world {self.world_id}[/green]")
        self.running = True
        
        # Update world state
        await self.state.update("world_state", {
            "world_id": self.world_id,
            "status": "running",
            "agent_count": len(self.agents)
        })
        
        # Publish world started event
        await self.state.publish_event(Event(
            type="world_started",
            data={"world_id": self.world_id},
            source=self.world_id
        ))
        
        console.print(f"[cyan]Starting {len(self.agents)} agents...[/cyan]")
        
        # Start all agents
        agent_tasks = []
        for agent in self.agents:
            task = asyncio.create_task(agent.run())
            agent_tasks.append(task)
        
        # Wait for all agents
        await asyncio.gather(*agent_tasks)
    
    async def stop(self):
        """Stop the world simulation"""
        console.print(f"[yellow]Stopping world {self.world_id}[/yellow]")
        self.running = False
        
        # Stop all agents
        for agent in self.agents:
            await agent.stop()
        
        # Update state
        await self.state.update("world_state", {
            "world_id": self.world_id,
            "status": "stopped",
            "agent_count": len(self.agents)
        })