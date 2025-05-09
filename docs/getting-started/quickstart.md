# Quick Start Guide

This guide will help you get started with the Prompt Efficiency Suite in minutes.

## Installation

1. Install the package:
```bash
pip install prompt-efficiency-suite
```

2. Verify the installation:
```bash
prompt-efficiency --version
```

## Your First Prompt Analysis

1. Open your terminal and run:
```bash
prompt-efficiency analyze "Write a function to calculate the Fibonacci sequence"
```

2. You'll see a detailed analysis of your prompt:
```
Quality Metrics:
- Clarity: 0.85
- Completeness: 0.92
- Consistency: 0.88

Cost Estimate:
- Tokens: 150
- Estimated Cost: $0.003

Suggestions:
- Add input validation
- Specify output format
```

## Optimizing a Prompt

1. Run the optimization command:
```bash
prompt-efficiency optimize "Write a function to calculate the Fibonacci sequence" --target-ratio 0.8
```

2. The optimized prompt will be displayed:
```
Original: Write a function to calculate the Fibonacci sequence
Optimized: Create a function that computes Fibonacci numbers with input validation and clear output format
```

## Using the Web UI

1. Start the web interface:
```bash
prompt-efficiency web
```

2. Open your browser and go to `http://localhost:3000`

3. You'll see the dashboard with:
   - Prompt analysis tools
   - Cost tracking
   - Performance metrics
   - Repository scanning

## Using VS Code Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Prompt Efficiency Suite"
4. Click Install
5. Open any file with prompts
6. Use the command palette (Ctrl+Shift+P) and type "Prompt Efficiency"

## Using JetBrains Plugin

1. Open your JetBrains IDE
2. Go to Settings/Preferences → Plugins
3. Search for "Prompt Efficiency Suite"
4. Click Install
5. Restart your IDE
6. Use the tool window to access features

## Next Steps

1. [Learn Basic Concepts](concepts.md)
2. [Explore Features](../features/analysis.md)
3. [Configure Settings](../configuration/global.md)
4. [Try Examples](../examples/basic.md)

## Common Tasks

### Analyzing Multiple Prompts

```bash
prompt-efficiency analyze-batch prompts.txt
```

### Scanning a Repository

```bash
prompt-efficiency scan /path/to/repo
```

### Managing Budget

```bash
prompt-efficiency budget --set 1000
```

### Using Macros

```bash
prompt-efficiency macro create summary "Summarize: {text}"
prompt-efficiency macro apply summary "Your text here"
```

## Need Help?

- Check the [Troubleshooting Guide](../troubleshooting/common-issues.md)
- Join our [GitHub Discussions](https://github.com/yourusername/prompt-efficiency-suite/discussions)
- Contact [support@prompt.com](mailto:support@prompt.com) 