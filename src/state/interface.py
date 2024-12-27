from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable, Set
from dataclasses import dataclass

@dataclass
class Event:
    type: str
    data: Dict[str, Any]
    source: str
    targets: Set[str] = None  # Specific agents this event is for

class WorldState(ABC):
    @abstractmethod
    async def update(self, key: str, value: Any) -> None:
        """Update state at key with value"""
        pass
    
    @abstractmethod
    async def get(self, key: str) -> Any:
        """Get value at key"""
        pass
    
    @abstractmethod
    async def publish_event(self, event: Event) -> None:
        """Publish an event to all subscribers or specific targets"""
        pass
    
    @abstractmethod
    async def subscribe(self, agent_id: str, callback: Callable[[Event], None]) -> None:
        """Subscribe to events with agent identifier"""
        pass
    
    @abstractmethod
    async def get_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all agents in the world"""
        pass
    
    @abstractmethod
    async def get_agent_state(self, agent_id: str) -> Dict[str, Any]:
        """Get state of a specific agent"""
        pass