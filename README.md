# WorldMorph

A parallel multi-agent simulation system using Claude for agent intelligence.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Configure environment:
- Copy `.env.example` to `.env`
- Add your Anthropic API key to `.env`

## Running Simulations

Basic simulation:
```bash
python examples/run_simulation.py
```

Monitored simulation:
```bash
python examples/run_monitored_simulation.py
```

Multi-agent simulation:
```bash
python examples/run_multi_agent.py
```

## Project Structure

- `src/`: Core implementation
  - `agent.py`: Agent implementation
  - `controller.py`: Simulation controller
  - `llm.py`: Claude interface
  - `monitor.py`: Visualization
  - `state/`: State management
  - `utils/`: Utilities

- `examples/`: Example scripts
  - Various example implementations

## Adding New Features

1. Agents: Extend the Agent class in `agent.py`
2. World Rules: Modify WorldSimulation in `world.py`
3. Monitoring: Customize WorldMonitor in `monitor.py`