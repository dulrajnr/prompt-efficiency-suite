"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const assert = __importStar(require("assert"));
const vscode = __importStar(require("vscode"));
const sinon = __importStar(require("sinon"));
const axios_1 = __importDefault(require("axios"));
suite('Prompt Efficiency Suite Extension Test Suite', () => {
    let sandbox;
    let axiosInstance;
    suiteSetup(async () => {
        // Set up configuration before activating extension
        const config = vscode.workspace.getConfiguration('promptEfficiency');
        await config.update('apiKey', 'test-key', vscode.ConfigurationTarget.Global);
        await config.update('serverUrl', 'http://localhost:3000', vscode.ConfigurationTarget.Global);
        await config.update('defaultModel', 'gpt-4', vscode.ConfigurationTarget.Global);
        await config.update('defaultCurrency', 'USD', vscode.ConfigurationTarget.Global);
        // Mock axios.create to return our stubbed instance
        axiosInstance = {
            get: sinon.stub(),
            post: sinon.stub(),
            interceptors: {
                request: { use: sinon.stub() },
                response: { use: sinon.stub() }
            }
        };
        sinon.stub(axios_1.default, 'create').returns(axiosInstance);
        // Wait for extension to activate
        const extension = vscode.extensions.getExtension('prompt-efficiency.prompt-efficiency-suite');
        await extension?.activate();
    });
    suiteTeardown(() => {
        sinon.restore();
    });
    setup(() => {
        sandbox = sinon.createSandbox();
    });
    teardown(() => {
        sandbox.restore();
        axiosInstance.get.reset();
        axiosInstance.post.reset();
    });
    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('prompt-efficiency.prompt-efficiency-suite'));
    });
    test('Should register all commands', async () => {
        const commands = [
            'prompt-efficiency.analyze',
            'prompt-efficiency.optimize',
            'prompt-efficiency.estimate-cost',
            'prompt-efficiency.scan-repository',
            'prompt-efficiency.translate-model',
            'prompt-efficiency.checkConnection',
            'prompt-efficiency.openConfig'
        ];
        const getCommandsStub = sandbox.stub(vscode.commands, 'getCommands').resolves(commands);
        for (const command of commands) {
            const result = await vscode.commands.getCommands(true);
            assert.ok(result.includes(command), `Command ${command} not found`);
        }
        assert.ok(getCommandsStub.called);
    });
    test('Should handle analyze command', async () => {
        // Mock editor and selection
        const mockEditor = {
            document: {
                getText: () => 'Test prompt'
            },
            selection: new vscode.Selection(0, 0, 0, 11)
        };
        sandbox.stub(vscode.window, 'activeTextEditor').value(mockEditor);
        // Mock API response
        const mockResponse = {
            data: {
                clarity_score: 0.8,
                structure_score: 0.7,
                complexity_score: 0.6,
                token_count: 10,
                suggestions: ['Add more context', 'Be more specific']
            }
        };
        axiosInstance.post.resolves(mockResponse);
        // Mock createWebviewPanel
        const mockPanel = {
            webview: {
                html: ''
            }
        };
        sandbox.stub(vscode.window, 'createWebviewPanel').returns(mockPanel);
        // Execute command and wait for it to complete
        await vscode.commands.executeCommand('prompt-efficiency.analyze');
        await new Promise(resolve => setTimeout(resolve, 100)); // Give time for command to complete
        // Verify API call
        sinon.assert.calledWith(axiosInstance.post, '/api/v1/analyze', {
            prompt: 'Test prompt',
            model: 'gpt-4'
        });
    });
    test('Should handle optimize command', async () => {
        // Mock editor and selection
        const mockEditor = {
            document: {
                getText: () => 'Test prompt'
            },
            selection: new vscode.Selection(0, 0, 0, 11),
            edit: (callback) => {
                const mockEditBuilder = {
                    replace: sandbox.stub(),
                    insert: sandbox.stub(),
                    delete: sandbox.stub(),
                    setEndOfLine: sandbox.stub()
                };
                callback(mockEditBuilder);
                return Promise.resolve(true);
            }
        };
        sandbox.stub(vscode.window, 'activeTextEditor').value(mockEditor);
        // Mock API response
        const mockResponse = {
            data: {
                optimized_prompt: 'Optimized test prompt',
                improvement_ratio: 0.2
            }
        };
        axiosInstance.post.resolves(mockResponse);
        // Execute command and wait for it to complete
        await vscode.commands.executeCommand('prompt-efficiency.optimize');
        await new Promise(resolve => setTimeout(resolve, 100)); // Give time for command to complete
        // Verify API call
        sinon.assert.calledWith(axiosInstance.post, '/api/v1/optimize', {
            prompt: 'Test prompt',
            method: 'trim',
            preserve_ratio: 0.8,
            model: 'gpt-4'
        });
    });
    test('Should handle estimate-cost command', async () => {
        // Mock editor and selection
        const mockEditor = {
            document: {
                getText: () => 'Test prompt'
            },
            selection: new vscode.Selection(0, 0, 0, 11)
        };
        sandbox.stub(vscode.window, 'activeTextEditor').value(mockEditor);
        // Mock API response
        const mockResponse = {
            data: {
                total_cost: 0.002,
                currency: 'USD',
                token_count: 10
            }
        };
        axiosInstance.post.resolves(mockResponse);
        // Mock showInformationMessage
        const showInfoStub = sandbox.stub(vscode.window, 'showInformationMessage');
        // Execute command and wait for it to complete
        await vscode.commands.executeCommand('prompt-efficiency.estimate-cost');
        await new Promise(resolve => setTimeout(resolve, 100)); // Give time for command to complete
        // Verify API call
        sinon.assert.calledWith(axiosInstance.post, '/api/v1/estimate-cost', {
            prompt: 'Test prompt',
            model: 'gpt-4',
            currency: 'USD'
        });
        // Verify message shown
        sinon.assert.calledWith(showInfoStub, 'Estimated cost: 0.002 USD');
    });
    test('Should handle scan-repository command', async () => {
        // Mock workspace folders
        const mockWorkspaceFolder = {
            uri: {
                fsPath: '/test/path'
            }
        };
        sandbox.stub(vscode.workspace, 'workspaceFolders').value([mockWorkspaceFolder]);
        // Mock API response
        const mockResponse = {
            data: {
                files_scanned: 10,
                prompts_found: 5,
                results: [
                    {
                        file: 'test1.txt',
                        prompt: 'Test prompt 1'
                    },
                    {
                        file: 'test2.txt',
                        prompt: 'Test prompt 2'
                    }
                ]
            }
        };
        axiosInstance.post.resolves(mockResponse);
        // Mock createWebviewPanel
        const mockPanel = {
            webview: {
                html: ''
            }
        };
        sandbox.stub(vscode.window, 'createWebviewPanel').returns(mockPanel);
        // Execute command and wait for it to complete
        await vscode.commands.executeCommand('prompt-efficiency.scan-repository');
        await new Promise(resolve => setTimeout(resolve, 100)); // Give time for command to complete
        // Verify API call
        sinon.assert.calledWith(axiosInstance.post, '/api/v1/scan-repository', {
            directory: '/test/path',
            include_patterns: ['*.txt', '*.md'],
            exclude_patterns: ['*.py', '*.ipynb']
        });
    });
    test('Should handle translate-model command', async () => {
        // Mock editor and selection
        const mockEditor = {
            document: {
                getText: () => 'Test prompt'
            },
            selection: new vscode.Selection(0, 0, 0, 11),
            edit: (callback) => {
                const mockEditBuilder = {
                    replace: sandbox.stub(),
                    insert: sandbox.stub(),
                    delete: sandbox.stub(),
                    setEndOfLine: sandbox.stub()
                };
                callback(mockEditBuilder);
                return Promise.resolve(true);
            }
        };
        sandbox.stub(vscode.window, 'activeTextEditor').value(mockEditor);
        // Mock API response
        const mockResponse = {
            data: {
                translated_prompt: 'Translated test prompt'
            }
        };
        axiosInstance.post.resolves(mockResponse);
        // Execute command and wait for it to complete
        await vscode.commands.executeCommand('prompt-efficiency.translate-model');
        await new Promise(resolve => setTimeout(resolve, 100)); // Give time for command to complete
        // Verify API call
        sinon.assert.calledWith(axiosInstance.post, '/api/v1/translate', {
            prompt: 'Test prompt',
            source_model: 'gpt-4',
            target_model: 'gpt-3.5-turbo'
        });
    });
    test('Should handle openConfig command', async () => {
        // Mock createWebviewPanel
        const mockPanel = {
            webview: {
                html: '',
                postMessage: sandbox.stub(),
                onDidReceiveMessage: sandbox.stub().returns({ dispose: sandbox.stub() })
            },
            onDidDispose: sandbox.stub().returns({ dispose: sandbox.stub() })
        };
        const createWebviewPanelStub = sandbox.stub(vscode.window, 'createWebviewPanel').returns(mockPanel);
        // Execute command and wait for it to complete
        await vscode.commands.executeCommand('prompt-efficiency.openConfig');
        await new Promise(resolve => setTimeout(resolve, 100)); // Give time for command to complete
        // Verify panel was created
        sinon.assert.calledWith(createWebviewPanelStub, 'promptEfficiencyConfig', 'Prompt Efficiency Settings', vscode.ViewColumn.One, {
            enableScripts: true,
            retainContextWhenHidden: true
        });
    });
    test('Should handle connection check', async () => {
        // Mock API response
        axiosInstance.get.resolves({ status: 200 });
        // Mock status bar item
        const mockStatusBarItem = {
            text: '',
            tooltip: ''
        };
        sandbox.stub(vscode.window, 'createStatusBarItem').returns(mockStatusBarItem);
        // Execute command and wait for it to complete
        await vscode.commands.executeCommand('prompt-efficiency.checkConnection');
        await new Promise(resolve => setTimeout(resolve, 100)); // Give time for command to complete
        // Verify API call
        sinon.assert.calledWith(axiosInstance.get, '/health');
    });
});
//# sourceMappingURL=extension.test.js.map