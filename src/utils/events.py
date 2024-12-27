from enum import Enum, auto
from typing import Dict, Any

class EventType(Enum):
    STATE_CHANGED = auto()
    AGENT_SPAWNED = auto()
    AGENT_ACTION = auto()
    WORLD_CREATED = auto()
    WORLD_STARTED = auto()
    WORLD_STOPPED = auto()

def create_event(event_type: EventType, data: Dict[str, Any], source: str) -> Dict[str, Any]:
    """Create a properly formatted event"""
    return {
        "type": event_type.name,
        "data": data,
        "source": source,
        "timestamp": None  # You could add actual timestamps here
    }