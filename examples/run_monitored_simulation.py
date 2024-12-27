import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

def setup_environment():
    """Setup environment variables and check configuration"""
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables.")
        print("Please create a .env file in the project root with content:")
        print("ANTHROPIC_API_KEY=your_api_key_here")
        sys.exit(1)
    
    return api_key

async def main():
    # Setup environment
    api_key = setup_environment()
    print(f"Found API key: {api_key[:8]}...")
    
    # Import after environment is set up
    from src.controller import SimulationController
    from src.monitor import WorldMonitor
    
    # Create controller and world
    controller = SimulationController()
    world = await controller.create_world("monitored_world", num_agents=3)
    
    # Create monitor for the world
    monitor = WorldMonitor("monitored_world", world.state)
    
    try:
        print("Starting monitored simulation...")
        print("You'll see a live view of events and agent states")
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