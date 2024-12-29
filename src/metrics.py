from typing import Dict, Any, List, Optional
import time
import json
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table

console = Console()

@dataclass
class MetricDefinition:
    name: str
    description: str
    type: str  # 'numeric', 'percentage', 'categorical'
    initial_value: Any
    aggregation: str = 'latest'  # 'latest', 'average', 'sum'
    target_value: Optional[Any] = None
    target_direction: Optional[str] = None  # 'maximize', 'minimize', 'target'

class MetricsTracker:
    def __init__(self):
        self.metrics: Dict[str, List[Dict[str, Any]]] = {}
        self.definitions: Dict[str, MetricDefinition] = {}
        
    def define_metric(self, definition: MetricDefinition):
        """Define a new metric to track"""
        self.metrics[definition.name] = []
        self.definitions[definition.name] = definition
        
        # Record initial value
        self.record_metric(definition.name, definition.initial_value)
        
    def record_metric(self, metric_name: str, value: Any):
        """Record a new value for a metric"""
        if metric_name not in self.metrics:
            raise ValueError(f"Metric {metric_name} not defined")
            
        self.metrics[metric_name].append({
            "timestamp": time.time(),
            "value": value
        })
        
    def get_current_value(self, metric_name: str) -> Any:
        """Get current value of a metric"""
        if not self.metrics[metric_name]:
            return None
            
        definition = self.definitions[metric_name]
        values = [entry["value"] for entry in self.metrics[metric_name]]
        
        if definition.aggregation == 'latest':
            return values[-1]
        elif definition.aggregation == 'average':
            return sum(values) / len(values)
        elif definition.aggregation == 'sum':
            return sum(values)
        
    def get_trend(self, metric_name: str, window: int = 5) -> str:
        """Get trend direction for a metric"""
        if len(self.metrics[metric_name]) < 2:
            return "stable"
            
        recent = self.metrics[metric_name][-window:]
        if len(recent) < 2:
            return "stable"
            
        first = recent[0]["value"]
        last = recent[-1]["value"]
        
        if last > first:
            return "increasing"
        elif last < first:
            return "decreasing"
        return "stable"
        
    def create_report(self) -> str:
        """Generate metrics report"""
        table = Table(title="Metrics Report")
        table.add_column("Metric")
        table.add_column("Current Value")
        table.add_column("Trend")
        table.add_column("Target")
        
        for name, definition in self.definitions.items():
            current = self.get_current_value(name)
            trend = self.get_trend(name)
            target = f"{definition.target_value} ({definition.target_direction})" if definition.target_value else "N/A"
            
            table.add_row(
                name,
                str(current),
                trend,
                target
            )
            
        console.print(table)
        
    def save_to_file(self, filename: str):
        """Save metrics history to file"""
        with open(filename, 'w') as f:
            json.dump({
                "metrics": self.metrics,
                "definitions": {
                    name: vars(defn)
                    for name, defn in self.definitions.items()
                }
            }, f, indent=2)
            
    @classmethod
    def load_from_file(cls, filename: str) -> 'MetricsTracker':
        """Load metrics history from file"""
        tracker = cls()
        
        with open(filename) as f:
            data = json.load(f)
            
        # Load definitions
        for name, defn_dict in data["definitions"].items():
            tracker.definitions[name] = MetricDefinition(**defn_dict)
            
        # Load metrics history
        tracker.metrics = data["metrics"]
        
        return tracker

# Example metric definitions for different simulation types
ORGANIZATIONAL_METRICS = [
    MetricDefinition(
        name="employee_satisfaction",
        description="Average employee satisfaction score",
        type="numeric",
        initial_value=75,
        aggregation="average",
        target_value=85,
        target_direction="maximize"
    ),
    MetricDefinition(
        name="productivity",
        description="Team productivity score",
        type="percentage",
        initial_value=100,
        aggregation="latest",
        target_value=120,
        target_direction="maximize"
    ),
    MetricDefinition(
        name="retention_rate",
        description="Employee retention rate",
        type="percentage",
        initial_value=95,
        aggregation="latest",
        target_value=90,
        target_direction="minimize"
    )
]

URBAN_METRICS = [
    MetricDefinition(
        name="carbon_footprint",
        description="City carbon emissions (tons)",
        type="numeric",
        initial_value=1000000,
        aggregation="latest",
        target_value=500000,
        target_direction="minimize"
    ),
    MetricDefinition(
        name="quality_of_life",
        description="Citizen quality of life score",
        type="numeric",
        initial_value=70,
        aggregation="average",
        target_value=85,
        target_direction="maximize"
    )
]