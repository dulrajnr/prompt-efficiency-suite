import * as vscode from 'vscode';
import axios from 'axios';

let statusBarItem: vscode.StatusBarItem;
let apiClient: any;
let connectionCheckInterval: NodeJS.Timeout | undefined;
let configPanel: vscode.WebviewPanel | undefined;

export function activate(context: vscode.ExtensionContext) {
    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'prompt-efficiency.checkConnection';
    context.subscriptions.push(statusBarItem);

    // Initialize API client
    initializeApiClient();

    // Register check connection command
    const checkConnectionDisposable = vscode.commands.registerCommand('prompt-efficiency.checkConnection', async () => {
        try {
            await apiClient.get('/health');
            statusBarItem.text = '$(check) Prompt Efficiency';
            statusBarItem.tooltip = 'Connected to Prompt Efficiency Suite';
        } catch (error) {
            statusBarItem.text = '$(error) Prompt Efficiency';
            statusBarItem.tooltip = 'Failed to connect to Prompt Efficiency Suite';
        }
    });

    // Register configuration panel command
    const configPanelDisposable = vscode.commands.registerCommand('prompt-efficiency.openConfig', () => {
        if (configPanel) {
            configPanel.reveal(vscode.ViewColumn.One);
            return;
        }

        configPanel = vscode.window.createWebviewPanel(
            'promptEfficiencyConfig',
            'Prompt Efficiency Settings',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        configPanel.webview.html = getConfigPanelHtml();

        configPanel.webview.onDidReceiveMessage(
            async message => {
                switch (message.command) {
                    case 'saveConfig': {
                        const config = vscode.workspace.getConfiguration('promptEfficiency');
                        await config.update('apiKey', message.apiKey, vscode.ConfigurationTarget.Global);
                        await config.update('serverUrl', message.serverUrl, vscode.ConfigurationTarget.Global);
                        await config.update('defaultModel', message.model, vscode.ConfigurationTarget.Global);
                        break;
                    }
                    case 'getConfig': {
                        const config = vscode.workspace.getConfiguration('promptEfficiency');
                        if (configPanel) {
                            configPanel.webview.postMessage({
                                command: 'config',
                                apiKey: config.get('apiKey'),
                                serverUrl: config.get('serverUrl'),
                                model: config.get('defaultModel')
                            });
                        }
                        break;
                    }
                    case 'testConnection':
                        try {
                            await apiClient.get('/health');
                            configPanel?.webview.postMessage({ command: 'connectionStatus', status: 'success' });
                        } catch (error) {
                            configPanel?.webview.postMessage({ command: 'connectionStatus', status: 'error' });
                        }
                        break;
                }
            },
            undefined,
            context.subscriptions
        );

        configPanel.onDidDispose(
            () => {
                configPanel = undefined;
            },
            null,
            context.subscriptions
        );
    });

    // Register analyze command
    const analyzeDisposable = vscode.commands.registerCommand('prompt-efficiency.analyze', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.selection;
        const text = editor.document.getText(selection);

        try {
            const config = vscode.workspace.getConfiguration('promptEfficiency');
            const response = await apiClient.post('/api/v1/analyze', {
                prompt: text,
                model: config.get('defaultModel')
            });
            const analysis = response.data;

            // Create and show analysis results
            const panel = vscode.window.createWebviewPanel(
                'promptAnalysis',
                'Prompt Analysis Results',
                vscode.ViewColumn.Beside,
                {}
            );

            panel.webview.html = getAnalysisHtml(analysis);
        } catch (error) {
            vscode.window.showErrorMessage('Failed to analyze prompt');
        }
    });

    // Register optimize command
    const optimizeDisposable = vscode.commands.registerCommand('prompt-efficiency.optimize', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.selection;
        const text = editor.document.getText(selection);

        try {
            const config = vscode.workspace.getConfiguration('promptEfficiency');
            const response = await apiClient.post('/api/v1/optimize', {
                prompt: text,
                method: 'trim',
                preserve_ratio: 0.8,
                model: config.get('defaultModel')
            });

            const optimized = response.data;
            editor.edit(editBuilder => {
                editBuilder.replace(selection, optimized.optimized_prompt);
            });
        } catch (error) {
            vscode.window.showErrorMessage('Failed to optimize prompt');
        }
    });

    // Register estimate-cost command
    const estimateCostDisposable = vscode.commands.registerCommand('prompt-efficiency.estimate-cost', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.selection;
        const text = editor.document.getText(selection);

        try {
            const config = vscode.workspace.getConfiguration('promptEfficiency');
            const response = await apiClient.post('/api/v1/estimate-cost', {
                prompt: text,
                model: config.get('defaultModel'),
                currency: config.get('defaultCurrency')
            });

            const cost = response.data;
            vscode.window.showInformationMessage(
                `Estimated cost: ${cost.total_cost} ${cost.currency}`
            );
        } catch (error) {
            vscode.window.showErrorMessage('Failed to estimate cost');
        }
    });

    // Register scan-repository command
    const scanRepositoryDisposable = vscode.commands.registerCommand('prompt-efficiency.scan-repository', async () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder open');
            return;
        }

        try {
            const response = await apiClient.post('/api/v1/scan-repository', {
                directory: workspaceFolders[0].uri.fsPath,
                include_patterns: ['*.txt', '*.md'],
                exclude_patterns: ['*.py', '*.ipynb']
            });

            const results = response.data;
            const panel = vscode.window.createWebviewPanel(
                'repositoryScan',
                'Repository Scan Results',
                vscode.ViewColumn.Beside,
                {}
            );

            panel.webview.html = getScanResultsHtml(results);
        } catch (error) {
            vscode.window.showErrorMessage('Failed to scan repository');
        }
    });

    // Register translate-model command
    const translateModelDisposable = vscode.commands.registerCommand('prompt-efficiency.translate-model', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor');
            return;
        }

        const selection = editor.selection;
        const text = editor.document.getText(selection);

        try {
            const config = vscode.workspace.getConfiguration('promptEfficiency');
            const response = await apiClient.post('/api/v1/translate', {
                prompt: text,
                source_model: config.get('defaultModel'),
                target_model: 'gpt-3.5-turbo'
            });

            const translation = response.data;
            editor.edit(editBuilder => {
                editBuilder.replace(selection, translation.translated_prompt);
            });
        } catch (error) {
            vscode.window.showErrorMessage('Failed to translate prompt');
        }
    });

    // Add disposables to context
    context.subscriptions.push(
        checkConnectionDisposable,
        configPanelDisposable,
        analyzeDisposable,
        optimizeDisposable,
        estimateCostDisposable,
        scanRepositoryDisposable,
        translateModelDisposable
    );

    // Handle configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('promptEfficiency')) {
                initializeApiClient();
                setupConnectionCheck();
                if (configPanel) {
                    configPanel.webview.postMessage({ command: 'configChanged' });
                }
            }
        })
    );

    // Initial setup
    setupConnectionCheck();
}

function initializeApiClient() {
    const config = vscode.workspace.getConfiguration('promptEfficiency');
    const apiKey = config.get<string>('apiKey');
    const serverUrl = config.get<string>('serverUrl');

    apiClient = axios.create({
        baseURL: serverUrl,
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        }
    });
}

function setupConnectionCheck() {
    const config = vscode.workspace.getConfiguration('promptEfficiency');
    const autoCheck = config.get<boolean>('autoCheckConnection');
    const interval = config.get<number>('connectionCheckInterval');

    if (connectionCheckInterval) {
        clearInterval(connectionCheckInterval);
    }

    if (autoCheck) {
        connectionCheckInterval = setInterval(() => {
            vscode.commands.executeCommand('prompt-efficiency.checkConnection');
        }, interval);
    }
}

function getConfigPanelHtml(): string {
    const config = vscode.workspace.getConfiguration('promptEfficiency');
    const apiKey = config.get<string>('apiKey') || '';
    const serverUrl = config.get<string>('serverUrl') || 'http://localhost:8000';
    const defaultModel = config.get<string>('defaultModel') || 'gpt-4';
    const defaultCurrency = config.get<string>('defaultCurrency') || 'USD';
    const autoCheckConnection = config.get<boolean>('autoCheckConnection') ?? true;
    const connectionCheckInterval = config.get<number>('connectionCheckInterval') || 30000;

    return `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    padding: 20px;
                    font-family: var(--vscode-font-family);
                    color: var(--vscode-foreground);
                }
                .form-group {
                    margin-bottom: 15px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                }
                input[type="text"],
                input[type="number"],
                select {
                    width: 100%;
                    padding: 5px;
                    margin-bottom: 5px;
                    background: var(--vscode-input-background);
                    color: var(--vscode-input-foreground);
                    border: 1px solid var(--vscode-input-border);
                }
                .description {
                    font-size: 0.9em;
                    color: var(--vscode-descriptionForeground);
                    margin-bottom: 10px;
                }
                button {
                    padding: 5px 10px;
                    background: var(--vscode-button-background);
                    color: var(--vscode-button-foreground);
                    border: none;
                    cursor: pointer;
                }
                button:hover {
                    background: var(--vscode-button-hoverBackground);
                }
                .status {
                    margin-top: 10px;
                    padding: 10px;
                    border-radius: 3px;
                }
                .success {
                    background: var(--vscode-testing-iconPassed);
                    color: white;
                }
                .error {
                    background: var(--vscode-testing-iconFailed);
                    color: white;
                }
            </style>
        </head>
        <body>
            <div class="form-group">
                <label for="apiKey">API Key</label>
                <div class="description">Your API key for the Prompt Efficiency Suite</div>
                <input type="text" id="apiKey" value="${apiKey}" />
            </div>

            <div class="form-group">
                <label for="serverUrl">Server URL</label>
                <div class="description">The URL of your Prompt Efficiency Suite server</div>
                <input type="text" id="serverUrl" value="${serverUrl}" />
            </div>

            <div class="form-group">
                <label for="defaultModel">Default Model</label>
                <div class="description">The default model to use for analysis and optimization</div>
                <select id="defaultModel">
                    <option value="gpt-4" ${defaultModel === 'gpt-4' ? 'selected' : ''}>GPT-4</option>
                    <option value="gpt-3.5-turbo" ${defaultModel === 'gpt-3.5-turbo' ? 'selected' : ''}>GPT-3.5 Turbo</option>
                    <option value="claude-2" ${defaultModel === 'claude-2' ? 'selected' : ''}>Claude 2</option>
                    <option value="claude-instant" ${defaultModel === 'claude-instant' ? 'selected' : ''}>Claude Instant</option>
                </select>
            </div>

            <div class="form-group">
                <label for="defaultCurrency">Default Currency</label>
                <div class="description">The default currency for cost estimation</div>
                <select id="defaultCurrency">
                    <option value="USD" ${defaultCurrency === 'USD' ? 'selected' : ''}>USD</option>
                    <option value="EUR" ${defaultCurrency === 'EUR' ? 'selected' : ''}>EUR</option>
                    <option value="GBP" ${defaultCurrency === 'GBP' ? 'selected' : ''}>GBP</option>
                </select>
            </div>

            <div class="form-group">
                <label for="autoCheckConnection">Auto Check Connection</label>
                <div class="description">Automatically check API connection status</div>
                <input type="checkbox" id="autoCheckConnection" ${autoCheckConnection ? 'checked' : ''} />
            </div>

            <div class="form-group">
                <label for="connectionCheckInterval">Connection Check Interval (ms)</label>
                <div class="description">Interval in milliseconds to check API connection status</div>
                <input type="number" id="connectionCheckInterval" value="${connectionCheckInterval}" />
            </div>

            <button onclick="testConnection()">Test Connection</button>
            <div id="connectionStatus" class="status" style="display: none;"></div>

            <script>
                const vscode = acquireVsCodeApi();

                // Handle input changes
                document.querySelectorAll('input, select').forEach(element => {
                    element.addEventListener('change', () => {
                        const key = element.id;
                        let value = element.type === 'checkbox' ? element.checked : element.value;
                        if (element.type === 'number') {
                            value = parseInt(value);
                        }
                        vscode.postMessage({
                            command: 'updateConfig',
                            key: key,
                            value: value
                        });
                    });
                });

                // Handle connection status updates
                window.addEventListener('message', event => {
                    const message = event.data;
                    if (message.command === 'connectionStatus') {
                        const statusDiv = document.getElementById('connectionStatus');
                        statusDiv.style.display = 'block';
                        if (message.status === 'success') {
                            statusDiv.className = 'status success';
                            statusDiv.textContent = 'Connection successful!';
                        } else {
                            statusDiv.className = 'status error';
                            statusDiv.textContent = 'Connection failed. Please check your settings.';
                        }
                    }
                });

                function testConnection() {
                    vscode.postMessage({
                        command: 'testConnection'
                    });
                }
            </script>
        </body>
        </html>
    `;
}

function getAnalysisHtml(analysis: any): string {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { padding: 20px; font-family: Arial, sans-serif; }
                .metric { margin-bottom: 10px; }
                .score { font-weight: bold; }
                .suggestion { margin-top: 20px; }
            </style>
        </head>
        <body>
            <h2>Prompt Analysis Results</h2>
            <div class="metric">
                <h3>Clarity</h3>
                <p class="score">${analysis.clarity}</p>
            </div>
            <div class="metric">
                <h3>Structure</h3>
                <p class="score">${analysis.structure}</p>
            </div>
            <div class="metric">
                <h3>Complexity</h3>
                <p class="score">${analysis.complexity}</p>
            </div>
            <div class="suggestion">
                <h3>Suggestions</h3>
                <ul>
                    ${analysis.suggestions.map((s: string) => `<li>${s}</li>`).join('')}
                </ul>
            </div>
        </body>
        </html>
    `;
}

function getScanResultsHtml(results: any): string {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { padding: 20px; font-family: Arial, sans-serif; }
                .summary { margin-bottom: 20px; }
                .file { margin-bottom: 10px; }
                .prompt { margin-left: 20px; }
            </style>
        </head>
        <body>
            <h2>Repository Scan Results</h2>
            <div class="summary">
                <h3>Summary</h3>
                <p>Files Scanned: ${results.files_scanned}</p>
                <p>Prompts Found: ${results.prompts_found}</p>
            </div>
            <div class="results">
                <h3>Results</h3>
                ${results.results.map((result: any) => `
                    <div class="file">
                        <h4>${result.file}</h4>
                        <div class="prompt">
                            <p>${result.prompt}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        </body>
        </html>
    `;
}

export function deactivate() {
    if (statusBarItem) {
        statusBarItem.dispose();
    }
    if (connectionCheckInterval) {
        clearInterval(connectionCheckInterval);
    }
    if (configPanel) {
        configPanel.dispose();
    }
}
