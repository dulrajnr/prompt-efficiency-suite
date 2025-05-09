# Contributing to Prompt Efficiency Suite

Thank you for your interest in contributing to the Prompt Efficiency Suite! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read it before contributing.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip
- virtualenv (recommended)

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/prompt-efficiency-suite.git
   cd prompt-efficiency-suite
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

### Branching Strategy

- `main`: Production-ready code
- `develop`: Development branch
- Feature branches: `feature/feature-name`
- Bug fix branches: `fix/bug-name`
- Release branches: `release/vX.Y.Z`

### Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Run tests:
   ```bash
   pytest
   ```

4. Run linting:
   ```bash
   flake8
   black .
   isort .
   ```

5. Commit your changes:
   ```bash
   git commit -m "feat: add new feature"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a Pull Request

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

### Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update the changelog
5. Request review from maintainers

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_compressor.py

# Run with coverage
pytest --cov=prompt_efficiency_suite
```

### Writing Tests

- Use pytest fixtures
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Test edge cases
- Example:
  ```python
  def test_compressor_compression():
      # Arrange
      compressor = BaseCompressor()
      text = "Test prompt"
      
      # Act
      result = await compressor.compress(text)
      
      # Assert
      assert result.compression_ratio > 0
      assert result.compressed_text != ""
  ```

## Documentation

### Writing Documentation

- Use clear, concise language
- Include code examples
- Document all public APIs
- Follow the existing style
- Example:
  ```python
  def compress(text: str) -> str:
      """Compress the input text.
      
      Args:
          text: The text to compress
          
      Returns:
          The compressed text
          
      Example:
          >>> compress("This is a test")
          "Test"
      """
  ```

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make html
```

## Code Style

### Python Style Guide

- Follow PEP 8
- Use type hints
- Write docstrings
- Use meaningful names
- Example:
  ```python
  from typing import List, Optional

  def process_prompts(
      prompts: List[str],
      target_ratio: Optional[float] = None
  ) -> List[str]:
      """Process a list of prompts.
      
      Args:
          prompts: List of prompts to process
          target_ratio: Optional target compression ratio
          
      Returns:
          List of processed prompts
      """
  ```

### Linting

We use:
- flake8 for linting
- black for code formatting
- isort for import sorting
- mypy for type checking

Run all checks:
```bash
flake8
black .
isort .
mypy .
```

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- MAJOR: Incompatible API changes
- MINOR: Backwards-compatible functionality
- PATCH: Backwards-compatible bug fixes

### Creating a Release

1. Update version in:
   - `setup.py`
   - `__init__.py`
   - Documentation

2. Update changelog

3. Create release branch:
   ```bash
   git checkout -b release/vX.Y.Z
   ```

4. Create release commit:
   ```bash
   git commit -m "chore: release vX.Y.Z"
   ```

5. Create tag:
   ```bash
   git tag -a vX.Y.Z -m "Version X.Y.Z"
   ```

6. Push changes:
   ```bash
   git push origin release/vX.Y.Z
   git push origin vX.Y.Z
   ```

7. Create GitHub release

## Project Structure

```
prompt-efficiency-suite/
├── src/
│   └── prompt_efficiency_suite/
│       ├── __init__.py
│       ├── compressor.py
│       ├── analyzer.py
│       ├── metrics.py
│       ├── optimizer.py
│       ├── macro.py
│       ├── scanner.py
│       ├── budget.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_compressor.py
│   ├── test_analyzer.py
│   └── ...
├── docs/
│   ├── index.md
│   ├── getting-started.md
│   └── ...
├── setup.py
├── requirements.txt
├── README.md
└── CONTRIBUTING.md
```

## Getting Help

- Check the documentation
- Search existing issues
- Join our community chat
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the project's license. 