package com.prompt.efficiency.settings

import com.intellij.openapi.options.Configurable
import com.intellij.openapi.options.ConfigurationException
import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.ComboBox
import com.intellij.ui.components.JBLabel
import com.intellij.ui.components.JBTextField
import com.intellij.util.ui.FormBuilder
import javax.swing.JComponent
import javax.swing.JPanel

class PromptEfficiencySettingsPanel(private val project: Project) : Configurable {
    private val serverUrlField = JBTextField()
    private val apiKeyField = JBTextField()
    private val defaultModelCombo = ComboBox(arrayOf("gpt-4", "gpt-3.5-turbo", "claude-2", "claude-instant"))
    private val currencyCombo = ComboBox(arrayOf("USD", "EUR", "GBP", "JPY"))
    private val timeoutField = JBTextField()
    private val maxTokensField = JBTextField()
    private val autoAnalyzeCheckbox = javax.swing.JCheckBox()
    private val showSuggestionsCheckbox = javax.swing.JCheckBox()
    private val enableTemplatesCheckbox = javax.swing.JCheckBox()

    private var modified = false

    override fun getDisplayName(): String = "Prompt Efficiency"

    override fun createComponent(): JComponent {
        val settings = PromptEfficiencySettings.getInstance()

        // Initialize fields with current settings
        serverUrlField.text = settings.serverUrl
        apiKeyField.text = settings.apiKey
        defaultModelCombo.selectedItem = settings.defaultModel
        currencyCombo.selectedItem = settings.currency
        timeoutField.text = settings.timeout.toString()
        maxTokensField.text = settings.maxTokens.toString()
        autoAnalyzeCheckbox.isSelected = settings.autoAnalyze
        showSuggestionsCheckbox.isSelected = settings.showSuggestions
        enableTemplatesCheckbox.isSelected = settings.enableTemplates

        // Add listeners to track modifications
        val textFields = listOf(serverUrlField, apiKeyField, timeoutField, maxTokensField)
        textFields.forEach { field ->
            field.document.addDocumentListener(object : javax.swing.event.DocumentListener {
                override fun insertUpdate(e: javax.swing.event.DocumentEvent?) { modified = true }
                override fun removeUpdate(e: javax.swing.event.DocumentEvent?) { modified = true }
                override fun changedUpdate(e: javax.swing.event.DocumentEvent?) { modified = true }
            })
        }

        val comboBoxes = listOf(defaultModelCombo, currencyCombo)
        comboBoxes.forEach { combo ->
            combo.addActionListener { modified = true }
        }

        val checkboxes = listOf(autoAnalyzeCheckbox, showSuggestionsCheckbox, enableTemplatesCheckbox)
        checkboxes.forEach { checkbox ->
            checkbox.addActionListener { modified = true }
        }

        return FormBuilder.createFormBuilder()
            .addLabeledComponent("Server URL:", serverUrlField)
            .addLabeledComponent("API Key:", apiKeyField)
            .addLabeledComponent("Default Model:", defaultModelCombo)
            .addLabeledComponent("Currency:", currencyCombo)
            .addLabeledComponent("Timeout (seconds):", timeoutField)
            .addLabeledComponent("Max Tokens:", maxTokensField)
            .addComponent(autoAnalyzeCheckbox.apply { text = "Auto-analyze selected text" })
            .addComponent(showSuggestionsCheckbox.apply { text = "Show improvement suggestions" })
            .addComponent(enableTemplatesCheckbox.apply { text = "Enable template management" })
            .addComponentFillVertically(JPanel(), 0)
            .panel
    }

    override fun isModified(): Boolean = modified

    @Throws(ConfigurationException::class)
    override fun apply() {
        val settings = PromptEfficiencySettings.getInstance()

        // Validate fields
        validateFields()

        // Update settings
        settings.serverUrl = serverUrlField.text
        settings.apiKey = apiKeyField.text
        settings.defaultModel = defaultModelCombo.selectedItem.toString()
        settings.currency = currencyCombo.selectedItem.toString()
        settings.timeout = timeoutField.text.toIntOrNull() ?: 30
        settings.maxTokens = maxTokensField.text.toIntOrNull() ?: 4096
        settings.autoAnalyze = autoAnalyzeCheckbox.isSelected
        settings.showSuggestions = showSuggestionsCheckbox.isSelected
        settings.enableTemplates = enableTemplatesCheckbox.isSelected

        modified = false
    }

    override fun reset() {
        val settings = PromptEfficiencySettings.getInstance()

        serverUrlField.text = settings.serverUrl
        apiKeyField.text = settings.apiKey
        defaultModelCombo.selectedItem = settings.defaultModel
        currencyCombo.selectedItem = settings.currency
        timeoutField.text = settings.timeout.toString()
        maxTokensField.text = settings.maxTokens.toString()
        autoAnalyzeCheckbox.isSelected = settings.autoAnalyze
        showSuggestionsCheckbox.isSelected = settings.showSuggestions
        enableTemplatesCheckbox.isSelected = settings.enableTemplates

        modified = false
    }

    @Throws(ConfigurationException::class)
    private fun validateFields() {
        if (serverUrlField.text.isBlank()) {
            throw ConfigurationException("Server URL cannot be empty")
        }
        if (apiKeyField.text.isBlank()) {
            throw ConfigurationException("API Key cannot be empty")
        }
        if (timeoutField.text.toIntOrNull() == null || timeoutField.text.toInt() <= 0) {
            throw ConfigurationException("Timeout must be a positive number")
        }
        if (maxTokensField.text.toIntOrNull() == null || maxTokensField.text.toInt() <= 0) {
            throw ConfigurationException("Max Tokens must be a positive number")
        }
    }
}
