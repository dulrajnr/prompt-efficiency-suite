#!/bin/bash

# Exit on error
set -e

echo "Installing required dependencies..."

# Install safety for security checks
pip install safety

# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install test dependencies
pip install -r requirements-test.txt

# Install additional required packages
pip install spacy python-multipart tenacity cachetools python-jose passlib bcrypt python-magic

# Download spaCy model
python -m spacy download en_core_web_sm

# Install development tools
pip install flake8 pre-commit twine build

# Initialize pre-commit hooks
pre-commit install

echo "Dependencies installed successfully!" 