import asyncio
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from dotenv import load_dotenv
from src.llm import get_claude_response

async def main():
    load_dotenv()
    
    try:
        response = await get_claude_response("Say hello!")
        print("\nAPI test successful!")
        print("Response:", response)
    except Exception as e:
        print("\nAPI test failed!")
        print("Error:", str(e))
        print("\nChecking environment:")
        print("API KEY present:", bool(os.getenv("ANTHROPIC_API_KEY")))
        if os.getenv("ANTHROPIC_API_KEY"):
            print("API KEY starts with:", os.getenv("ANTHROPIC_API_KEY")[:8])

if __name__ == "__main__":
    asyncio.run(main())