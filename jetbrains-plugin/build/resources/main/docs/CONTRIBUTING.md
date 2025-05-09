# Contributing to Prompt Efficiency Plugin

Thank you for your interest in contributing to the Prompt Efficiency Plugin! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites
- JDK 11 or later
- IntelliJ IDEA (recommended)
- Gradle 7.0 or later

### Getting Started
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/prompt-efficiency.git
   ```
3. Add the original repository as upstream:
   ```bash
   git remote add upstream https://github.com/original-owner/prompt-efficiency.git
   ```
4. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Building the Plugin
1. Open the project in IntelliJ IDEA
2. Import the Gradle project
3. Build the plugin:
   ```bash
   ./gradlew build
   ```
4. Run tests:
   ```bash
   ./gradlew test
   ```

## Development Guidelines

### Code Style
- Follow Kotlin coding conventions
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused
- Write unit tests for new features

### Architecture
- Follow the existing package structure
- Use dependency injection where appropriate
- Keep UI and business logic separate
- Follow the plugin's state management pattern

### Testing
- Write unit tests for new features
- Include integration tests for UI components
- Test edge cases and error conditions
- Maintain or improve test coverage

### Documentation
- Update README.md for new features
- Add Javadoc comments for public APIs
- Document configuration options
- Update user documentation

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation with any new features
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

### Pull Request Guidelines
- Use a clear and descriptive title
- Reference any related issues
- Include screenshots for UI changes
- Describe the changes and their impact
- Follow the existing code style

## Feature Requests and Bug Reports

### Feature Requests
- Use the issue tracker
- Provide a clear description
- Explain the use case
- Suggest implementation if possible

### Bug Reports
- Use the issue tracker
- Include steps to reproduce
- Provide expected and actual behavior
- Include relevant logs and screenshots

## Release Process

### Versioning
- Follow semantic versioning
- Update version in build.gradle
- Update CHANGELOG.md
- Tag releases in git

### Release Checklist
1. Update version numbers
2. Update documentation
3. Run all tests
4. Build release artifacts
5. Create release notes
6. Tag the release
7. Deploy to plugin repository

## Code of Conduct

### Our Pledge
- Be respectful and inclusive
- Be patient and welcoming
- Be thoughtful
- Be collaborative

### Our Standards
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Gracefully accept constructive criticism
- Focus on what is best for the community

## Getting Help

- Check existing documentation
- Search existing issues
- Join our community chat
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License. 