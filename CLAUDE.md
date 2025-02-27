# Startup Success Forecasting Framework Guide

## Commands
- Run app: `python app.py`
- Run experiment: `python experiments/experiment.py`
- Run single test: `python -m unittest path/to/test_file.py::TestClass::test_method`
- Run all tests: `python -m unittest discover`

## Code Style
- Import order: standard library, third-party, local modules
- Use type hints for all functions and classes
- Use dataclasses for structured data
- Class names: CamelCase 
- Function/variable names: snake_case
- Error handling: Use try/except with specific exceptions, log errors using logging module
- Model objects use model_dump() methods for serialization
- All agents follow base_agent.py pattern
- Document functions with docstrings
- Use Enum classes for enumerated types
- Log important operations with proper logging level