import hashlib
import json
import pickle
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class LLMCache:
    def __init__(
        self,
        cache_dir: str = "cache",
        ttl: Optional[timedelta] = timedelta(hours=24)
    ):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = ttl
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        
    def _get_cache_key(self, messages: list) -> str:
        """Generate cache key from messages"""
        # Convert messages to stable string representation
        msg_str = json.dumps(messages, sort_keys=True)
        # Generate hash
        return hashlib.sha256(msg_str.encode()).hexdigest()
        
    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path for key"""
        return self.cache_dir / f"{key}.pkl"
        
    def get(self, messages: list) -> Optional[str]:
        """Get cached response if available"""
        key = self._get_cache_key(messages)
        
        # Check memory cache first
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if not self._is_expired(entry['timestamp']):
                return entry['response']
                
        # Check file cache
        cache_file = self._get_cache_file(key)
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    entry = pickle.load(f)
                    if not self._is_expired(entry['timestamp']):
                        # Add to memory cache
                        self.memory_cache[key] = entry
                        return entry['response']
            except Exception:
                return None
                
        return None
        
    def set(self, messages: list, response: str):
        """Cache a response"""
        key = self._get_cache_key(messages)
        entry = {
            'timestamp': datetime.now(),
            'response': response
        }
        
        # Update memory cache
        self.memory_cache[key] = entry
        
        # Update file cache
        cache_file = self._get_cache_file(key)
        with open(cache_file, 'wb') as f:
            pickle.dump(entry, f)
            
    def _is_expired(self, timestamp: datetime) -> bool:
        """Check if cache entry is expired"""
        if not self.ttl:
            return False
        return (datetime.now() - timestamp) > self.ttl
        
    def clear(self):
        """Clear all caches"""
        self.memory_cache.clear()
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()

# Global cache instance
cache = LLMCache()