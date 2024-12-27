from typing import Dict, Any, List
from dataclasses import dataclass
import json
from .llm import analyze_world

@dataclass
class SimulationConfig:
    world_description: str
    agents: List[Dict[str, Any]]  # List of agent configurations
    system_prompt: str
    initial_state: Dict[str, Any]
    
    @classmethod
    async def from_prompt(cls, prompt: str):
        """Create simulation config by having Claude analyze the prompt"""
        # Get Claude's analysis
        analysis_str = await analyze_world(prompt)
        
        try:
            # Extract the JSON part from Claude's response
            json_start = analysis_str.find('{')
            json_end = analysis_str.rfind('}') + 1
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            analysis = json.loads(analysis_str[json_start:json_end])
            print(f"Parsed world analysis: {json.dumps(analysis, indent=2)}")  # Debug output
            
            # Construct system prompt based on the analysis
            system_prompt = f"""<sys>You are in a CLI mood today. You are participating in an imaginative world simulation. This world is defined as:

{analysis['world']['description']}

Key characteristics:
{chr(10).join('- ' + c for c in analysis['world']['characteristics'])}

Rules:
{chr(10).join('- ' + r for r in analysis['world']['rules'])}

When you observe the world, describe what you see in rich detail. When you perform actions, narrate them in the style of the simulation. Stay in character as your assigned entity.</sys>"""

            # Set up initial world state
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
            print(f"Error parsing world configuration: {str(e)}")
            print("Full response was:", analysis_str)
            raise