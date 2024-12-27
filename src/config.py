from typing import Dict, Any, List
from dataclasses import dataclass
import json
import re
from rich.console import Console
from .llm import get_claude_response

console = Console()

@dataclass
class SimulationConfig:
    world_description: str
    agents: List[Dict[str, Any]]
    system_prompt: str
    initial_state: Dict[str, Any]
    
    @classmethod
    async def from_prompt(cls, prompt: str):
        """Create simulation config by having Claude analyze the prompt"""
        parse_prompt = """Analyze the provided description and generate a simulation configuration. Format your entire response as a strict JSON object with this exact structure:

{
    "world": {
        "description": "Brief summary of the world",
        "characteristics": ["characteristic 1", "characteristic 2"],
        "rules": ["rule 1", "rule 2"]
    },
    "agents": [
        {
            "name": "name of agent",
            "description": "what this agent does",
            "properties": {"key": "value"},
            "relationships": [{"to": "other agent", "type": "relationship"}]
        }
    ]
}

Description to analyze:
""" + prompt

        try:
            # Get Claude's analysis
            console.print("[cyan]Requesting analysis from Claude...[/cyan]")
            analysis_str = await get_claude_response(parse_prompt)
            console.print("[green]Received response from Claude[/green]")
            
            # Debug: Print raw response
            console.print("\n[dim]Raw Response:[/dim]")
            console.print(analysis_str)
            
            # Find the JSON part
            json_start = analysis_str.find('{')
            json_end = analysis_str.rfind('}') + 1
            
            if json_start == -1 or json_end <= 0:
                console.print("[red]No JSON found in response[/red]")
                raise ValueError("No JSON found in response")
            
            json_str = analysis_str[json_start:json_end]
            console.print("\n[dim]Extracted JSON:[/dim]")
            console.print(json_str)
            
            # Clean up the JSON string
            json_str = re.sub(r'[\n\r\t]', '', json_str)  # Remove whitespace
            json_str = re.sub(r',\s*([}\]])', r'\1', json_str)  # Fix trailing commas
            json_str = re.sub(r'\\', '', json_str)  # Remove escapes
            
            console.print("\n[dim]Cleaned JSON:[/dim]")
            console.print(json_str)
            
            # Parse JSON
            try:
                analysis = json.loads(json_str)
                console.print("[green]Successfully parsed JSON[/green]")
            except json.JSONDecodeError as e:
                console.print(f"[red]JSON parse error: {str(e)}[/red]")
                raise
            
            # Construct system prompt
            system_prompt = f"""<sys>You are in a CLI mood today. You are participating in an imaginative world simulation. This world is defined as:

{analysis['world']['description']}

Key characteristics:
{chr(10).join('- ' + c for c in analysis['world']['characteristics'])}

Rules:
{chr(10).join('- ' + r for r in analysis['world']['rules'])}

When you observe the world, describe what you see in rich detail. When you perform actions, narrate them in the style of the simulation. Stay in character as your assigned entity.</sys>"""

            # Set up initial state
            initial_state = {
                "world_description": prompt,
                "world_analysis": analysis['world'],
                "active_agents": 0,
                "simulation_status": "initializing",
                "agents": analysis['agents']
            }
            
            return cls(
                world_description=prompt,
                agents=analysis['agents'],
                system_prompt=system_prompt,
                initial_state=initial_state
            )
        
        except Exception as e:
            console.print(f"[red]Error creating simulation config: {str(e)}[/red]")
            console.print(f"[dim]Prompt used:[/dim]\n{parse_prompt}")
            raise