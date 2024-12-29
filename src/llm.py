import os
import asyncio
from typing import List, Dict
from anthropic import Anthropic
from rich.console import Console
from pathlib import Path
from dotenv import load_dotenv
from .llm_cache import cache

console = Console()

def verify_api_key():
    """Verify that we have a valid API key"""
    # Try to load from .env
    load_dotenv()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("""ANTHROPIC_API_KEY not found in environment

Please create a .env file in the project root with your API key:
ANTHROPIC_API_KEY=your_key_here

You can get an API key from: https://console.anthropic.com/""")
        
    return api_key

def get_client():
    """Get authenticated Anthropic client"""
    api_key = verify_api_key()
    return Anthropic(api_key=api_key)

async def get_claude_response(prompt: str) -> str:
    """Get a response from Claude with caching"""
    try:
        # Check cache first
        cached_response = cache.get([prompt])
        if cached_response:
            console.print("[dim]Cache hit - using cached response[/dim]")
            return cached_response

        console.print("[dim]Cache miss - calling Claude API[/dim]")
        
        # Verify API key before making call
        verify_api_key()
        
        # If not in cache, call API
        MAX_RETRIES = 3
        RETRY_DELAY = 1  # seconds
        
        for attempt in range(MAX_RETRIES):
            try:
                client = get_client()
                response = client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=4096,
                    temperature=0.0,  # Use consistent outputs for better caching
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                result = response.content[0].text
                
                # Cache the response
                cache.set([prompt], result)
                
                return result
                
            except Exception as e:
                console.print(f"[yellow]Attempt {attempt + 1} failed: {str(e)}[/yellow]")
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
                else:
                    raise
                    
    except Exception as e:
        console.print(f"[red]Error getting Claude response: {str(e)}[/red]")
        raise

async def analyze_simulation_metrics(metrics_data: Dict, world_description: str) -> str:
    """Have Claude analyze simulation metrics"""
    prompt = f"""Given the following simulation metrics and world description, provide an analysis of the simulation outcomes.

World Description:
{world_description}

Metrics Data:
{metrics_data}

Please analyze:
1. Key trends and patterns
2. Notable achievements or issues
3. Recommendations for improvement
4. Overall simulation effectiveness

Format your response as a structured report."""

    return await get_claude_response(prompt)