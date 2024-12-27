from typing import List, Dict, Any, Optional
import asyncio
from .state.interface import WorldState, Event
from .agent import Agent
from .config import SimulationConfig

class WorldSimulation:
    def __init__(self, world_id: str, state: WorldState, config: Optional[SimulationConfig] = None):
        self.world_id = world_id
        self.state = state
        self.config = config
        self.agents: List[Agent] = []
        self.running = False
        
        # Initialize world state
        asyncio.create_task(self.state.update("world_state", {
            "world_id": world_id,
            "status": "initialized",
            "agent_count": 0,
            "description": config.world_description if config else None
        }))
    
    async def spawn_agent(self, agent_id: str) -> Agent:
        """Create a new agent in this world"""
        # Create agent with its specific configuration
        agent = Agent(agent_id, self.state, self.config)
        self.agents.append(agent)
        
        # Get agent config if available
        agent_config = None
        if self.config and self.config.agents:
            agent_config = next(
                (a for a in self.config.agents if a['name'] == agent_id),
                None
            )
        
        # Update agent state in the state manager
        agent_state = {
            "id": agent_id,
            "active": True,
            "last_action": "Agent initialized",
            "status": "ready"
        }
        
        # Add config details if available
        if agent_config:
            agent_state.update(agent_config)
        
        await self.state.update(f"agent_{agent_id}", agent_state)
        
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
        self.running = True
        
        # Update world state
        await self.state.update("world_state", {
            "world_id": self.world_id,
            "status": "running",
            "agent_count": len(self.agents),
            "description": self.config.world_description if self.config else None
        })
        
        # Publish world started event
        await self.state.publish_event(Event(
            type="world_started",
            data={"world_id": self.world_id},
            source=self.world_id
        ))
        
        # Start all agents in parallel
        agent_tasks = [agent.run() for agent in self.agents]
        await asyncio.gather(*agent_tasks)
    
    async def stop(self):
        """Stop the world simulation"""
        self.running = False
        
        # Update world state
        await self.state.update("world_state", {
            "world_id": self.world_id,
            "status": "stopped",
            "agent_count": len(self.agents)
        })
        
        # Stop all agents
        for agent in self.agents:
            await agent.stop()
        
        # Publish world stopped event
        await self.state.publish_event(Event(
            type="world_stopped",
            data={"world_id": self.world_id},
            source=self.world_id
        ))