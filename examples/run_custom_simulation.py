import asyncio
import os
from datetime import timedelta
from rich.console import Console
from rich.prompt import Prompt

from src.config import SimulationConfig
from src.controller import SimulationController
from src.monitor import WorldMonitor
from src.metrics import MetricDefinition, MetricsTracker
from src.metrics_viz import MetricsVisualizer

console = Console()

async def define_custom_metrics() -> list:
    """Interactive creation of custom metrics"""
    metrics = []
    console.print("\n[cyan]Define Custom Metrics[/cyan]")
    
    while True:
        # Get metric details
        name = Prompt.ask("Metric name (or 'done' to finish)")
        if name.lower() == 'done':
            break
            
        description = Prompt.ask("Description")
        type_choice = Prompt.ask(
            "Type",
            choices=["numeric", "percentage", "categorical"],
            default="numeric"
        )
        
        initial = Prompt.ask(
            "Initial value",
            default="0"
        )
        initial_value = float(initial) if type_choice in ["numeric", "percentage"] else initial
        
        aggregation = Prompt.ask(
            "Aggregation method",
            choices=["latest", "average", "sum"],
            default="latest"
        )
        
        target = Prompt.ask("Target value (optional)", default="")
        if target:
            target_value = float(target) if type_choice in ["numeric", "percentage"] else target
            target_direction = Prompt.ask(
                "Target direction",
                choices=["maximize", "minimize", "target"],
                default="maximize"
            )
        else:
            target_value = None
            target_direction = None
        
        # Create metric definition
        metric = MetricDefinition(
            name=name,
            description=description,
            type=type_choice,
            initial_value=initial_value,
            aggregation=aggregation,
            target_value=target_value,
            target_direction=target_direction
        )
        
        metrics.append(metric)
        console.print(f"[green]Added metric: {name}[/green]")
    
    return metrics

async def main():
    console = Console()
    
    # Get world description
    console.print("\n[bold cyan]Custom Simulation Setup[/bold cyan]")
    world_prompt = Prompt.ask("\nEnter your world description")
    
    # Define custom metrics
    metrics = await define_custom_metrics()
    
    # Get simulation duration
    duration_hours = float(Prompt.ask(
        "\nSimulation duration (hours)",
        default="24"
    ))
    
    # Create simulation config
    console.print("\n[bold cyan]Initializing Simulation...[/bold cyan]")
    config = await SimulationConfig.from_prompt(world_prompt)
    
    # Create and run simulation
    controller = SimulationController()
    world = await controller.create_world(
        "custom_world",
        config=config,
        duration=timedelta(hours=duration_hours),
        metrics=metrics
    )
    
    monitor = WorldMonitor("custom_world", world.state)
    
    console.print("\n[bold green]Starting Simulation![/bold green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    
    try:
        # Run simulation with monitor
        await asyncio.gather(
            monitor.start(),
            world.run()
        )
        
        # Create visualizations
        console.print("\n[cyan]Generating metric visualizations...[/cyan]")
        viz = MetricsVisualizer(world.metrics)
        viz.create_dashboard("custom_metrics_dashboard.html")
        viz.create_summary_plot("custom_metrics_summary.html")
        viz.create_correlation_plot("custom_metrics_correlation.html")
        
        console.print("\n[green]Simulation complete! Metric visualizations have been generated.[/green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping simulation...[/yellow]")
        await world.stop()
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        await world.stop()

if __name__ == "__main__":
    asyncio.run(main())