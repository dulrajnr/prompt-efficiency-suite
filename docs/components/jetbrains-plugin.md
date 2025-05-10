# JetBrains Plugin

The Prompt Efficiency Suite JetBrains plugin provides seamless integration with JetBrains IDEs for prompt optimization and management.

## Installation

1. Open JetBrains IDE
2. Go to Settings/Preferences
3. Navigate to Plugins
4. Search for "Prompt Efficiency Suite"
5. Click Install
6. Restart IDE

## Features

### 1. Prompt Analysis

#### In-Editor Analysis
- Right-click on selected text
- Choose "Prompt Efficiency: Analyze"
- View results in tool window

#### Analysis Panel
- Shows quality metrics
- Displays improvement suggestions
- Provides pattern recognition
- Command: `Ctrl+Alt+A` (Windows/Linux) or `Cmd+Alt+A` (macOS)

### 2. Prompt Optimization

#### Quick Optimization
- Select text in editor
- Right-click and choose "Prompt Efficiency: Optimize"
- View optimized version in diff view

#### Optimization Settings
```json
{
    "optimization": {
        "method": "compress",
        "target_ratio": 0.8,
        "preserve_terms": ["API", "endpoint"],
        "min_quality": 0.7
    }
}
```

### 3. Cost Estimation

#### In-Editor Estimation
- Select text in editor
- Right-click and choose "Prompt Efficiency: Estimate Cost"
- View cost breakdown in tool window

#### Cost Settings
```json
{
    "cost": {
        "default_model": "gpt-4",
        "default_currency": "USD",
        "show_breakdown": true
    }
}
```

### 4. Repository Scanning

#### Scan Project
- Right-click on project
- Choose "Prompt Efficiency: Scan Project"
- View results in tool window

#### Scan Settings
```json
{
    "scanning": {
        "include_analysis": true,
        "include_suggestions": true,
        "file_patterns": ["*.py", "*.js"],
        "exclude_patterns": ["tests/*", "docs/*"]
    }
}
```

### 5. Model Translation

#### Translate Prompt
- Select text in editor
- Right-click and choose "Prompt Efficiency: Translate"
- Choose target model
- View translation in diff view

#### Translation Settings
```json
{
    "translation": {
        "preserve_style": true,
        "optimize_tokens": true,
        "default_target": "claude-2"
    }
}
```

### 6. Pattern Management

#### Pattern Recognition
- Automatically detects common patterns
- Suggests pattern improvements
- Provides pattern documentation

#### Pattern Settings
```json
{
    "patterns": {
        "enabled": true,
        "auto_detect": true,
        "suggest_improvements": true
    }
}
```

### 7. Cost Analytics

#### Usage Tracking
- Tracks token usage
- Monitors costs
- Provides usage reports

#### Analytics Settings
```json
{
    "analytics": {
        "track_usage": true,
        "show_notifications": true,
        "budget_alerts": true
    }
}
```

## UI Components

### 1. Tool Window

#### Analysis Panel
- Quality metrics
- Improvement suggestions
- Pattern recognition results

#### Cost Panel
- Token usage
- Cost estimates
- Budget tracking

#### Scan Panel
- Repository scan results
- Optimization opportunities
- Cost reports

### 2. Editor Integration

#### In-Editor Actions
- Right-click menu
- Quick fixes
- Intention actions

#### Status Bar
- Current model
- Token count
- API connection status

### 3. Settings Dialog

#### General Settings
- API configuration
- Default models
- Output formats

#### Feature Settings
- Analysis options
- Optimization settings
- Cost tracking

## Configuration

### 1. API Settings
```json
{
    "api": {
        "key": "your-api-key",
        "url": "http://localhost:8000",
        "timeout": 30
    }
}
```

### 2. Editor Settings
```json
{
    "editor": {
        "auto_analyze": true,
        "show_suggestions": true,
        "highlight_patterns": true
    }
}
```

### 3. Cost Settings
```json
{
    "cost": {
        "track_usage": true,
        "show_notifications": true,
        "budget_alerts": true
    }
}
```

## Keyboard Shortcuts

### Default Shortcuts
- `Ctrl+Alt+A` (Windows/Linux) or `Cmd+Alt+A` (macOS): Analyze
- `Ctrl+Alt+O` (Windows/Linux) or `Cmd+Alt+O` (macOS): Optimize
- `Ctrl+Alt+C` (Windows/Linux) or `Cmd+Alt+C` (macOS): Estimate Cost
- `Ctrl+Alt+S` (Windows/Linux) or `Cmd+Alt+S` (macOS): Scan Project
- `Ctrl+Alt+T` (Windows/Linux) or `Cmd+Alt+T` (macOS): Translate

### Custom Shortcuts
1. Open Settings/Preferences
2. Navigate to Keymap
3. Search for "Prompt Efficiency"
4. Modify shortcuts as needed

## Integration Features

### 1. Version Control
- Git integration
- Commit message analysis
- Branch-specific settings

### 2. Build Tools
- Gradle integration
- Maven integration
- Build script analysis

### 3. Testing
- Test case analysis
- Test coverage integration
- Performance testing

## Best Practices

### 1. Editor Usage
- Use keyboard shortcuts
- Enable auto-analysis
- Review suggestions regularly
- Keep settings updated

### 2. Cost Management
- Monitor token usage
- Set budget alerts
- Review cost reports
- Optimize frequently used prompts

### 3. Pattern Usage
- Follow pattern guidelines
- Use pattern templates
- Review pattern suggestions
- Document custom patterns

## Troubleshooting

### 1. Common Issues

#### API Connection
- Verify API key
- Check server URL
- Review network settings

#### Analysis Issues
- Check prompt format
- Verify model compatibility
- Review error messages

#### Performance Issues
- Clear caches
- Update settings
- Check system resources

### 2. Error Messages
- `API Connection Failed`: Check API settings
- `Invalid Prompt`: Review prompt format
- `Model Not Available`: Verify model compatibility
- `Configuration Error`: Check settings format

## Support

### 1. Documentation
- [User Guide](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Examples](examples/)

### 2. Support Channels
- Email: support@prompt.com
- GitHub Issues: https://github.com/yourusername/prompt-efficiency-suite/issues
- Documentation: https://docs.prompt.com

### 3. Community
- Stack Overflow: https://stackoverflow.com/questions/tagged/prompt-efficiency
- Discord: https://discord.gg/prompt-efficiency
- Twitter: @prompt_efficiency

## Development

### 1. Building from Source
1. Clone the repository
2. Open in IntelliJ IDEA
3. Build the project
4. Run the plugin

### 2. Running Tests
```bash
./gradlew test
```

### 3. Debugging
1. Run in debug mode
2. Use the Debug Console
3. Set breakpoints
4. Monitor variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- JetBrains team for the excellent plugin API
- The open-source community for inspiration and support
- All contributors who have helped shape this project
