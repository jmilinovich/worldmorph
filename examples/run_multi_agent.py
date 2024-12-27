import asyncio
import os
from dotenv import load_dotenv
from src.controller import SimulationController
from src.monitor import WorldMonitor

async def main():
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("Please set ANTHROPIC_API_KEY environment variable")
    
    # Create controller and world
    controller = SimulationController()
    
    # Create a single world with multiple agents that can interact
    world = await controller.create_world("interactive_world", num_agents=4)
    
    # Create monitor to watch the interactions
    monitor = WorldMonitor("interactive_world", world.state)
    
    try:
        print("Starting multi-agent simulation...")
        print("Agents can observe and interact with each other")
        print("Press Ctrl+C to stop")
        
        # Run monitor and simulation in parallel
        await asyncio.gather(
            monitor.start(),
            controller.run_all()
        )
    except KeyboardInterrupt:
        print("\nStopping simulation...")
        await controller.stop_all()

if __name__ == "__main__":
    asyncio.run(main())