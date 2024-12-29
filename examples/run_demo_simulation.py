import asyncio
import os
from datetime import timedelta
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from pathlib import Path
from dotenv import load_dotenv

from src.config import SimulationConfig
from src.controller import SimulationController
from src.monitor import WorldMonitor
from src.metrics_viz import MetricsVisualizer
from src.realtime_viz import RealtimeVisualizer
from src.simulations import SIMULATIONS
from src.example_metrics import ORGANIZATION_METRICS, URBAN_METRICS, ECONOMIC_METRICS

console = Console()

SIMULATION_METRICS = {
    "organization": ORGANIZATION_METRICS,
    "economic": ECONOMIC_METRICS,
    "urban": URBAN_METRICS
}

def check_environment():
    """Check and set up environment variables"""
    # Try to load from .env file
    env_file = Path('.env')
    if not env_file.exists():
        console.print("[yellow]No .env file found[/yellow]")
        
        # Ask user for API key
        api_key = Prompt.ask(
            "Please enter your Anthropic API key",
            password=True
        )
        
        # Save to .env file
        with open(env_file, 'w') as f:
            f.write(f"ANTHROPIC_API_KEY={api_key}")
            
        console.print("[green].env file created with API key[/green]")
    
    # Load environment variables
    load_dotenv()
    
    # Verify API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("""[red]Error: ANTHROPIC_API_KEY not found in environment[/red]
        
Please create a .env file in the project root with your API key:

1. Create a file named '.env'
2. Add the following line:
   ANTHROPIC_API_KEY=your_key_here
3. Replace 'your_key_here' with your actual Anthropic API key

You can get an API key from: https://console.anthropic.com/
""")
        return False
        
    return True

async def main():
    # Nice title
    console.print("\n[bold cyan]Multi-Agent Simulation Demo[/bold cyan]")
    
    # Check environment setup
    if not check_environment():
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
        choices=["organization", "economic", "urban"],
        default="organization"
    )
    
    # Get simulation duration
    duration_mins = float(Prompt.ask(
        "\nSimulation duration (minutes)",
        default="5"
    ))
    
    # Get visualization update interval
    update_interval = float(Prompt.ask(
        "\nVisualization update interval (seconds)",
        default="1.0"
    ))
    
    # Create simulation config
    console.print("\n[bold cyan]Initializing Simulation...[/bold cyan]")
    
    # Get appropriate metrics for this simulation type
    metrics = SIMULATION_METRICS[choice]
    
    # Create config from template
    config = await SimulationConfig.from_prompt(SIMULATIONS[choice]["content"])
    
    # Create and run simulation
    controller = SimulationController()
    world = await controller.create_world(
        world_id="demo_world",
        config=config,
        duration=timedelta(minutes=duration_mins),
        metrics=metrics
    )
    
    # Create monitor and visualizer
    monitor = WorldMonitor("demo_world", world.state)
    visualizer = RealtimeVisualizer(world.metrics, update_interval)
    
    console.print("\n[bold green]Starting Simulation![/bold green]")
    console.print("[cyan]Monitor will show real-time events and agent status[/cyan]")
    console.print("[cyan]Live metrics visualization will open in your browser[/cyan]")
    console.print("\n[dim]Press Ctrl+C to stop[/dim]")
    
    try:
        # Run simulation with monitor and live visualization
        await asyncio.gather(
            monitor.start(),
            visualizer.run(),
            world.run()
        )
        
        # Create final visualizations
        console.print("\n[cyan]Generating final metric visualizations...[/cyan]")
        viz = MetricsVisualizer(world.metrics)
        
        # Create different visualization types
        viz.create_dashboard("demo_metrics_dashboard.html")
        viz.create_summary_plot("demo_metrics_summary.html")
        viz.create_correlation_plot("demo_metrics_correlation.html")
        
        # Show completion message with links to visualizations
        console.print("\n[green]Simulation complete! The following files have been generated:[/green]")
        console.print("- [cyan]demo_metrics_dashboard.html[/cyan]: Interactive dashboard of all metrics")
        console.print("- [cyan]demo_metrics_summary.html[/cyan]: Summary plot of normalized metrics")
        console.print("- [cyan]demo_metrics_correlation.html[/cyan]: Correlation analysis between metrics")
        console.print("\nOpen these files in a web browser to view the visualizations!")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping simulation...[/yellow]")
        visualizer.stop()
        await world.stop()
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        console.print("[dim]Full error:[/dim]")
        import traceback
        console.print(traceback.format_exc())
        visualizer.stop()
        await world.stop()

if __name__ == "__main__":
    asyncio.run(main())