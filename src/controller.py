from typing import Dict, List, Optional
import asyncio
from .world import WorldSimulation
from .state.memory import InMemoryState
from .config import SimulationConfig

class SimulationController:
    def __init__(self):
        self.worlds: Dict[str, WorldSimulation] = {}
        self.running = False

    async def create_world(self, world_id: str, num_agents: int = 3, config: Optional[SimulationConfig] = None) -> WorldSimulation:
        """Create a new world simulation"""
        if world_id in self.worlds:
            raise ValueError(f"World {world_id} already exists")
        
        # Create new world with in-memory state
        state = InMemoryState()
        
        # If config provided, initialize state
        if config:
            # Initialize world state
            for key, value in config.initial_state.items():
                if key != "agents":  # Handle agents separately
                    await state.update(key, value)
            
            # Initialize agents
            await state.update("agents", config.agents)
        
        # Create world
        world = WorldSimulation(world_id, state, config)
        self.worlds[world_id] = world
        
        # Spawn initial agents based on config
        if config and config.agents:
            for agent in config.agents:
                await world.spawn_agent(agent['name'])
        else:
            # Spawn default agents if no config
            for i in range(num_agents):
                await world.spawn_agent(f"{world_id}_agent_{i}")
        
        return world

    async def start_world(self, world_id: str):
        """Start a specific world"""
        if world_id not in self.worlds:
            raise ValueError(f"World {world_id} does not exist")
        await self.worlds[world_id].run()

    async def stop_world(self, world_id: str):
        """Stop a specific world"""
        if world_id not in self.worlds:
            raise ValueError(f"World {world_id} does not exist")
        await self.worlds[world_id].stop()

    async def run_all(self):
        """Run all worlds in parallel"""
        self.running = True
        await asyncio.gather(
            *(world.run() for world in self.worlds.values())
        )

    async def stop_all(self):
        """Stop all worlds"""
        self.running = False
        await asyncio.gather(
            *(world.stop() for world in self.worlds.values())
        )

    def get_world(self, world_id: str) -> Optional[WorldSimulation]:
        """Get a specific world"""
        return self.worlds.get(world_id)