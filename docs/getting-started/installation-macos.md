# macOS Installation Guide

This guide will help you install the Prompt Efficiency Suite on macOS.

## Prerequisites

- macOS 10.15 (Catalina) or later
- Python 3.8 or later
- Xcode Command Line Tools
- Homebrew (recommended)

## Installation Methods

### 1. Using pip (Recommended)

1. Open Terminal and create a virtual environment:
```bash
python3 -m venv ~/prompt-efficiency-env
source ~/prompt-efficiency-env/bin/activate
```

2. Install the package:
```bash
pip install prompt-efficiency-suite
```

3. Verify the installation:
```bash
prompt-efficiency --version
```

### 2. Using Homebrew

1. Install Homebrew if you haven't already:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install the package:
```bash
brew install prompt-efficiency-suite
```

3. Verify the installation:
```bash
prompt-efficiency --version
```

### 3. Using Docker

1. Install Docker Desktop for Mac:
   - Download from [Docker's website](https://www.docker.com/products/docker-desktop)
   - Install and start Docker Desktop

2. Pull the image:
```bash
docker pull prompt-efficiency-suite:latest
```

3. Run the container:
```bash
docker run -it --rm prompt-efficiency-suite:latest
```

## IDE Integration

### VS Code Extension

1. Open VS Code
2. Press `Cmd+Shift+X` to open Extensions
3. Search for "Prompt Efficiency Suite"
4. Click Install
5. Reload VS Code

### JetBrains Plugin

1. Open your JetBrains IDE
2. Go to Preferences → Plugins
3. Search for "Prompt Efficiency Suite"
4. Click Install
5. Restart your IDE

## Configuration

1. Create configuration directory:
```bash
mkdir -p ~/.prompt-efficiency
```

2. Create configuration file:
```bash
touch ~/.prompt-efficiency/config.yaml
```

3. Add your configuration:
```yaml
api_key: your_api_key_here
model: gpt-4
default_settings:
  temperature: 0.7
  max_tokens: 2000
```

## Verification

Run the verification script:
```bash
prompt-efficiency verify
```

## Troubleshooting

### Common Issues

1. **Python Version Issues**
   ```bash
   # Check Python version
   python3 --version

   # If version is too old, install newer version
   brew install python@3.9
   ```

2. **Permission Issues**
   ```bash
   # Fix permissions
   sudo chown -R $(whoami) ~/.prompt-efficiency
   ```

3. **Dependency Issues**
   ```bash
   # Reinstall dependencies
   pip install --upgrade -r requirements.txt
   ```

4. **VS Code Extension Issues**
   - Uninstall and reinstall the extension
   - Check VS Code logs: `Cmd+Shift+P` → "Developer: Open Logs"

5. **JetBrains Plugin Issues**
   - Clear IDE cache: `File` → `Invalidate Caches`
   - Reinstall the plugin

### Getting Help

- Check the [Troubleshooting Guide](../troubleshooting/common-issues.md)
- Join our [GitHub Discussions](https://github.com/yourusername/prompt-efficiency-suite/discussions)
- Contact [support@prompt.com](mailto:support@prompt.com)

## Next Steps

1. [Learn Basic Concepts](concepts.md)
2. [Try the Quick Start Guide](quickstart.md)
3. [Explore Features](../features/analysis.md)
4. [Configure Settings](../configuration/global.md)
