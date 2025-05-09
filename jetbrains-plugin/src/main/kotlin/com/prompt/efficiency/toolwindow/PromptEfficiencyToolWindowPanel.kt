package com.prompt.efficiency.toolwindow

import com.intellij.openapi.editor.Editor
import com.intellij.openapi.editor.SelectionModel
import com.intellij.openapi.project.Project
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.table.JBTable
import com.prompt.efficiency.api.PromptEfficiencyApiClient
import com.prompt.efficiency.settings.PromptEfficiencySettings
import okhttp3.*
import org.json.JSONObject
import java.awt.BorderLayout
import java.awt.Dimension
import java.io.IOException
import javax.swing.*
import javax.swing.table.DefaultTableModel
import java.util.concurrent.TimeUnit

class PromptEfficiencyToolWindowPanel(private val project: Project) : JPanel(BorderLayout()) {
    private val apiClient = PromptEfficiencyApiClient.getInstance()
    private val settings = PromptEfficiencySettings.getInstance()

    private val toolbar = JToolBar()
    private val statusPanel = JPanel(BorderLayout())
    private val statusLabel = JLabel("Ready")
    private val progressBar = JProgressBar()
    private val resultsTable = JBTable(DefaultTableModel(arrayOf("Metric", "Value"), 0))
    private val suggestionsList = JList<String>()
    private val suggestionsModel = DefaultListModel<String>()

    init {
        setupUI()
        setupToolbar()
        setupStatusPanel()
        setupResultsPanel()
    }

    private fun setupUI() {
        // Main layout
        add(toolbar, BorderLayout.NORTH)
        add(statusPanel, BorderLayout.SOUTH)

        // Results panel
        val resultsPanel = JPanel(BorderLayout())
        val scrollPane = JBScrollPane(resultsTable)
        scrollPane.preferredSize = Dimension(400, 200)
        resultsPanel.add(scrollPane, BorderLayout.CENTER)

        // Suggestions panel
        val suggestionsPanel = JPanel(BorderLayout())
        suggestionsList.model = suggestionsModel
        val suggestionsScrollPane = JBScrollPane(suggestionsList)
        suggestionsScrollPane.preferredSize = Dimension(400, 100)
        suggestionsPanel.add(JLabel("Suggestions:"), BorderLayout.NORTH)
        suggestionsPanel.add(suggestionsScrollPane, BorderLayout.CENTER)

        // Combine panels
        val mainPanel = JPanel(BorderLayout())
        mainPanel.add(resultsPanel, BorderLayout.CENTER)
        mainPanel.add(suggestionsPanel, BorderLayout.SOUTH)
        add(mainPanel, BorderLayout.CENTER)
    }

    private fun setupToolbar() {
        val analyzeButton = JButton("Analyze")
        val optimizeButton = JButton("Optimize")
        val estimateButton = JButton("Estimate Cost")
        val scanButton = JButton("Scan Repository")
        val translateButton = JButton("Translate")

        analyzeButton.addActionListener { analyzeSelectedText() }
        optimizeButton.addActionListener { optimizeSelectedText() }
        estimateButton.addActionListener { estimateCost() }
        scanButton.addActionListener { scanRepository() }
        translateButton.addActionListener { translatePrompt() }

        toolbar.add(analyzeButton)
        toolbar.add(optimizeButton)
        toolbar.add(estimateButton)
        toolbar.add(scanButton)
        toolbar.add(translateButton)
    }

    private fun setupStatusPanel() {
        statusPanel.add(statusLabel, BorderLayout.WEST)
        statusPanel.add(progressBar, BorderLayout.CENTER)
        progressBar.isVisible = false
    }

    private fun setupResultsPanel() {
        resultsTable.model = DefaultTableModel(arrayOf("Metric", "Value"), 0)
        resultsTable.setShowGrid(true)
    }

    private fun analyzeSelectedText() {
        val editor = getCurrentEditor() ?: return
        val selectedText = editor.selectionModel.selectedText ?: return

        showProgress("Analyzing prompt...")
        try {
            val result = apiClient.analyzePrompt(selectedText)
            updateResultsTable(mapOf(
                "Token Count" to result.tokenCount.toString(),
                "Estimated Cost" to "${result.estimatedCost} ${settings.currency}",
                "Complexity" to result.complexity,
                "Readability" to result.readability
            ))
            updateSuggestions(result.suggestions)
            statusLabel.text = "Analysis complete"
        } catch (e: Exception) {
            showError("Analysis failed: ${e.message}")
        } finally {
            hideProgress()
        }
    }

    private fun optimizeSelectedText() {
        val editor = getCurrentEditor() ?: return
        val selectedText = editor.selectionModel.selectedText ?: return

        showProgress("Optimizing prompt...")
        try {
            val result = apiClient.optimizePrompt(selectedText)
            updateResultsTable(mapOf(
                "Token Reduction" to result.tokenReduction.toString(),
                "Cost Reduction" to "${result.costReduction} ${settings.currency}",
                "Optimized Prompt" to result.optimizedPrompt
            ))
            updateSuggestions(result.improvements)
            statusLabel.text = "Optimization complete"
        } catch (e: Exception) {
            showError("Optimization failed: ${e.message}")
        } finally {
            hideProgress()
        }
    }

    private fun estimateCost() {
        val editor = getCurrentEditor() ?: return
        val selectedText = editor.selectionModel.selectedText ?: return

        showProgress("Estimating cost...")
        try {
            val result = apiClient.estimateCost(selectedText, settings.defaultModel)
            updateResultsTable(mapOf(
                "Token Count" to result.tokenCount.toString(),
                "Estimated Cost" to "${result.estimatedCost} ${result.currency}",
                "Model" to result.model
            ))
            statusLabel.text = "Cost estimation complete"
        } catch (e: Exception) {
            showError("Cost estimation failed: ${e.message}")
        } finally {
            hideProgress()
        }
    }

    private fun scanRepository() {
        showProgress("Scanning repository...")
        try {
            val result = apiClient.scanRepository(project.basePath)
            updateResultsTable(mapOf(
                "Total Prompts" to result.totalPrompts.toString(),
                "Total Tokens" to result.totalTokens.toString(),
                "Estimated Cost" to "${result.estimatedCost} ${settings.currency}"
            ))
            updateSuggestions(result.suggestions)
            statusLabel.text = "Repository scan complete"
        } catch (e: Exception) {
            showError("Repository scan failed: ${e.message}")
        } finally {
            hideProgress()
        }
    }

    private fun translatePrompt() {
        val editor = getCurrentEditor() ?: return
        val selectedText = editor.selectionModel.selectedText ?: return

        val targetLanguage = JOptionPane.showInputDialog(
            this,
            "Enter target language code (e.g., 'es' for Spanish):",
            "Translate Prompt",
            JOptionPane.QUESTION_MESSAGE
        ) ?: return

        showProgress("Translating prompt...")
        try {
            val result = apiClient.translatePrompt(selectedText, targetLanguage)
            updateResultsTable(mapOf(
                "Translated Prompt" to result.translatedPrompt,
                "Source Language" to result.sourceLanguage,
                "Target Language" to result.targetLanguage,
                "Confidence" to result.confidence.toString()
            ))
            statusLabel.text = "Translation complete"
        } catch (e: Exception) {
            showError("Translation failed: ${e.message}")
        } finally {
            hideProgress()
        }
    }

    private fun getCurrentEditor(): Editor? {
        val editor = com.intellij.openapi.fileEditor.FileEditorManager.getInstance(project).selectedTextEditor
        return editor
    }

    private fun updateResultsTable(results: Map<String, String>) {
        val model = resultsTable.model as DefaultTableModel
        model.rowCount = 0
        results.forEach { (metric, value) ->
            model.addRow(arrayOf(metric, value))
        }
    }

    private fun updateSuggestions(suggestions: List<String>) {
        suggestionsModel.clear()
        suggestions.forEach { suggestionsModel.addElement(it) }
    }

    private fun showProgress(message: String) {
        statusLabel.text = message
        progressBar.isIndeterminate = true
        progressBar.isVisible = true
    }

    private fun hideProgress() {
        progressBar.isVisible = false
        progressBar.isIndeterminate = false
    }

    private fun showError(message: String) {
        statusLabel.text = message
        JOptionPane.showMessageDialog(
            this,
            message,
            "Error",
            JOptionPane.ERROR_MESSAGE
        )
    }
} 