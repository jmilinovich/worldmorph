from typing import Any, Dict, List, Callable, Set
from .interface import WorldState, Event

class InMemoryState(WorldState):
    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.subscribers: Dict[str, Callable[[Event], None]] = {}
        self.agents: Dict[str, Dict[str, Any]] = {}
    
    async def update(self, key: str, value: Any) -> None:
        """Update state at key with value"""
        print(f"Updating state: {key}")  # Debug logging
        
        self.state[key] = value
        
        # Special handling for agent-related updates
        if key == "agents":
            # If we're updating the agents list, convert it to our internal format
            if isinstance(value, list):
                for agent in value:
                    agent_id = agent.get('name', 'unknown')
                    self.agents[agent_id] = {
                        'id': agent_id,
                        'active': True,
                        'last_action': None,
                        'status': 'initialized',
                        **agent  # Include all the agent data
                    }
        elif key.startswith("agent_"):
            # Individual agent updates
            agent_id = key.replace("agent_", "")
            if agent_id in self.agents:
                self.agents[agent_id].update(value)
            else:
                self.agents[agent_id] = value
        
        # Notify subscribers of state change
        await self.publish_event(Event(
            type="state_changed",
            data={
                "key": key,
                "value": value,
                "timestamp": "now"
            },
            source="state_manager"
        ))
    
    async def get(self, key: str) -> Any:
        """Get value at key"""
        return self.state.get(key)
    
    async def publish_event(self, event: Event) -> None:
        """Publish an event to all subscribers or specific targets"""
        if event.targets:
            # Send only to specific agents
            for agent_id in event.targets:
                if agent_id in self.subscribers:
                    await self.subscribers[agent_id](event)
        else:
            # Broadcast to all subscribers
            for subscriber in self.subscribers.values():
                await subscriber(event)
    
    async def subscribe(self, agent_id: str, callback: Callable[[Event], None]) -> None:
        """Subscribe to events with agent identifier"""
        print(f"New subscriber: {agent_id}")  # Debug logging
        self.subscribers[agent_id] = callback
    
    async def get_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all agents"""
        return self.agents.copy()  # Return a copy to prevent external modifications
    
    async def get_agent_state(self, agent_id: str) -> Dict[str, Any]:
        """Get state of a specific agent"""
        return self.agents.get(agent_id, {})