package com.prompt.efficiency.settings

import com.intellij.openapi.options.Configurable
import com.intellij.openapi.project.Project
import com.intellij.testFramework.fixtures.BasePlatformTestCase
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.mockito.Mockito.*
import javax.swing.JComponent
import javax.swing.JTextField
import javax.swing.JComboBox
import javax.swing.JCheckBox
import javax.swing.JSpinner

class PromptEfficiencyConfigurableTest : BasePlatformTestCase() {
    private lateinit var configurable: PromptEfficiencyConfigurable
    private lateinit var settings: PromptEfficiencySettings
    private lateinit var project: Project

    @BeforeEach
    override fun setUp() {
        super.setUp()
        project = mock(Project::class.java)
        settings = PromptEfficiencySettings()
        configurable = PromptEfficiencyConfigurable(project)
    }

    @Test
    fun `test display name`() {
        assertEquals("Prompt Efficiency", configurable.displayName)
    }

    @Test
    fun `test create component`() {
        val component = configurable.createComponent()
        assertNotNull(component)
        assertTrue(component is JComponent)
    }

    @Test
    fun `test is modified when values change`() {
        val component = configurable.createComponent()

        // Get references to the UI components
        val apiKeyField = findComponent<JTextField>(component, "apiKeyField")
        val serverUrlField = findComponent<JTextField>(component, "serverUrlField")
        val modelCombo = findComponent<JComboBox<String>>(component, "modelCombo")
        val currencyCombo = findComponent<JComboBox<String>>(component, "currencyCombo")
        val autoCheckBox = findComponent<JCheckBox>(component, "autoCheckBox")
        val intervalSpinner = findComponent<JSpinner>(component, "intervalSpinner")

        // Change values
        apiKeyField.text = "new-key"
        serverUrlField.text = "http://new-server:8000"
        modelCombo.selectedItem = "gpt-3.5-turbo"
        currencyCombo.selectedItem = "EUR"
        autoCheckBox.isSelected = false
        intervalSpinner.value = 60000

        assertTrue(configurable.isModified)
    }

    @Test
    fun `test apply changes`() {
        val component = configurable.createComponent()

        // Get references to the UI components
        val apiKeyField = findComponent<JTextField>(component, "apiKeyField")
        val serverUrlField = findComponent<JTextField>(component, "serverUrlField")
        val modelCombo = findComponent<JComboBox<String>>(component, "modelCombo")
        val currencyCombo = findComponent<JComboBox<String>>(component, "currencyCombo")
        val autoCheckBox = findComponent<JCheckBox>(component, "autoCheckBox")
        val intervalSpinner = findComponent<JSpinner>(component, "intervalSpinner")

        // Change values
        apiKeyField.text = "new-key"
        serverUrlField.text = "http://new-server:8000"
        modelCombo.selectedItem = "gpt-3.5-turbo"
        currencyCombo.selectedItem = "EUR"
        autoCheckBox.isSelected = false
        intervalSpinner.value = 60000

        configurable.apply()

        val settings = PromptEfficiencySettings.getInstance()
        assertEquals("new-key", settings.apiKey)
        assertEquals("http://new-server:8000", settings.serverUrl)
        assertEquals("gpt-3.5-turbo", settings.defaultModel)
        assertEquals("EUR", settings.defaultCurrency)
        assertFalse(settings.autoCheckConnection)
        assertEquals(60000, settings.connectionCheckInterval)
    }

    @Test
    fun `test reset`() {
        val component = configurable.createComponent()

        // Get references to the UI components
        val apiKeyField = findComponent<JTextField>(component, "apiKeyField")
        val serverUrlField = findComponent<JTextField>(component, "serverUrlField")
        val modelCombo = findComponent<JComboBox<String>>(component, "modelCombo")
        val currencyCombo = findComponent<JComboBox<String>>(component, "currencyCombo")
        val autoCheckBox = findComponent<JCheckBox>(component, "autoCheckBox")
        val intervalSpinner = findComponent<JSpinner>(component, "intervalSpinner")

        // Change values
        apiKeyField.text = "new-key"
        serverUrlField.text = "http://new-server:8000"
        modelCombo.selectedItem = "gpt-3.5-turbo"
        currencyCombo.selectedItem = "EUR"
        autoCheckBox.isSelected = false
        intervalSpinner.value = 60000

        configurable.reset()

        assertEquals("", apiKeyField.text)
        assertEquals("http://localhost:8000", serverUrlField.text)
        assertEquals("gpt-4", modelCombo.selectedItem)
        assertEquals("USD", currencyCombo.selectedItem)
        assertTrue(autoCheckBox.isSelected)
        assertEquals(30000, intervalSpinner.value)
    }

    private inline fun <reified T : JComponent> findComponent(parent: JComponent, name: String): T {
        return parent.components
            .filterIsInstance<JComponent>()
            .find { it.name == name } as T
    }
}
