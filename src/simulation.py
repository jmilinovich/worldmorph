import asyncio
import time
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from pathlib import Path
from rich.console import Console

from .metrics import MetricsTracker, MetricDefinition

console = Console()

class SimulationClock:
    def __init__(self, start_time: datetime, time_scale: float = 1.0):
        """
        Initialize simulation clock
        start_time: When simulation starts
        time_scale: How many real seconds per simulated second
        """
        self.start_time = start_time
        self.time_scale = time_scale
        self.current_time = start_time
        self.running = False
        
    async def run(self, duration: Optional[timedelta] = None):
        """Run the clock for specified duration"""
        self.running = True
        start_real_time = time.time()
        
        while self.running:
            if duration and (self.current_time - self.start_time) >= duration:
                self.running = False
                break
                
            # Update simulated time based on real time elapsed
            elapsed_real = time.time() - start_real_time
            elapsed_sim = timedelta(seconds=elapsed_real * self.time_scale)
            self.current_time = self.start_time + elapsed_sim
            
            await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
            
    def stop(self):
        """Stop the clock"""
        self.running = False

class SimulationLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Set up logging
        self.logger = logging.getLogger("simulation")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler(
            self.log_dir / f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
    def log_event(self, event_type: str, source: str, data: Dict[str, Any]):
        """Log an event with all details"""
        self.logger.info(f"{event_type} from {source}: {data}")
        
    def log_metric(self, metric_name: str, value: Any):
        """Log a metric update"""
        self.logger.debug(f"Metric {metric_name} updated to {value}")
        
    def log_error(self, source: str, error: Exception):
        """Log an error"""
        self.logger.error(f"Error in {source}: {str(error)}", exc_info=True)

class SimulationBase:
    def __init__(
        self,
        duration: Optional[timedelta] = None,
        time_scale: float = 1.0,
        metrics: Optional[list[MetricDefinition]] = None
    ):
        # Initialize components
        self.clock = SimulationClock(
            start_time=datetime.now(),
            time_scale=time_scale
        )
        self.logger = SimulationLogger()
        self.metrics = MetricsTracker()
        
        # Set up metrics if provided
        if metrics:
            for metric in metrics:
                self.metrics.define_metric(metric)
                
        self.duration = duration
        self.running = False
        
    async def run(self):
        """Run the simulation"""
        self.running = True
        
        try:
            # Start clock
            clock_task = asyncio.create_task(
                self.clock.run(self.duration)
            )
            
            # Run until clock stops
            while self.clock.running:
                await self.update()
                await asyncio.sleep(0.1)
                
        except Exception as e:
            self.logger.log_error("simulation", e)
            raise
        finally:
            self.running = False
            
    async def update(self):
        """Override this in specific simulation implementations"""
        pass
        
    def stop(self):
        """Stop the simulation"""
        self.clock.stop()
        self.running = False
        
    def get_metrics_report(self):
        """Generate metrics report"""
        return self.metrics.create_report()