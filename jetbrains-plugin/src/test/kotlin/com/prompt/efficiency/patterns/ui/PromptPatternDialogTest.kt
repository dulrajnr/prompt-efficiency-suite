package com.prompt.efficiency.patterns.ui

import com.intellij.testFramework.LightPlatformTestCase
import com.prompt.efficiency.patterns.PromptPatternLibrary
import java.util.UUID
import javax.swing.JTextField
import javax.swing.JTextArea
import javax.swing.JComboBox

class PromptPatternDialogTest : LightPlatformTestCase() {
    private lateinit var dialog: PromptPatternDialog
    private lateinit var patternLibrary: PromptPatternLibrary

    override fun setUp() {
        super.setUp()
        patternLibrary = PromptPatternLibrary.getInstance(project)
        dialog = PromptPatternDialog(project)
    }

    fun testInitialState() {
        // Verify initial state of dialog components
        assertNotNull(dialog.contentPanel)
        assertTrue(dialog.isVisible)
        assertTrue(dialog.isShowing)

        // Verify all fields are empty
        val nameField = findTextField(dialog.contentPanel, "Name")
        val descriptionField = findTextField(dialog.contentPanel, "Description")
        val templateField = findTextArea(dialog.contentPanel, "Template")
        val categoryCombo = findComboBox(dialog.contentPanel, "Category")
        val modelCombo = findComboBox(dialog.contentPanel, "Model")
        val tagsField = findTextField(dialog.contentPanel, "Tags")

        assertNotNull(nameField)
        assertNotNull(descriptionField)
        assertNotNull(templateField)
        assertNotNull(categoryCombo)
        assertNotNull(modelCombo)
        assertNotNull(tagsField)

        assertEquals("", nameField.text)
        assertEquals("", descriptionField.text)
        assertEquals("", templateField.text)
        assertEquals("", tagsField.text)
    }

    fun testEditExistingPattern() {
        // Create a test pattern
        val pattern = PromptPatternLibrary.PromptPattern(
            id = UUID.randomUUID().toString(),
            name = "Test Pattern",
            description = "Test Description",
            template = "Test Template",
            category = "Test Category",
            model = "gpt-4",
            tags = mutableSetOf("test", "pattern"),
            usageCount = 0,
            successRate = 0.0,
            lastUsed = 0
        )

        // Create dialog with existing pattern
        val editDialog = PromptPatternDialog(project, pattern)

        // Verify fields are populated with pattern data
        val nameField = findTextField(editDialog.contentPanel, "Name")
        val descriptionField = findTextField(editDialog.contentPanel, "Description")
        val templateField = findTextArea(editDialog.contentPanel, "Template")
        val categoryCombo = findComboBox(editDialog.contentPanel, "Category")
        val modelCombo = findComboBox(editDialog.contentPanel, "Model")
        val tagsField = findTextField(editDialog.contentPanel, "Tags")

        assertNotNull(nameField)
        assertNotNull(descriptionField)
        assertNotNull(templateField)
        assertNotNull(categoryCombo)
        assertNotNull(modelCombo)
        assertNotNull(tagsField)

        assertEquals(pattern.name, nameField.text)
        assertEquals(pattern.description, descriptionField.text)
        assertEquals(pattern.template, templateField.text)
        assertEquals(pattern.category, categoryCombo.selectedItem)
        assertEquals(pattern.model, modelCombo.selectedItem)
        assertEquals(pattern.tags.joinToString(", "), tagsField.text)
    }

    fun testValidation() {
        // Test empty name
        val nameField = findTextField(dialog.contentPanel, "Name")
        val templateField = findTextArea(dialog.contentPanel, "Template")
        val categoryCombo = findComboBox(dialog.contentPanel, "Category")
        val modelCombo = findComboBox(dialog.contentPanel, "Model")

        assertNotNull(nameField)
        assertNotNull(templateField)
        assertNotNull(categoryCombo)
        assertNotNull(modelCombo)

        nameField.text = ""
        templateField.text = "Test Template"
        categoryCombo.selectedItem = "Test Category"
        modelCombo.selectedItem = "gpt-4"

        assertFalse(dialog.validateInput())

        // Test empty template
        nameField.text = "Test Pattern"
        templateField.text = ""
        assertFalse(dialog.validateInput())

        // Test empty category
        templateField.text = "Test Template"
        categoryCombo.selectedItem = null
        assertFalse(dialog.validateInput())

        // Test empty model
        categoryCombo.selectedItem = "Test Category"
        modelCombo.selectedItem = null
        assertFalse(dialog.validateInput())

        // Test valid input
        modelCombo.selectedItem = "gpt-4"
        assertTrue(dialog.validateInput())
    }

    fun testGetPattern() {
        // Set up test data
        val nameField = findTextField(dialog.contentPanel, "Name")
        val descriptionField = findTextField(dialog.contentPanel, "Description")
        val templateField = findTextArea(dialog.contentPanel, "Template")
        val categoryCombo = findComboBox(dialog.contentPanel, "Category")
        val modelCombo = findComboBox(dialog.contentPanel, "Model")
        val tagsField = findTextField(dialog.contentPanel, "Tags")

        assertNotNull(nameField)
        assertNotNull(descriptionField)
        assertNotNull(templateField)
        assertNotNull(categoryCombo)
        assertNotNull(modelCombo)
        assertNotNull(tagsField)

        nameField.text = "Test Pattern"
        descriptionField.text = "Test Description"
        templateField.text = "Test Template"
        categoryCombo.selectedItem = "Test Category"
        modelCombo.selectedItem = "gpt-4"
        tagsField.text = "test, pattern"

        // Get pattern and verify data
        val pattern = dialog.getPattern()
        assertEquals("Test Pattern", pattern.name)
        assertEquals("Test Description", pattern.description)
        assertEquals("Test Template", pattern.template)
        assertEquals("Test Category", pattern.category)
        assertEquals("gpt-4", pattern.model)
        assertEquals(setOf("test", "pattern"), pattern.tags)
    }

    private fun findTextField(component: java.awt.Component, name: String): JTextField? {
        if (component is JTextField && component.name == name) {
            return component
        }
        if (component is java.awt.Container) {
            for (child in component.components) {
                val found = findTextField(child, name)
                if (found != null) {
                    return found
                }
            }
        }
        return null
    }

    private fun findTextArea(component: java.awt.Component, name: String): JTextArea? {
        if (component is JTextArea && component.name == name) {
            return component
        }
        if (component is java.awt.Container) {
            for (child in component.components) {
                val found = findTextArea(child, name)
                if (found != null) {
                    return found
                }
            }
        }
        return null
    }

    private fun findComboBox(component: java.awt.Component, name: String): JComboBox<*>? {
        if (component is JComboBox<*> && component.name == name) {
            return component
        }
        if (component is java.awt.Container) {
            for (child in component.components) {
                val found = findComboBox(child, name)
                if (found != null) {
                    return found
                }
            }
        }
        return null
    }
}
