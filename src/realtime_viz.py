import asyncio
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import defaultdict
import webbrowser
import os
from rich.console import Console

console = Console()

class RealtimeVisualizer:
    def __init__(self, metrics_tracker, update_interval: float = 1.0):
        self.metrics = metrics_tracker
        self.update_interval = update_interval
        self.running = False
        
        # Store data points for each metric
        self.data = defaultdict(lambda: {"times": [], "values": []})
        
        # Create the initial plot
        self.create_plot()
        
    def create_plot(self):
        """Create the initial plot"""
        num_metrics = len(self.metrics.definitions)
        
        self.fig = make_subplots(
            rows=num_metrics, cols=1,
            subplot_titles=list(self.metrics.definitions.keys()),
            vertical_spacing=0.1
        )
        
        # Add empty traces for each metric
        for idx, metric_name in enumerate(self.metrics.definitions.keys(), start=1):
            self.fig.add_trace(
                go.Scatter(
                    x=[],
                    y=[],
                    name=metric_name,
                    mode='lines+markers'
                ),
                row=idx, col=1
            )
            
            # Add target line if exists
            definition = self.metrics.definitions[metric_name]
            if definition.target_value is not None:
                self.fig.add_hline(
                    y=definition.target_value,
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Target",
                    row=idx, col=1
                )
        
        # Update layout
        self.fig.update_layout(
            height=300 * num_metrics,
            showlegend=False,
            title_text="Live Simulation Metrics",
            title_x=0.5,
            uirevision=True  # Keep zoom level during updates
        )
        
        # Save initial plot
        self.fig.write_html(
            "live_metrics.html",
            auto_open=False,
            include_plotlyjs=True
        )
        
        # Open in browser
        webbrowser.open('file://' + os.path.realpath("live_metrics.html"))
    
    def update_plot(self):
        """Update the plot with new data"""
        for idx, (metric_name, definition) in enumerate(self.metrics.definitions.items()):
            # Get current value
            current = self.metrics.get_current_value(metric_name)
            if current is not None:
                # Add new data point
                self.data[metric_name]["times"].append(datetime.now())
                self.data[metric_name]["values"].append(current)
                
                # Update trace
                self.fig.data[idx*2].x = self.data[metric_name]["times"]
                self.fig.data[idx*2].y = self.data[metric_name]["values"]
        
        # Save updated plot
        self.fig.write_html(
            "live_metrics.html",
            auto_open=False,
            include_plotlyjs=True
        )
    
    async def run(self):
        """Run the live visualization"""
        self.running = True
        console.print("[cyan]Starting live metrics visualization...[/cyan]")
        console.print("[dim]Open live_metrics.html in your browser to see real-time updates[/dim]")
        
        while self.running:
            try:
                self.update_plot()
                await asyncio.sleep(self.update_interval)
            except Exception as e:
                console.print(f"[red]Error updating plot: {str(e)}[/red]")
                await asyncio.sleep(1)
    
    def stop(self):
        """Stop the visualization"""
        self.running = False