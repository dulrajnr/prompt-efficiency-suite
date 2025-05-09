package com.prompt.efficiency.settings

import com.intellij.openapi.options.Configurable
import com.intellij.openapi.options.ConfigurationException
import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.ComboBox
import com.intellij.ui.components.JBCheckBox
import com.intellij.ui.components.JBLabel
import com.intellij.ui.components.JBTextField
import com.intellij.util.ui.FormBuilder
import javax.swing.JComponent
import javax.swing.JPanel

class PromptEfficiencyConfigurable : Configurable {
    private var mainPanel: JPanel? = null
    private val apiKeyField = JBTextField()
    private val serverUrlField = JBTextField()
    private val defaultModelCombo = ComboBox(arrayOf("gpt-4", "gpt-3.5-turbo", "claude-2", "claude-instant"))
    private val defaultCurrencyCombo = ComboBox(arrayOf("USD", "EUR", "GBP"))
    private val autoCheckConnectionBox = JBCheckBox()
    private val connectionCheckIntervalField = JBTextField()

    override fun getDisplayName(): String = "Prompt Efficiency"

    override fun createComponent(): JComponent {
        val settings = PromptEfficiencySettings.getInstance()
        
        apiKeyField.text = settings.apiKey
        serverUrlField.text = settings.serverUrl
        defaultModelCombo.selectedItem = settings.defaultModel
        defaultCurrencyCombo.selectedItem = settings.defaultCurrency
        autoCheckConnectionBox.isSelected = settings.autoCheckConnection
        connectionCheckIntervalField.text = settings.connectionCheckInterval.toString()

        mainPanel = FormBuilder.createFormBuilder()
            .addLabeledComponent(JBLabel("API Key:"), apiKeyField, 1, false)
            .addLabeledComponent(JBLabel("Server URL:"), serverUrlField, 1, false)
            .addLabeledComponent(JBLabel("Default Model:"), defaultModelCombo, 1, false)
            .addLabeledComponent(JBLabel("Default Currency:"), defaultCurrencyCombo, 1, false)
            .addLabeledComponent(JBLabel("Auto Check Connection:"), autoCheckConnectionBox, 1, false)
            .addLabeledComponent(JBLabel("Connection Check Interval (ms):"), connectionCheckIntervalField, 1, false)
            .addComponentFillVertically(JPanel(), 0)
            .panel

        return mainPanel!!
    }

    override fun isModified(): Boolean {
        val settings = PromptEfficiencySettings.getInstance()
        return apiKeyField.text != settings.apiKey ||
                serverUrlField.text != settings.serverUrl ||
                defaultModelCombo.selectedItem != settings.defaultModel ||
                defaultCurrencyCombo.selectedItem != settings.defaultCurrency ||
                autoCheckConnectionBox.isSelected != settings.autoCheckConnection ||
                connectionCheckIntervalField.text.toIntOrNull() != settings.connectionCheckInterval
    }

    @Throws(ConfigurationException::class)
    override fun apply() {
        val settings = PromptEfficiencySettings.getInstance()
        settings.apiKey = apiKeyField.text
        settings.serverUrl = serverUrlField.text
        settings.defaultModel = defaultModelCombo.selectedItem as String
        settings.defaultCurrency = defaultCurrencyCombo.selectedItem as String
        settings.autoCheckConnection = autoCheckConnectionBox.isSelected
        settings.connectionCheckInterval = connectionCheckIntervalField.text.toIntOrNull() ?: 30000
    }

    override fun reset() {
        val settings = PromptEfficiencySettings.getInstance()
        apiKeyField.text = settings.apiKey
        serverUrlField.text = settings.serverUrl
        defaultModelCombo.selectedItem = settings.defaultModel
        defaultCurrencyCombo.selectedItem = settings.defaultCurrency
        autoCheckConnectionBox.isSelected = settings.autoCheckConnection
        connectionCheckIntervalField.text = settings.connectionCheckInterval.toString()
    }

    override fun disposeUIResources() {
        mainPanel = null
    }
} 