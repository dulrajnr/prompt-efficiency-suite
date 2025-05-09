# Contributing to Prompt Efficiency Suite

We love your input! We want to make contributing to the Prompt Efficiency Suite as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with GitHub

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html)

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/prompt-efficiency/prompt-efficiency-suite/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/prompt-efficiency/prompt-efficiency-suite/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Process

1. Set up your development environment:
   ```bash
   # Clone the repository
   git clone https://github.com/prompt-efficiency/prompt-efficiency-suite.git
   cd prompt-efficiency-suite

   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install development dependencies
   pip install -e ".[dev]"
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Check code style:
   ```bash
   black .
   isort .
   flake8
   mypy .
   ```

## Code Style

We use:
- [Black](https://black.readthedocs.io/) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [flake8](https://flake8.pycqa.org/) for linting
- [mypy](https://mypy.readthedocs.io/) for type checking

## Documentation

- All new features should be documented
- Update the README.md if needed
- Add docstrings to all new functions and classes
- Update API documentation if you change the API

## License

By contributing, you agree that your contributions will be licensed under its MIT License. 