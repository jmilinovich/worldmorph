from typing import Dict, List, Optional
import asyncio
from datetime import timedelta
from rich.console import Console

from .world import WorldSimulation
from .state.memory import InMemoryState
from .config import SimulationConfig
from .metrics import MetricDefinition

console = Console()

class SimulationController:
    def __init__(self):
        self.worlds: Dict[str, WorldSimulation] = {}
        self.running = False

    async def create_world(
        self,
        world_id: str,
        config: Optional[SimulationConfig] = None,
        duration: Optional[timedelta] = None,
        time_scale: float = 1.0,
        metrics: Optional[list[MetricDefinition]] = None
    ) -> WorldSimulation:
        """Create a new world simulation"""
        if world_id in self.worlds:
            raise ValueError(f"World {world_id} already exists")
        
        # Create new world with in-memory state
        state = InMemoryState()
        
        # Create world
        world = WorldSimulation(
            world_id=world_id,
            state=state,
            config=config,
            duration=duration,
            time_scale=time_scale,
            metrics=metrics
        )
        
        self.worlds[world_id] = world
        
        # Initialize agents if config provided
        if config and hasattr(config, 'agents'):
            console.print(f"[cyan]Creating {len(config.agents)} agents...[/cyan]")
            for agent in config.agents:
                await world.spawn_agent(agent['name'])
        
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
        """Run all worlds"""
        self.running = True
        await asyncio.gather(
            *(world.run() for world in self.worlds.values())
        )

    async def stop_all(self):
        """Stop all worlds"""
        self.running = False
        for world in self.worlds.values():
            await world.stop()

    def get_world(self, world_id: str) -> Optional[WorldSimulation]:
        """Get a specific world"""
        return self.worlds.get(world_id)

    def list_worlds(self) -> List[str]:
        """Get list of all world IDs"""
        return list(self.worlds.keys())