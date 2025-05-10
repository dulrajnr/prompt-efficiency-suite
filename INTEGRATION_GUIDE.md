# Prompt Efficiency Suite Integration Guide

This guide demonstrates how to integrate the Prompt Efficiency Suite into every stage of your development lifecycle.

## 1. Local Development & Prototyping

### CLI Tools
```bash
# Install the suite
pip install prompt-efficiency-suite

# Basic prompt analysis
prompt-efficiency analyze "Your prompt here"

# Get optimization suggestions
prompt-efficiency suggest "Your prompt here"

# Trim prompts while preserving domain terms
prompt-efficiency trim --preserve-ratio 0.8 "Your prompt here"

# Optimize code-containing prompts
prompt-efficiency compress-code "Your prompt with code here"

# Bulk optimize multiple prompts
prompt-efficiency bulk-optimize prompts/*.txt
```

### Python SDK
```python
from prompt_efficiency_suite import (
    PromptAnalyzer,
    DomainAwareTrimmer,
    AdaptiveBudgeting,
    CodeAwareCompressor
)

# Initialize components
analyzer = PromptAnalyzer()
trimmer = DomainAwareTrimmer()
budget_tracker = AdaptiveBudgeting()
compressor = CodeAwareCompressor()

# Analyze a prompt
result = analyzer.analyze_prompt("Your prompt here")
print(f"Quality Score: {result.quality_score}")

# Trim while preserving domain terms
trimmed = trimmer.trim(
    text="Your prompt here",
    preserve_ratio=0.8,
    domain_terms=["specific", "technical", "terms"]
)

# Track budget usage
budget_tracker.track_usage(
    prompt="Your prompt here",
    model="gpt-4",
    tokens=150
)

# Compress code in prompts
compressed = compressor.compress(
    prompt="Your prompt with code here",
    language="python"
)
```

## 2. IDE & Editor Integration

### VS Code Extension
1. Install the "Prompt Efficiency" extension
2. Features:
   - Inline trimming suggestions
   - Token count display
   - Right-click menu for prompt operations
   - Real-time quality analysis

### JetBrains Plugin
1. Install from JetBrains Marketplace
2. Features:
   - Tool window for budget management
   - Dictionary management
   - Regex cleanup
   - Keyboard shortcuts for common operations

## 3. CI/CD & Pre-Merge Checks

### GitHub Actions
```yaml
name: Prompt Analysis

on: [pull_request]

jobs:
  analyze-prompts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install prompt-efficiency-suite
      - name: Analyze prompts
        run: |
          prompt-efficiency analyze "prompts/**/*.txt"
          prompt-efficiency check-budget "prompts/**/*.txt"
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Analyze Prompts') {
            steps {
                sh 'pip install prompt-efficiency-suite'
                sh 'prompt-efficiency analyze "prompts/**/*.txt"'
                sh 'prompt-efficiency check-budget "prompts/**/*.txt"'
            }
        }
    }
}
```

## 4. Runtime & Production Services

### REST API Integration
```python
import requests

# Initialize API client
API_BASE = "http://your-prompt-efficiency-service:8000"

# Analyze prompt
response = requests.post(
    f"{API_BASE}/analyze",
    json={"prompt": "Your prompt here"}
)
result = response.json()

# Trim prompt
response = requests.post(
    f"{API_BASE}/trim",
    json={
        "prompt": "Your prompt here",
        "preserve_ratio": 0.8
    }
)
trimmed = response.json()["trimmed_prompt"]

# Track usage
response = requests.post(
    f"{API_BASE}/track-usage",
    json={
        "prompt": "Your prompt here",
        "model": "gpt-4",
        "tokens": 150
    }
)
```

### Prometheus Metrics
```python
from prompt_efficiency_suite import AdaptiveBudgeting

budget_tracker = AdaptiveBudgeting()

# Expose metrics for Prometheus
budget_tracker.expose_metrics(
    port=9090,
    path="/metrics"
)
```

## 5. Bulk & Scheduled Tasks

### Nightly Optimization
```bash
# Create a cron job
0 0 * * * /usr/local/bin/prompt-efficiency bulk-optimize /path/to/prompts

# Or use the Python API
from prompt_efficiency_suite import BulkOptimizer

optimizer = BulkOptimizer()
optimizer.optimize_directory(
    directory="/path/to/prompts",
    output_dir="/path/to/optimized"
)
```

### Macro Management
```bash
# Install community macros
prompt-efficiency macro install community-patterns

# List available macros
prompt-efficiency macro list

# Apply macros to prompts
prompt-efficiency macro apply community-patterns prompts/*.txt
```

## 6. Dashboards & Reporting

### Grafana Integration
1. Install the Prompt Efficiency Suite Grafana plugin
2. Import pre-built dashboards:
   - Token Usage Overview
   - Budget Alerts
   - CI Pass Rates
   - Macro Savings

### Web UI
1. Deploy the Prompt Efficiency Suite web interface
2. Features:
   - Benchmark leaderboards
   - Dictionary health monitoring
   - Orchestration logs
   - Team performance metrics

## Best Practices

1. **Local Development**
   - Use the CLI for quick checks
   - Integrate the SDK into your development workflow
   - Leverage IDE plugins for real-time feedback

2. **CI/CD**
   - Run prompt analysis on every PR
   - Enforce budget constraints
   - Archive optimization reports

3. **Production**
   - Monitor token usage
   - Track budget adherence
   - Use adaptive optimization
   - Maintain prompt dictionaries

4. **Team Collaboration**
   - Share macro patterns
   - Maintain common dictionaries
   - Review optimization reports
   - Track team performance

## Support

For additional help:
- Documentation: [docs/](docs/)
- Issues: [GitHub Issues](https://github.com/prompt-efficiency/prompt-efficiency-suite/issues)
- Discussions: [GitHub Discussions](https://github.com/prompt-efficiency/prompt-efficiency-suite/discussions)
