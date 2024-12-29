import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pandas as pd
from typing import Dict, List
from .metrics import MetricsTracker

class MetricsVisualizer:
    def __init__(self, metrics_tracker: MetricsTracker):
        self.metrics = metrics_tracker

    def create_dashboard(self, output_file: str = "metrics_dashboard.html"):
        """Create an interactive dashboard of all metrics"""
        # Get all metric data
        metric_names = list(self.metrics.definitions.keys())
        num_metrics = len(metric_names)
        
        # Create subplots
        fig = make_subplots(
            rows=num_metrics, cols=1,
            subplot_titles=metric_names,
            vertical_spacing=0.1
        )

        # Add traces for each metric
        for idx, metric_name in enumerate(metric_names, start=1):
            metric_data = self.metrics.metrics[metric_name]
            df = pd.DataFrame(metric_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            
            # Line plot for the metric
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['value'],
                    name=metric_name,
                    mode='lines+markers'
                ),
                row=idx, col=1
            )
            
            # Add target line if exists
            definition = self.metrics.definitions[metric_name]
            if definition.target_value is not None:
                fig.add_hline(
                    y=definition.target_value,
                    line_dash="dash",
                    line_color="red",
                    annotation_text="Target",
                    row=idx, col=1
                )

        # Update layout
        fig.update_layout(
            height=300 * num_metrics,
            showlegend=False,
            title_text="Simulation Metrics Dashboard",
            title_x=0.5
        )

        # Add tooltips and interactivity
        fig.update_traces(
            hovertemplate="<br>".join([
                "Time: %{x}",
                "Value: %{y:.2f}"
            ])
        )

        # Save to file
        fig.write_html(output_file, auto_open=False)
        
    def create_summary_plot(self, output_file: str = "metrics_summary.html"):
        """Create a summary plot showing normalized metrics for comparison"""
        # Prepare data
        all_data = {}
        for metric_name in self.metrics.definitions.keys():
            metric_data = self.metrics.metrics[metric_name]
            df = pd.DataFrame(metric_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            
            # Normalize values to 0-1 range
            min_val = df['value'].min()
            max_val = df['value'].max()
            if max_val > min_val:
                df['normalized'] = (df['value'] - min_val) / (max_val - min_val)
            else:
                df['normalized'] = df['value']
                
            all_data[metric_name] = df

        # Create plot
        fig = go.Figure()

        for metric_name, df in all_data.items():
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df['normalized'],
                    name=metric_name,
                    mode='lines+markers'
                )
            )

        fig.update_layout(
            title="Normalized Metrics Comparison",
            xaxis_title="Time",
            yaxis_title="Normalized Value",
            height=600,
            showlegend=True
        )

        fig.write_html(output_file, auto_open=False)

    def create_correlation_plot(self, output_file: str = "metrics_correlation.html"):
        """Create a correlation plot between metrics"""
        # Prepare data
        dfs = []
        for metric_name in self.metrics.definitions.keys():
            metric_data = self.metrics.metrics[metric_name]
            df = pd.DataFrame(metric_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df = df.set_index('timestamp')
            df.columns = [metric_name]
            dfs.append(df)

        # Merge all dataframes
        combined_df = pd.concat(dfs, axis=1)
        
        # Calculate correlations
        corr = combined_df.corr()

        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmid=0
        ))

        fig.update_layout(
            title="Metrics Correlation Heatmap",
            height=600,
            width=600
        )

        fig.write_html(output_file, auto_open=False)