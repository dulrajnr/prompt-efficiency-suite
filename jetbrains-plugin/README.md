# Prompt Efficiency Plugin for JetBrains IDEs

A powerful plugin that helps developers analyze, optimize, and manage prompts for large language models directly from their JetBrains IDE.

## Features

### Prompt Analysis
- Analyze prompt clarity, structure, and complexity
- Get detailed feedback on prompt effectiveness
- Identify potential improvements
- Score prompts on multiple dimensions

### Prompt Optimization
- Automatically optimize prompts for better results
- Get suggestions for clarity and structure improvements
- Maintain prompt intent while enhancing effectiveness
- Apply best practices automatically

### Cost Estimation
- Estimate token usage and costs
- Support for multiple currencies
- Real-time cost calculation
- Cost optimization suggestions

### Repository Scanning
- Scan entire codebase for prompts
- Identify and analyze all prompts in use
- Get repository-wide insights
- Track prompt usage patterns

### Prompt Translation
- Translate prompts between languages
- Maintain prompt structure and intent
- Support for multiple target languages
- Preserve technical terminology

## Installation

1. Open your JetBrains IDE
2. Go to Settings/Preferences
3. Select Plugins
4. Click on Marketplace
5. Search for "Prompt Efficiency"
6. Click Install
7. Restart your IDE

## Configuration

### API Settings
1. Open Settings/Preferences
2. Navigate to Tools > Prompt Efficiency
3. Enter your API key
4. Set your server URL (default: http://localhost:8000)
5. Choose your default model
6. Select your preferred currency

### Connection Settings
- Enable/disable automatic connection checking
- Set connection check interval
- Configure retry behavior
- Set timeout values

## Usage

### Tool Window
- Open the Prompt Efficiency tool window (View > Tool Windows > Prompt Efficiency)
- Use the toolbar for quick access to features
- View results in the integrated table
- Monitor connection status

### Keyboard Shortcuts
- Analyze Prompt: `Ctrl+Alt+A` (Windows/Linux) or `Cmd+Alt+A` (macOS)
- Optimize Prompt: `Ctrl+Alt+O` (Windows/Linux) or `Cmd+Alt+O` (macOS)
- Estimate Cost: `Ctrl+Alt+E` (Windows/Linux) or `Cmd+Alt+E` (macOS)
- Scan Repository: `Ctrl+Alt+S` (Windows/Linux) or `Cmd+Alt+S` (macOS)
- Translate Prompt: `Ctrl+Alt+T` (Windows/Linux) or `Cmd+Alt+T` (macOS)
- Open Settings: `Ctrl+Alt+,` (Windows/Linux) or `Cmd+Alt+,` (macOS)

### Context Menu
- Right-click on selected text to access prompt features
- Choose from available actions
- View results in the tool window

## API Integration

### Endpoints
- `/analyze` - Analyze prompt effectiveness
- `/optimize` - Optimize prompt structure
- `/estimate` - Calculate prompt costs
- `/scan` - Scan repository for prompts
- `/translate` - Translate prompts

### Authentication
- Bearer token authentication
- API key required
- Secure transmission

### Rate Limiting
- Default: 100 requests per minute
- Configurable limits
- Automatic retry with backoff

## Development

### Building from Source
1. Clone the repository
2. Open in IntelliJ IDEA
3. Install Gradle
4. Run `./gradlew build`

### Running Tests
```bash
./gradlew test
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

### Issues
- Report bugs on GitHub Issues
- Include detailed reproduction steps
- Attach relevant logs

### Feature Requests
- Submit via GitHub Issues
- Describe the feature
- Explain the use case

### Documentation
- Check the [Wiki](https://github.com/your-repo/wiki)
- Read the [API Documentation](https://github.com/your-repo/api-docs)
- Join the [Discord](https://discord.gg/your-server)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- JetBrains for the excellent IDE platform
- The open-source community for inspiration and support
- All contributors who have helped shape this project
