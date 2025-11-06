# Python Game Development Best Practices

## Clean Code

- Follow PEP 8 style guidelines.
- Use meaningful names for variables, classes, and functions.
- Keep functions and classes small and focused.

## Project Structure

- Organize code into logical modules (e.g., agents, assets, systems).
- Separate game logic, rendering, and configuration.

## Maintainability

- Write clear comments and docstrings.
- Use type hints for better readability.
- Keep code DRY (Don’t Repeat Yourself).

## Testing Guidelines for Agents

- Write unit tests for core agent behaviors (e.g., movement, state transitions, decision-making).
- Keep tests **fast, deterministic, and repeatable**.
- Use mock data or fixtures to isolate agents from other systems.
- Cover edge cases (e.g., invalid inputs, extreme values, unusual interactions).
- Test agents in both **isolation** (unit tests) and **integration** (with other agents/systems).
- Automate test execution with a framework like `pytest`.
