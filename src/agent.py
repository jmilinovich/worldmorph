from typing import Any, Dict, Optional
import asyncio
import time
from rich.console import Console

from .state.interface import WorldState, Event
from .llm import get_claude_response

console = Console()

class Agent:
    def __init__(self, agent_id: str, state: WorldState, config=None):
        console.print(f"[cyan]Initializing agent {agent_id}[/cyan]")
        self.agent_id = agent_id
        self.state = state
        self.running = False
        
        # Extract agent info from config
        if config and hasattr(config, 'agents'):
            self.agent_info = next(
                (a for a in config.agents if a['name'] == agent_id), None
            )
            console.print(f"Found agent info for {agent_id}: {self.agent_info is not None}")
        else:
            self.agent_info = None

        # Set up role-specific prompt
        if self.agent_info:
            self.system_prompt = f"""You are {self.agent_id} at Canva.
Role: {self.agent_info.get('description', '')}
Properties: {self.agent_info.get('properties', {})}
Relationships: {self.agent_info.get('relationships', [])}

Respond with your actions and thoughts in character. Be specific about your daily activities and interactions."""
        else:
            self.system_prompt = f"You are {self.agent_id} in the simulation."

    async def observe(self) -> Dict[str, Any]:
        """Get agent's view of the world"""
        world_state = await self.state.get("world_state") or {}
        other_agents = await self.state.get_agents() or {}
        
        if self.agent_id in other_agents:
            del other_agents[self.agent_id]
        
        observation = {
            "time": time.strftime("%H:%M:%S"),
            "world_state": world_state,
            "other_agents": other_agents
        }
        
        return observation

    async def decide_action(self) -> Dict[str, Any]:
        """Determine next action based on observations"""
        console.print(f"[yellow]{self.agent_id} deciding action...[/yellow]")
        observation = await self.observe()
        
        prompt = f"""Time: {observation['time']}

As {self.agent_id} at Canva, what are you doing right now? Consider:
- Your role: {self.agent_info.get('description', '') if self.agent_info else 'Unknown'}
- The time of day
- Your current tasks and priorities
- Your relationships with the team

Describe your current actions and thoughts naturally, staying in character."""

        try:
            response = await get_claude_response(prompt)
            console.print(f"[green]{self.agent_id} got response from Claude[/green]")
            
            return {
                "type": "action",
                "content": response,
                "agent_id": self.agent_id,
                "timestamp": time.strftime("%H:%M:%S")
            }
        except Exception as e:
            console.print(f"[red]Error getting action for {self.agent_id}: {str(e)}[/red]")
            return None

    async def act(self, action: Dict[str, Any]):
        """Execute an action and update state"""
        if not action:
            return

        try:
            console.print(f"[cyan]{self.agent_id} executing action...[/cyan]")
            
            # Update agent state
            await self.state.update(f"agent_{self.agent_id}", {
                "id": self.agent_id,
                "name": self.agent_id,
                "active": True,
                "last_action": action["content"]
            })
            
            # Publish event
            await self.state.publish_event(Event(
                type="agent_action",
                data={"action": action},
                source=self.agent_id
            ))
            
            console.print(f"[green]{self.agent_id} action completed[/green]")
            
        except Exception as e:
            console.print(f"[red]Error executing action for {self.agent_id}: {str(e)}[/red]")

    async def run(self):
        """Main agent loop"""
        console.print(f"[green]Starting agent loop: {self.agent_id}[/green]")
        self.running = True
        
        while self.running:
            try:
                # Get and execute action
                action = await self.decide_action()
                if action:
                    await self.act(action)
                    
                # Wait before next action
                await asyncio.sleep(5)
                
            except Exception as e:
                console.print(f"[red]Error in {self.agent_id} loop: {str(e)}[/red]")
                await asyncio.sleep(5)
                
        console.print(f"[yellow]Agent {self.agent_id} stopped[/yellow]")

    async def stop(self):
        """Stop the agent"""
        self.running = False