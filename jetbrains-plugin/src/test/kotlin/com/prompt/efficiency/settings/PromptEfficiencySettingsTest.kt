package com.prompt.efficiency.settings

import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.testFramework.LightPlatformTestCase
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.Assertions.*

class PromptEfficiencySettingsTest : LightPlatformTestCase() {
    private lateinit var settings: PromptEfficiencySettings

    @BeforeEach
    override fun setUp() {
        super.setUp()
        settings = PromptEfficiencySettings()
    }

    @Test
    fun `test default values`() {
        assertEquals("https://api.prompt.com", settings.serverUrl)
        assertEquals("", settings.apiKey)
        assertEquals("gpt-4", settings.defaultModel)
        assertEquals("USD", settings.currency)
        assertEquals(30, settings.timeout)
        assertEquals(4096, settings.maxTokens)
        assertFalse(settings.autoAnalyze)
        assertTrue(settings.showSuggestions)
        assertTrue(settings.enableTemplates)
    }

    @Test
    fun `test state persistence`() {
        // Set new values
        settings.serverUrl = "https://test.api.com"
        settings.apiKey = "test-key"
        settings.defaultModel = "gpt-3.5-turbo"
        settings.currency = "EUR"
        settings.timeout = 60
        settings.maxTokens = 2048
        settings.autoAnalyze = true
        settings.showSuggestions = false
        settings.enableTemplates = false

        // Get state
        val state = settings.state

        // Verify state
        assertEquals("https://test.api.com", state.serverUrl)
        assertEquals("test-key", state.apiKey)
        assertEquals("gpt-3.5-turbo", state.defaultModel)
        assertEquals("EUR", state.currency)
        assertEquals(60, state.timeout)
        assertEquals(2048, state.maxTokens)
        assertTrue(state.autoAnalyze)
        assertFalse(state.showSuggestions)
        assertFalse(state.enableTemplates)
    }

    @Test
    fun `test load state`() {
        // Create state with new values
        val state = PromptEfficiencySettings().apply {
            serverUrl = "https://test.api.com"
            apiKey = "test-key"
            defaultModel = "gpt-3.5-turbo"
            currency = "EUR"
            timeout = 60
            maxTokens = 2048
            autoAnalyze = true
            showSuggestions = false
            enableTemplates = false
        }

        // Load state
        settings.loadState(state)

        // Verify loaded values
        assertEquals("https://test.api.com", settings.serverUrl)
        assertEquals("test-key", settings.apiKey)
        assertEquals("gpt-3.5-turbo", settings.defaultModel)
        assertEquals("EUR", settings.currency)
        assertEquals(60, settings.timeout)
        assertEquals(2048, settings.maxTokens)
        assertTrue(settings.autoAnalyze)
        assertFalse(settings.showSuggestions)
        assertFalse(settings.enableTemplates)
    }
}

class PromptEfficiencySettingsPanelTest : LightPlatformTestCase() {
    private lateinit var panel: PromptEfficiencySettingsPanel
    private lateinit var settings: PromptEfficiencySettings

    @BeforeEach
    override fun setUp() {
        super.setUp()
        settings = PromptEfficiencySettings()
        panel = PromptEfficiencySettingsPanel(project)
    }

    @Test
    fun `test initial component state`() {
        val component = panel.createComponent()
        assertNotNull(component)
    }

    @Test
    fun `test apply settings`() {
        // Create component
        val component = panel.createComponent()

        // Set values
        val serverUrlField = findComponent<JBTextField>(component, "Server URL:")
        val apiKeyField = findComponent<JBTextField>(component, "API Key:")
        val defaultModelCombo = findComponent<ComboBox<String>>(component, "Default Model:")
        val currencyCombo = findComponent<ComboBox<String>>(component, "Currency:")
        val timeoutField = findComponent<JBTextField>(component, "Timeout (seconds):")
        val maxTokensField = findComponent<JBTextField>(component, "Max Tokens:")
        val autoAnalyzeCheckbox = findComponent<JCheckBox>(component, "Auto-analyze selected text")
        val showSuggestionsCheckbox = findComponent<JCheckBox>(component, "Show improvement suggestions")
        val enableTemplatesCheckbox = findComponent<JCheckBox>(component, "Enable template management")

        serverUrlField.text = "https://test.api.com"
        apiKeyField.text = "test-key"
        defaultModelCombo.selectedItem = "gpt-3.5-turbo"
        currencyCombo.selectedItem = "EUR"
        timeoutField.text = "60"
        maxTokensField.text = "2048"
        autoAnalyzeCheckbox.isSelected = true
        showSuggestionsCheckbox.isSelected = false
        enableTemplatesCheckbox.isSelected = false

        // Apply settings
        panel.apply()

        // Verify settings
        assertEquals("https://test.api.com", settings.serverUrl)
        assertEquals("test-key", settings.apiKey)
        assertEquals("gpt-3.5-turbo", settings.defaultModel)
        assertEquals("EUR", settings.currency)
        assertEquals(60, settings.timeout)
        assertEquals(2048, settings.maxTokens)
        assertTrue(settings.autoAnalyze)
        assertFalse(settings.showSuggestions)
        assertFalse(settings.enableTemplates)
    }

    @Test
    fun `test validation`() {
        // Create component
        val component = panel.createComponent()

        // Set invalid values
        val serverUrlField = findComponent<JBTextField>(component, "Server URL:")
        val apiKeyField = findComponent<JBTextField>(component, "API Key:")
        val timeoutField = findComponent<JBTextField>(component, "Timeout (seconds):")
        val maxTokensField = findComponent<JBTextField>(component, "Max Tokens:")

        serverUrlField.text = ""
        apiKeyField.text = ""
        timeoutField.text = "-1"
        maxTokensField.text = "0"

        // Verify validation
        assertThrows(ConfigurationException::class.java) {
            panel.apply()
        }
    }

    private inline fun <reified T : Component> findComponent(parent: Container, label: String): T {
        for (component in parent.components) {
            if (component is JPanel) {
                for (child in component.components) {
                    if (child is JBLabel && child.text == label) {
                        val nextComponent = component.getComponent(component.getComponentZOrder(child) + 1)
                        if (nextComponent is T) {
                            return nextComponent
                        }
                    }
                }
            }
            if (component is Container) {
                try {
                    return findComponent(component, label)
                } catch (e: NoSuchElementException) {
                    // Continue searching
                }
            }
        }
        throw NoSuchElementException("Component of type ${T::class.java} with label '$label' not found")
    }
} 