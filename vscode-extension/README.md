# Prompt Efficiency Suite VS Code Extension

A powerful VS Code extension that helps developers optimize and manage their AI prompts efficiently.

## Features

### 1. Prompt Analysis
- Analyze prompts for quality and effectiveness
- Get detailed metrics and suggestions
- Measure complexity and readability
- Command: `prompt-efficiency.analyze`

### 2. Prompt Optimization
- Automatically optimize prompts for efficiency
- Reduce token count while maintaining quality
- Get detailed improvement suggestions
- Command: `prompt-efficiency.optimize`

### 3. Cost Estimation
- Estimate costs for different models
- Support for multiple currencies
- Detailed token breakdown
- Command: `prompt-efficiency.estimate-cost`

### 4. Repository Scanning
- Scan entire repositories for prompts
- Identify optimization opportunities
- Generate cost reports
- Command: `prompt-efficiency.scan-repository`

### 5. Model Translation
- Translate prompts between models
- Maintain prompt structure and intent
- Support for multiple models
- Command: `prompt-efficiency.translate-model`

### 6. Configuration Management
- Easy access to settings
- Customize extension behavior
- Manage API connections
- Command: `prompt-efficiency.openConfig`

## Installation

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Prompt Efficiency Suite"
4. Click Install
5. Reload VS Code

## Configuration

### API Settings
1. Open Command Palette (Ctrl+Shift+P)
2. Type "Prompt Efficiency: Open Config"
3. Configure the following settings:
   - API Key
   - Server URL
   - Default Model
   - Default Currency
   - Timeout Settings
   - Max Tokens

### Extension Settings
```json
{
    "promptEfficiency.apiKey": "your-api-key",
    "promptEfficiency.serverUrl": "http://localhost:8000",
    "promptEfficiency.defaultModel": "gpt-4",
    "promptEfficiency.defaultCurrency": "USD",
    "promptEfficiency.timeout": 30000,
    "promptEfficiency.maxTokens": 4000,
    "promptEfficiency.autoAnalyze": true,
    "promptEfficiency.showSuggestions": true
}
```

## Usage

### Analyzing Prompts
1. Select text in your editor
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
3. Type "Prompt Efficiency: Analyze"
4. View analysis results in the output panel

### Optimizing Prompts
1. Select text in your editor
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
3. Type "Prompt Efficiency: Optimize"
4. Review optimized version and improvements

### Estimating Costs
1. Select text in your editor
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
3. Type "Prompt Efficiency: Estimate Cost"
4. View cost breakdown by model

### Scanning Repository
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. Type "Prompt Efficiency: Scan Repository"
3. Select repository folder
4. Review results and suggestions

### Translating Prompts
1. Select text in your editor
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
3. Type "Prompt Efficiency: Translate Model"
4. Choose target model
5. Review translation

### Managing Configuration
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. Type "Prompt Efficiency: Open Config"
3. Modify settings as needed
4. Save changes

## UI Components

### Output Panel
- Displays analysis results
- Shows optimization suggestions
- Presents cost estimates
- Lists repository scan results

### Status Bar
- Shows current model
- Displays token count
- Indicates API connection status
- Shows current currency

### Webview Panels
- Configuration panel
- Analysis results panel
- Optimization suggestions panel
- Cost estimation panel

## Error Handling

### Common Issues
1. API Connection Issues
   - Verify API key and server URL
   - Check network connection
   - Review timeout settings

2. Analysis Failures
   - Check prompt length
   - Verify model compatibility
   - Review error messages

3. Configuration Issues
   - Verify settings format
   - Check required fields
   - Review validation errors

### Error Messages
- `API Connection Failed`: Check API settings and network
- `Invalid Prompt`: Review prompt format and length
- `Model Not Available`: Verify model compatibility
- `Configuration Error`: Check settings format

## Best Practices

### Writing Efficient Prompts
- Be specific and concise
- Use clear instructions
- Structure prompts logically
- Include examples when helpful

### Cost Optimization
- Monitor token usage
- Use appropriate models
- Optimize frequently used prompts
- Review repository-wide usage

### Extension Usage
- Use keyboard shortcuts
- Enable auto-analysis
- Review suggestions regularly
- Keep configuration updated

## Development

### Building from Source
1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Build the extension:
   ```bash
   npm run compile
   ```

### Running Tests
```bash
npm test
```

### Debugging
1. Open the project in VS Code
2. Press F5 to start debugging
3. Use the Debug Console for output
4. Set breakpoints in the code

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Support

### Getting Help
- Check the [GitHub repository](https://github.com/your-repo)
- Submit issues and feature requests
- Contact support at support@prompt.com

### Documentation
- [User Guide](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Contributing Guide](CONTRIBUTING.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- VS Code team for the excellent extension API
- The open-source community for inspiration and support
- All contributors who have helped shape this project 