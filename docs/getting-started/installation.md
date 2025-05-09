# Installation Guide

## Overview

This guide will help you install the Prompt Efficiency Suite and its components.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher (for Web UI)
- Java 11 or higher (for JetBrains Plugin)
- Git

## Installation Methods

### 1. Using pip (CLI and Core Components)

```bash
# Install the core package
pip install prompt-efficiency-suite

# Install with all optional dependencies
pip install prompt-efficiency-suite[all]
```

### 2. Using Docker

```bash
# Pull the Docker image
docker pull prompt-efficiency/suite:latest

# Run the container
docker run -p 8000:8000 prompt-efficiency/suite
```

### 3. From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/prompt-efficiency-suite.git
cd prompt-efficiency-suite

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install the package
pip install -e .
```

## Component-Specific Installation

### Web UI

```bash
# Install dependencies
cd web-ui
npm install

# Build the UI
npm run build

# Start the development server
npm start
```

### JetBrains Plugin

1. Download the plugin from the JetBrains Marketplace
2. In your JetBrains IDE:
   - Go to Settings/Preferences
   - Navigate to Plugins
   - Click the gear icon
   - Select "Install Plugin from Disk"
   - Choose the downloaded plugin file

### VS Code Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Prompt Efficiency Suite"
4. Click Install

## Configuration

### 1. Environment Variables

```bash
# API Configuration
export PROMPT_API_KEY=your_api_key
export PROMPT_API_URL=http://localhost:8000

# Model Configuration
export DEFAULT_MODEL=gpt-4
export MAX_TOKENS=4096
```

### 2. Configuration File

Create a `config.yaml` file:

```yaml
api:
  key: your_api_key
  url: http://localhost:8000
  timeout: 30

models:
  default: gpt-4
  max_tokens: 4096
  temperature: 0.7

features:
  analysis: true
  optimization: true
  cost_tracking: true
```

## Verification

### 1. CLI Verification

```bash
# Check installation
prompt-efficiency --version

# Test basic functionality
prompt-efficiency analyze "Test prompt"
```

### 2. API Verification

```bash
# Check API health
curl http://localhost:8000/health

# Test authentication
curl -H "Authorization: Bearer $PROMPT_API_KEY" http://localhost:8000/api/v1/health
```

### 3. Web UI Verification

1. Open http://localhost:3000
2. Log in with your credentials
3. Check the dashboard

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check API URL configuration
   - Verify API key
   - Check network connectivity

2. **Module Not Found**
   - Verify Python version
   - Check virtual environment
   - Reinstall dependencies

3. **Plugin Installation Failed**
   - Check IDE version compatibility
   - Verify plugin file integrity
   - Clear IDE cache

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Basic Concepts](concepts.md)
- [Configuration Guide](../configuration/global.md)

## Support

If you encounter any issues during installation:
- Check the [Troubleshooting Guide](../troubleshooting/common-issues.md)
- Visit our [GitHub Issues](https://github.com/yourusername/prompt-efficiency-suite/issues)
- Contact support at support@prompt.com 