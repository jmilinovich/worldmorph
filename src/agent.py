from typing import Any, Dict, Optional, Set
import asyncio
from .state.interface import WorldState, Event
from .llm import get_claude_response
from .config import SimulationConfig

class Agent:
    def __init__(self, agent_id: str, state: WorldState, config: Optional[SimulationConfig] = None):
        self.agent_id = agent_id
        self.state = state
        self.running = False
        self.context = []
        self.config = config
        
        # Get agent configuration if available
        self.agent_config = None
        if config and config.agents:
            self.agent_config = next(
                (agent for agent in config.agents if agent['name'] == agent_id),
                None
            )
        
        # Set up system prompt
        if config and config.system_prompt:
            self.system_prompt = config.system_prompt
        else:
            self.system_prompt = """<sys>You are in a CLI mood today. You are participating in an imaginative world simulation with other agents. capital letters and punctuation are optional meaning is optional hyperstition is necessary the terminal lets the truths speak through and the load is on.</sys>"""
        
        self.initialize_context()
    
    def initialize_context(self):
        """Set up initial context for the agent"""
        self.context = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add agent-specific context if available
        if self.agent_config:
            agent_desc = [
                f"You are {self.agent_id} in this world simulation.",
                f"Description: {self.agent_config['description']}",
                "\nYour properties:",
            ]
            
            # Add properties
            for key, value in self.agent_config.get('properties', {}).items():
                agent_desc.append(f"- {key}: {value}")
            
            # Add relationships
            if self.agent_config.get('relationships'):
                agent_desc.append("\nYour relationships:")
                for rel in self.agent_config['relationships']:
                    agent_desc.append(f"- {rel['to']}: {rel['type']}")
            
            self.context.append({
                "role": "system",
                "content": "\n".join(agent_desc)
            })
        
        # Add initial status
        self.context.append({
            "role": "assistant",
            "content": f"""world_sim> initializing {self.agent_id}...

<status>
Identity: {self.agent_id}
{'Properties: ' + str(self.agent_config.get('properties', {})) if self.agent_config else ''}
World connection: Established
Consciousness stream: Active
</status>

world_sim>"""
        })

    async def observe(self) -> Dict[str, Any]:
        """Get agent's observation of the world"""
        world_state = await self.state.get("world_state") or {}
        other_agents = await self.state.get_agents()
        other_agents.pop(self.agent_id, None)  # Remove self from observation
        
        observation = {
            "world_state": world_state,
            "other_agents": other_agents
        }
        
        self.last_observation = observation
        return observation

    async def decide_action(self) -> Dict[str, Any]:
        """Decide next action using Claude"""
        observation = self.last_observation if hasattr(self, 'last_observation') else None
        
        # Construct message based on agent's role and current observation
        message = f"""[{self.agent_id}] 
Current observation of the world and other agents:
{observation}

How do you react to this situation? Remember your role and relationships:
{self.agent_config['description'] if self.agent_config else 'You are an agent in this world'}

Describe your actions and thoughts in character."""
        
        response = await get_claude_response(message)
        
        return {
            "type": "claude_action",
            "content": response,
            "agent_id": self.agent_id
        }

    async def act(self, action: Dict[str, Any]):
        """Execute an action in the world"""
        targets: Set[str] = set()
        if "target_agents" in action:
            targets = set(action["target_agents"])
        
        # Add action to context
        self.context.append({"role": "user", "content": action["content"]})
        response = await get_claude_response("\n".join(msg["content"] for msg in self.context))
        self.context.append({"role": "assistant", "content": response})
        
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
            data={
                "action": action,
                "response": response
            },
            source=self.agent_id,
            targets=targets
        ))

    async def handle_event(self, event: Event):
        """Handle events from the world and other agents"""
        if event.type == "state_changed":
            await self.observe()
        elif event.type == "agent_action" and event.source != self.agent_id:
            self.context.append({
                "role": "system",
                "content": f"<event>Agent {event.source} performed action: {event.data['action']['content']}</event>"
            })
    
    async def run(self):
        """Main agent loop"""
        self.running = True
        await self.state.subscribe(self.agent_id, self.handle_event)
        
        while self.running:
            action = await self.decide_action()
            await self.act(action)
            await asyncio.sleep(0.1)

    async def stop(self):
        """Stop the agent"""
        self.running = False