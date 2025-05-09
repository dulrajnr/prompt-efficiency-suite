package com.prompt.efficiency.collab.ui

import com.intellij.testFramework.LightPlatformTestCase
import com.prompt.efficiency.collab.TeamPatternManager
import com.prompt.efficiency.settings.PromptEfficiencySettings
import java.util.*
import javax.swing.JTextField
import javax.swing.JTextArea
import javax.swing.JComboBox

class TeamPatternDialogTest : LightPlatformTestCase() {
    private lateinit var dialog: TeamPatternDialog
    private lateinit var settings: PromptEfficiencySettings

    override fun setUp() {
        super.setUp()
        settings = PromptEfficiencySettings.getInstance(project)
        settings.setModelSettings(listOf(
            PromptEfficiencySettings.ModelSetting("gpt-4", 8192, 0.03, 0.06),
            PromptEfficiencySettings.ModelSetting("gpt-3.5-turbo", 4096, 0.0015, 0.002)
        ))
        dialog = TeamPatternDialog(project)
    }

    fun testInitialState() {
        // Check initial field values
        assertEquals("", findTextField("Name:").text)
        assertEquals("", findTextArea("Description:").text)
        assertEquals("", findTextArea("Template:").text)
        assertEquals("", findTextField("Category:").text)
        assertEquals("gpt-4", (findComboBox("Model:") as JComboBox<String>).selectedItem)
        assertEquals("", findTextField("Tags (comma-separated):").text)
    }

    fun testLoadPattern() {
        val pattern = TeamPatternManager.TeamPattern(
            id = UUID.randomUUID().toString(),
            name = "Test Pattern",
            description = "Test Description",
            template = "Test Template",
            category = "Test Category",
            model = "gpt-3.5-turbo",
            tags = setOf("test", "example"),
            author = "Test User",
            status = TeamPatternManager.PatternStatus.DRAFT,
            version = 1,
            usageCount = 0,
            successRate = 0.0,
            reviews = mutableListOf()
        )

        val editDialog = TeamPatternDialog(project, pattern)

        // Check loaded values
        assertEquals(pattern.name, findTextField(editDialog, "Name:").text)
        assertEquals(pattern.description, findTextArea(editDialog, "Description:").text)
        assertEquals(pattern.template, findTextArea(editDialog, "Template:").text)
        assertEquals(pattern.category, findTextField(editDialog, "Category:").text)
        assertEquals(pattern.model, (findComboBox(editDialog, "Model:") as JComboBox<String>).selectedItem)
        assertEquals("test, example", findTextField(editDialog, "Tags (comma-separated):").text)
    }

    fun testValidation() {
        // Test empty fields
        assertNotNull(dialog.doValidate())

        // Fill required fields
        findTextField("Name:").text = "Test Pattern"
        findTextArea("Description:").text = "Test Description"
        findTextArea("Template:").text = "Test Template"
        findTextField("Category:").text = "Test Category"

        // Test validation passes
        assertNull(dialog.doValidate())
    }

    fun testGetPattern() {
        // Fill fields
        findTextField("Name:").text = "Test Pattern"
        findTextArea("Description:").text = "Test Description"
        findTextArea("Template:").text = "Test Template"
        findTextField("Category:").text = "Test Category"
        (findComboBox("Model:") as JComboBox<String>).selectedItem = "gpt-3.5-turbo"
        findTextField("Tags (comma-separated):").text = "test, example"

        // Get pattern
        val pattern = dialog.getPattern()

        // Check pattern values
        assertEquals("Test Pattern", pattern.name)
        assertEquals("Test Description", pattern.description)
        assertEquals("Test Template", pattern.template)
        assertEquals("Test Category", pattern.category)
        assertEquals("gpt-3.5-turbo", pattern.model)
        assertEquals(setOf("test", "example"), pattern.tags)
        assertEquals(TeamPatternManager.PatternStatus.DRAFT, pattern.status)
        assertEquals(1, pattern.version)
        assertEquals(0, pattern.usageCount)
        assertEquals(0.0, pattern.successRate)
        assertTrue(pattern.reviews.isEmpty())
    }

    private fun findTextField(label: String): JTextField {
        return findTextField(dialog, label)
    }

    private fun findTextField(dialog: TeamPatternDialog, label: String): JTextField {
        return dialog.contentPane.findComponent { 
            it is JTextField && it.parent?.findComponent { it is JLabel && it.text == label } != null 
        } as JTextField
    }

    private fun findTextArea(label: String): JTextArea {
        return findTextArea(dialog, label)
    }

    private fun findTextArea(dialog: TeamPatternDialog, label: String): JTextArea {
        return dialog.contentPane.findComponent { 
            it is JTextArea && it.parent?.parent?.findComponent { it is JLabel && it.text == label } != null 
        } as JTextArea
    }

    private fun findComboBox(label: String): JComboBox<*> {
        return findComboBox(dialog, label)
    }

    private fun findComboBox(dialog: TeamPatternDialog, label: String): JComboBox<*> {
        return dialog.contentPane.findComponent { 
            it is JComboBox<*> && it.parent?.findComponent { it is JLabel && it.text == label } != null 
        } as JComboBox<*>
    }
} 