import asyncio
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import os
import time
from typing import List, Any
from rich.console import Console

console = Console()

def log_process(msg: str):
    """Log process info with timestamp"""
    process = mp.current_process()
    console.print(f"[cyan]{time.strftime('%H:%M:%S')} - Process {process.name} (PID {process.pid}): {msg}[/cyan]")

class ParallelRunner:
    def __init__(self, num_processes: int = None):
        self.num_processes = num_processes or mp.cpu_count()
        log_process(f"Initializing ParallelRunner with {self.num_processes} processes")
        self.pool = ProcessPoolExecutor(max_workers=self.num_processes)
        
    async def run_parallel(self, func: callable, items: List[Any]) -> List[Any]:
        """Run a function over items in parallel using process pool"""
        log_process(f"Starting parallel execution of {len(items)} items")
        loop = asyncio.get_event_loop()
        
        # Create chunks of work
        chunk_size = max(1, len(items) // self.num_processes)
        chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
        log_process(f"Created {len(chunks)} chunks of size ~{chunk_size}")
        
        # Process chunks in parallel
        futures = [
            loop.run_in_executor(self.pool, self._process_chunk, func, chunk)
            for chunk in chunks
        ]
        
        # Wait for all chunks to complete
        results = []
        for future in asyncio.as_completed(futures):
            chunk_results = await future
            results.extend(chunk_results)
            log_process(f"Completed chunk, total results: {len(results)}")
            
        return results
    
    def _process_chunk(self, func: callable, items: List[Any]) -> List[Any]:
        """Process a chunk of items in a worker process"""
        log_process(f"Processing chunk of {len(items)} items")
        results = []
        for item in items:
            try:
                result = func(item)
                results.append(result)
            except Exception as e:
                log_process(f"Error processing item: {e}")
        return results
    
    def shutdown(self):
        """Clean up process pool"""
        log_process("Shutting down process pool")
        self.pool.shutdown(wait=True)

# Create runner instances per CPU core
num_cores = mp.cpu_count()
log_process(f"System has {num_cores} CPU cores")

# Global process pool
runner = ParallelRunner()

def run_world_simulation(config):
    """Run a single world simulation in a worker process"""
    log_process("Starting world simulation")
    start_time = time.time()
    
    try:
        # Set up new event loop for this process
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Import here to avoid circular imports
        from .controller import SimulationController
        from .monitor import WorldMonitor
        
        process_id = os.getpid()
        world_id = f"world_{process_id}"
        log_process(f"Initializing {world_id}")
        
        # Create and run world
        controller = SimulationController()
        world = loop.run_until_complete(
            controller.create_world(world_id, config=config)
        )
        monitor = WorldMonitor(world_id, world.state)
        
        # Run simulation with timeout
        log_process(f"Running {world_id}")
        try:
            loop.run_until_complete(
                asyncio.wait_for(
                    asyncio.gather(
                        monitor.start(),
                        controller.run_all()
                    ),
                    timeout=300  # 5 minute timeout
                )
            )
        except asyncio.TimeoutError:
            log_process(f"Simulation {world_id} timed out")
        
        duration = time.time() - start_time
        log_process(f"Completed {world_id} in {duration:.2f} seconds")
        
    except Exception as e:
        log_process(f"Error in simulation: {e}")
        raise
    finally:
        loop.close()