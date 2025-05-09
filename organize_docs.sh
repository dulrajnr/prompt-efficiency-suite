#!/bin/bash

# Create directory structure
mkdir -p docs/{getting-started,components,features,api,configuration,deployment,development,troubleshooting,best-practices,support}

# Move files to appropriate directories
# Getting Started
mv docs/getting-started.md docs/getting-started/
mv docs/quickstart.md docs/getting-started/
mv docs/usage_guide.md docs/getting-started/

# Components
mv docs/cli.md docs/components/
mv docs/web-ui.md docs/components/
mv docs/jetbrains-plugin.md docs/components/
mv docs/orchestrator.md docs/components/
mv docs/components.md docs/components/

# Features
mv docs/analyzer.md docs/features/
mv docs/optimizer.md docs/features/
mv docs/model_translator.md docs/features/
mv docs/translator.md docs/features/
mv docs/tester.md docs/features/
mv docs/advanced-features.md docs/features/

# API
mv docs/api.md docs/api/
mv docs/api-reference.md docs/api/
mv docs/api-endpoints.md docs/api/
mv docs/openapi.yaml docs/api/

# Development
mv docs/development.md docs/development/
mv docs/contributing.md docs/development/
mv docs/TECHNICAL_SPEC.md docs/development/
mv docs/IMPLEMENTATION_PLAN.md docs/development/

# Troubleshooting
mv docs/troubleshooting.md docs/troubleshooting/

# Best Practices
mv docs/best-practices.md docs/best-practices/
mv docs/PATTERNS.md docs/best-practices/

# Examples
mv docs/examples.md docs/examples/

# Keep README.md and index.md in the root docs directory 