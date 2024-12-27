import asyncio
import os
from dotenv import load_dotenv
from src.controller import SimulationController

async def main():
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("Please set ANTHROPIC_API_KEY environment variable")
    
    # Create two parallel worlds
    controller = SimulationController()
    
    # Create worlds with different numbers of agents
    await controller.create_world("world_1", num_agents=2)
    await controller.create_world("world_2", num_agents=3)
    
    try:
        print("Starting simulations...")
        print("Press Ctrl+C to stop")
        
        # Run both worlds in parallel
        await controller.run_all()
    except KeyboardInterrupt:
        print("\nStopping simulations...")
        await controller.stop_all()

if __name__ == "__main__":
    asyncio.run(main())