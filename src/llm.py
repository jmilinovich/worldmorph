import os
import asyncio
from typing import List, Dict
from anthropic import Anthropic # type: ignore

def get_client():
    """Get authenticated Anthropic client"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")
    
    # Print first few chars of key for debugging
    print(f"Using API key: {api_key[:8]}...")
    return Anthropic(api_key=api_key)

async def get_claude_response(prompt: str) -> str:
    """Get a response from Claude"""
    try:
        client = get_client()
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0  # Use low temperature for consistent structured output
        )
        
        return response.content[0].text
    except Exception as e:
        print(f"Error getting Claude response: {e}")
        raise  # Re-raise to handle in calling code

async def analyze_world(description: str) -> Dict:
    """Have Claude analyze a world description"""
    prompt = f"""Please analyze this world description and extract:
1. The key characteristics of the world/environment
2. The entities/agents that exist in it, including their properties and relationships
3. Any specific rules or dynamics that govern this world

Format your response as JSON with this structure:
{{
    "world": {{
        "description": "Summary of the world",
        "characteristics": ["key feature 1", "key feature 2", ...],
        "rules": ["rule 1", "rule 2", ...]
    }},
    "agents": [
        {{
            "name": "agent name",
            "description": "agent description",
            "properties": {{"property1": "value1", ...}},
            "relationships": [{{"to": "other agent name", "type": "relationship type"}}]
        }},
        ...
    ]
}}

Here's the world description to analyze:

{description}

Remember to return ONLY valid JSON that matches the structure above."""
    
    response = await get_claude_response(prompt)
    return response