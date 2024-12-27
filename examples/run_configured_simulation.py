import asyncio
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from dotenv import load_dotenv
from src.controller import SimulationController
from src.monitor import WorldMonitor
from src.config import SimulationConfig
from src.simulations import SIMULATIONS

async def main():
    console = Console()
    
    # Nice title
    console.print("\n[bold cyan]Multi-Agent World Simulator[/bold cyan]")
    
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        console.print("[red]Error: ANTHROPIC_API_KEY not found in environment variables[/red]")
        console.print("Please create a .env file with your API key:")
        console.print("ANTHROPIC_API_KEY=your_key_here")
        return
    
    # Show available simulations
    console.print("\n[bold]Available Simulation Types:[/bold]")
    for key, sim in SIMULATIONS.items():
        console.print(Panel(
            sim["description"],
            title=f"[bold]{sim['name']}[/bold]",
            border_style="cyan"
        ))
    
    # Get simulation choice
    choice = Prompt.ask(
        "\nChoose simulation type",
        choices=["organization", "economic", "urban", "custom"],
        default="organization"
    )
    
    # Get world description
    if choice == "custom":
        world_prompt = Prompt.ask("\nEnter your world description")
    else:
        world_prompt = SIMULATIONS[choice]["content"]
    
    # Create simulation config
    console.print("\n[bold cyan]Initializing Simulation...[/bold cyan]")
    config = await SimulationConfig.from_prompt(world_prompt)
    
    # Create and run simulation
    controller = SimulationController()
    world = await controller.create_world("world_1", config=config)
    monitor = WorldMonitor("world_1", world.state)
    
    console.print("\n[bold green]Starting Simulation![/bold green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    
    try:
        # Run simulation with monitor
        await asyncio.gather(
            monitor.start(),
            controller.run_all()
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping simulation...[/yellow]")
        await controller.stop_all()
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        console.print("[dim]Full error:[/dim]")
        import traceback
        console.print(traceback.format_exc())
        await controller.stop_all()

if __name__ == "__main__":
    asyncio.run(main())