import asyncio
from datetime import datetime
from typing import Dict, Any
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from .state.interface import WorldState, Event

class WorldMonitor:
    def __init__(self, world_id: str, state: WorldState):
        self.world_id = world_id
        self.state = state
        self.console = Console()
        self.events = []
        self.max_events = 20  # Show more events
        self.agent_states = {}
        
    def create_layout(self) -> Layout:
        """Create the display layout"""
        layout = Layout()
        
        # Events table
        events_table = Table(
            title=f"World {self.world_id} - Recent Events",
            show_header=True,
            header_style="bold magenta"
        )
        events_table.add_column("Time", width=12)
        events_table.add_column("Source", width=20)
        events_table.add_column("Type", width=10)
        events_table.add_column("Action", width=80)
        
        for event in self.events[-self.max_events:]:
            events_table.add_row(
                event["time"],
                event["source"],
                event["type"],
                event["action"]
            )
        
        # Agents table
        agents_table = Table(
            title="Active Agents",
            show_header=True,
            header_style="bold magenta"
        )
        agents_table.add_column("Agent ID", width=30)
        agents_table.add_column("Name", width=30)
        agents_table.add_column("Status", width=10)
        agents_table.add_column("Last Action", width=60)
        
        for agent_id, state in self.agent_states.items():
            agents_table.add_row(
                agent_id,
                state.get("name", "Unknown"),
                "Active" if state.get("active", False) else "Inactive",
                state.get("last_action", "No action")[:60] + "..." if state.get("last_action", "") else "No action"
            )
        
        # Combine in layout
        layout.split_column(
            Panel(events_table, title="Events Log", border_style="cyan"),
            Panel(agents_table, title="Agent Status", border_style="green")
        )
        
        return layout

    async def handle_event(self, event: Event):
        """Process and display new events"""
        time = datetime.now().strftime("%H:%M:%S")
        
        # Create event record
        event_record = {
            "time": time,
            "source": event.source,
            "type": event.type,
            "action": str(event.data.get("action", {}).get("content", "No content"))
        }
        
        # Add to events list
        self.events.append(event_record)
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
        
        # Print event to console
        if event.type == "agent_action":
            self.console.print(f"\n[cyan]{time} - {event.source}:[/cyan]")
            self.console.print(event_record["action"])
        
        # Update agent states
        self.agent_states = await self.state.get_agents() or {}

    async def start(self):
        """Start monitoring the world"""
        await self.state.subscribe("monitor", self.handle_event)
        self.agent_states = await self.state.get_agents() or {}
        
        try:
            with Live(self.create_layout(), refresh_per_second=2) as live:
                while True:
                    live.update(self.create_layout())
                    await asyncio.sleep(0.5)  # Update twice per second
        except Exception as e:
            self.console.print(f"[red]Monitor error: {str(e)}[/red]")
            raise