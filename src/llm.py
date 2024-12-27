import os
import asyncio
from typing import List, Dict
from anthropic import Anthropic
from rich.console import Console

console = Console()

def get_client():
    """Get authenticated Anthropic client"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment")
    
    console.print(f"[dim]Using API key: {api_key[:8]}...[/dim]")
    return Anthropic(api_key=api_key)

async def get_claude_response(prompt: str) -> str:
    """Get a response from Claude with retries"""
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    
    # Add JSON instructions to the prompt
    prompt = f"""IMPORTANT: Your response must be a valid JSON object. Do not include any other text, explanations, or formatting.

{prompt}

Remember: Return ONLY the JSON object with no additional text."""
    
    for attempt in range(MAX_RETRIES):
        try:
            client = get_client()
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0.0,  # Use consistent outputs
                messages=[
                    {"role": "user", "content": prompt}
                ],
                system="You are a JSON generator. Always return valid JSON objects with no additional text."
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            console.print(f"[yellow]Attempt {attempt + 1} failed: {str(e)}[/yellow]")
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
            else:
                raise