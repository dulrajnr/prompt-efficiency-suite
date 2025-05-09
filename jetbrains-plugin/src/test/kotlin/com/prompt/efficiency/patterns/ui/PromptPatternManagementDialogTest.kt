package com.prompt.efficiency.patterns.ui

import com.intellij.testFramework.LightPlatformTestCase
import com.prompt.efficiency.patterns.PromptPatternLibrary
import java.util.UUID
import javax.swing.JTable
import javax.swing.table.DefaultTableModel

class PromptPatternManagementDialogTest : LightPlatformTestCase() {
    private lateinit var dialog: PromptPatternManagementDialog
    private lateinit var patternLibrary: PromptPatternLibrary

    override fun setUp() {
        super.setUp()
        patternLibrary = PromptPatternLibrary.getInstance(project)
        dialog = PromptPatternManagementDialog(project)
    }

    fun testInitialState() {
        // Verify initial state of dialog components
        assertNotNull(dialog.contentPanel)
        assertTrue(dialog.isVisible)
        assertTrue(dialog.isShowing)
    }

    fun testAddPattern() {
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

        // Add pattern to library
        patternLibrary.addPattern(pattern)

        // Verify pattern appears in table
        val table = findTable(dialog.contentPanel)
        assertNotNull(table)
        val model = table.model as DefaultTableModel
        assertEquals(1, model.rowCount)
        assertEquals(pattern.name, model.getValueAt(0, 0))
        assertEquals(pattern.category, model.getValueAt(0, 1))
        assertEquals(pattern.model, model.getValueAt(0, 2))
    }

    fun testEditPattern() {
        // Create and add a test pattern
        val pattern = PromptPatternLibrary.PromptPattern(
            id = UUID.randomUUID().toString(),
            name = "Original Name",
            description = "Original Description",
            template = "Original Template",
            category = "Original Category",
            model = "gpt-4",
            tags = mutableSetOf("original"),
            usageCount = 0,
            successRate = 0.0,
            lastUsed = 0
        )
        patternLibrary.addPattern(pattern)

        // Edit the pattern
        val editedPattern = pattern.copy(
            name = "Updated Name",
            description = "Updated Description",
            template = "Updated Template",
            category = "Updated Category",
            tags = mutableSetOf("updated")
        )
        patternLibrary.updatePattern(editedPattern)

        // Verify pattern is updated in table
        val table = findTable(dialog.contentPanel)
        assertNotNull(table)
        val model = table.model as DefaultTableModel
        assertEquals(1, model.rowCount)
        assertEquals(editedPattern.name, model.getValueAt(0, 0))
        assertEquals(editedPattern.category, model.getValueAt(0, 1))
        assertEquals(editedPattern.model, model.getValueAt(0, 2))
    }

    fun testDeletePattern() {
        // Create and add a test pattern
        val pattern = PromptPatternLibrary.PromptPattern(
            id = UUID.randomUUID().toString(),
            name = "Test Pattern",
            description = "Test Description",
            template = "Test Template",
            category = "Test Category",
            model = "gpt-4",
            tags = mutableSetOf("test"),
            usageCount = 0,
            successRate = 0.0,
            lastUsed = 0
        )
        patternLibrary.addPattern(pattern)

        // Delete the pattern
        patternLibrary.deletePattern(pattern.id)

        // Verify pattern is removed from table
        val table = findTable(dialog.contentPanel)
        assertNotNull(table)
        val model = table.model as DefaultTableModel
        assertEquals(0, model.rowCount)
    }

    fun testFilterPatterns() {
        // Create test patterns
        val pattern1 = PromptPatternLibrary.PromptPattern(
            id = UUID.randomUUID().toString(),
            name = "Pattern 1",
            description = "Description 1",
            template = "Template 1",
            category = "Category 1",
            model = "gpt-4",
            tags = mutableSetOf("tag1"),
            usageCount = 0,
            successRate = 0.0,
            lastUsed = 0
        )
        val pattern2 = PromptPatternLibrary.PromptPattern(
            id = UUID.randomUUID().toString(),
            name = "Pattern 2",
            description = "Description 2",
            template = "Template 2",
            category = "Category 2",
            model = "gpt-3.5-turbo",
            tags = mutableSetOf("tag2"),
            usageCount = 0,
            successRate = 0.0,
            lastUsed = 0
        )
        patternLibrary.addPattern(pattern1)
        patternLibrary.addPattern(pattern2)

        // Test category filter
        val categoryCombo = findComboBox(dialog.contentPanel, "Category")
        assertNotNull(categoryCombo)
        categoryCombo.selectedItem = "Category 1"
        dialog.loadPatterns() // Trigger filter

        var table = findTable(dialog.contentPanel)
        assertNotNull(table)
        var model = table.model as DefaultTableModel
        assertEquals(1, model.rowCount)
        assertEquals(pattern1.name, model.getValueAt(0, 0))

        // Test model filter
        val modelCombo = findComboBox(dialog.contentPanel, "Model")
        assertNotNull(modelCombo)
        modelCombo.selectedItem = "gpt-3.5-turbo"
        dialog.loadPatterns() // Trigger filter

        table = findTable(dialog.contentPanel)
        assertNotNull(table)
        model = table.model as DefaultTableModel
        assertEquals(1, model.rowCount)
        assertEquals(pattern2.name, model.getValueAt(0, 0))
    }

    private fun findTable(component: java.awt.Component): JTable? {
        if (component is JTable) {
            return component
        }
        if (component is java.awt.Container) {
            for (child in component.components) {
                val found = findTable(child)
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