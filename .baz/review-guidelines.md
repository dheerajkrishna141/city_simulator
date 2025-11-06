# Code Review Guidelines - CitySim Project

## Overview

CitySim is a Python-based city simulation game. These guidelines ensure code quality, maintainability, and consistency across the project.

## Code Style & Standards

### Python Style (PEP 8)

- **Line Length**: Maximum 100 characters (88 for Black compatibility)
- **Indentation**: 4 spaces, no tabs
- **Naming Conventions**:
  - Classes: `PascalCase` (e.g., `Zone`, `Building`, `Infrastructure`)
  - Functions/Methods: `snake_case` (e.g., `calculate_desirability`, `place_zone`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `ZONE_TYPES`, `MAX_DEVELOPMENT`)
  - Private methods: Prefix with `_` (e.g., `_calculate_proximity`)

### Type Hints

- **Required** for all public methods and functions
- **Required** for method parameters and return types
- Example:
  ```python
  def calculate_desirability(self, city: City) -> float:
      """Calculate desirability score."""
      ...
  ```

### Documentation

- **Required** for all classes, public methods, and complex logic
- Use docstrings with format:

  ```python
  """
  Brief description.

  Args:
      param_name: Description of parameter

  Returns:
      Description of return value
  """
  ```

## Code Quality Principles

### DRY (Don't Repeat Yourself)

- ❌ **Reject**: Code with duplicate logic across multiple methods
- ✅ **Require**: Extract common patterns into reusable methods
- **Example**: Multiple proximity calculation methods should be consolidated

### Single Responsibility

- Each class should have one clear purpose
- Each method should do one thing well
- Keep methods under 50 lines when possible

### Magic Numbers

- ❌ **Reject**: Hardcoded numbers without explanation
- ✅ **Require**: Named constants for all configuration values
- Example:

  ```python
  # Bad
  if score > 80:
      state = 'thriving'

  # Good
  THRIVING_THRESHOLD = 80
  if score > THRIVING_THRESHOLD:
      state = 'thriving'
  ```

## Performance Considerations

### Computational Complexity

- Flag nested loops over large datasets (O(n²) or worse)
- Suggest caching for expensive calculations
- Consider spatial indexing for grid-based proximity searches

### Memory Management

- Avoid unnecessary object creation in hot paths
- Clear large data structures when no longer needed

## Testing Requirements

### Coverage

- **Minimum**: 70% code coverage for new features
- **Required**: Tests for all bug fixes
- **Edge Cases**: Must include boundary condition tests

### Test Organization

- Unit tests: Test individual components in isolation
- Integration tests: Test component interactions
- Use mocks/fixtures to isolate dependencies
- Tests must be fast, deterministic, and repeatable

### Test Naming

```python
def test_<component>_<scenario>_<expected_behavior>():
    """Test description."""
```

## Game-Specific Guidelines

### City Grid Operations

- Always validate coordinates with `is_valid_position()` before grid access
- Check cell occupation before placement
- Update coverage sets after infrastructure changes

### Zone Development

- Verify requirements (power, water, roads) before allowing development
- Update desirability scores periodically, not every frame
- Consider neighbor effects on development

### Building Operations

- Check construction costs before placement
- Track building age and efficiency degradation
- Maintain consistent maintenance cost calculations

### Infrastructure

- Update coverage areas after placement/removal
- Verify connection to road network where required
- Calculate pollution impact for industrial infrastructure

## Version Control

### Commit Guidelines

- Write clear, descriptive commit messages
- Use present tense ("Add feature" not "Added feature")
- Reference issue numbers when applicable
- Keep commits focused and atomic

### Files to Exclude

- ❌ Do not commit: `__pycache__/`, `*.pyc`, `*.pyo`
- ❌ Do not commit: IDE-specific files (except `.vscode/` for team consistency)
- ❌ Do not commit: Local configuration overrides
- ✅ Include: `.gitignore` with proper exclusions

## Security & Data Validation

### Input Validation

- Validate all user inputs (coordinates, zone types, building types)
- Check bounds before array/grid access
- Validate enum-like values against allowed lists

### Error Handling

- Use specific exception types
- Provide helpful error messages
- Don't silently fail; log or return error status

## Code Review Checklist

Before approving any PR, verify:

- [ ] Code follows PEP 8 style guidelines
- [ ] Type hints are present for public methods
- [ ] Docstrings explain complex logic
- [ ] No duplicate code (DRY principle)
- [ ] Magic numbers replaced with named constants
- [ ] Tests added/updated for changes
- [ ] Edge cases are handled
- [ ] Performance impact considered for grid operations
- [ ] No `__pycache__` or compiled files committed
- [ ] Input validation present where needed
- [ ] Error messages are helpful
- [ ] Code is readable and maintainable

## Severity Levels

### Critical (🔴 Must Fix)

- Security vulnerabilities
- Data corruption risks
- Game-breaking bugs
- Missing input validation on public APIs

### Major (🟡 Should Fix)

- Performance issues (O(n²) on large datasets)
- Significant code duplication
- Missing tests for new features
- Poor error handling

### Minor (🟢 Consider)

- Style guide violations
- Missing docstrings on private methods
- Opportunities for refactoring
- Optimization suggestions

## Resources

- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- Project-specific: See `agents.md` for testing guidelines
