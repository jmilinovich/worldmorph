import asyncio
import os
import sys
from pathlib import Path
import multiprocessing as mp
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.live import Live
from rich.table import Table

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from dotenv import load_dotenv
from src.config import SimulationConfig
from src.simulations import SIMULATIONS
from src.parallel import runner, run_world_simulation

def create_status_table(start_time: float, num_worlds: int, completed: int) -> Table:
    """Create status display table"""
    table = Table(title="Simulation Status")
    table.add_column("Metric")
    table.add_column("Value")
    
    # Add status rows
    duration = time.time() - start_time
    worlds_per_sec = completed / duration if duration > 0 else 0
    
    table.add_row("Time Elapsed", f"{duration:.1f} seconds")
    table.add_row("Worlds Completed", f"{completed} / {num_worlds}")
    table.add_row("Processing Rate", f"{worlds_per_sec:.2f} worlds/second")
    table.add_row("CPU Cores Used", str(mp.cpu_count()))
    
    return table

async def main():
    console = Console()
    
    # Nice title
    console.print("\n[bold cyan]Multi-Agent World Simulator[/bold cyan]")
    console.print(f"[dim]Running with {mp.cpu_count()} CPU cores[/dim]\n")
    
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
    
    # Get number of parallel worlds to run
    num_worlds = IntPrompt.ask(
        "\nHow many parallel worlds to simulate?",
        default=mp.cpu_count()
    )
    
    # Create simulation configs
    console.print("\n[bold cyan]Initializing Simulations...[/bold cyan]")
    configs = []
    
    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Creating world configs...", total=num_worlds)
        for i in range(num_worlds):
            config = await SimulationConfig.from_prompt(world_prompt)
            configs.append(config)
            progress.update(task, advance=1)
    
    # Run simulations in parallel processes
    console.print("\n[bold green]Starting Simulations![/bold green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    
    start_time = time.time()
    completed = 0
    
    try:
        # Show live status while processing
        with Live(create_status_table(start_time, num_worlds, completed), refresh_per_second=4) as live:
            # Process worlds in parallel
            results = await runner.run_parallel(run_world_simulation, configs)
            completed = len(results)
            live.update(create_status_table(start_time, num_worlds, completed))
        
        # Show final stats
        duration = time.time() - start_time
        console.print(f"\n[green]Completed {completed} worlds in {duration:.1f} seconds")
        console.print(f"Average processing rate: {completed/duration:.2f} worlds/second")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping all simulations...[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        console.print("[dim]Full error:[/dim]")
        import traceback
        console.print(traceback.format_exc())
    finally:
        # Clean up process pool
        runner.shutdown()

if __name__ == "__main__":
    # Enable parallel processing for Windows
    mp.freeze_support()
    
    # Run main async function
    asyncio.run(main())