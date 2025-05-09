package com.prompt.efficiency.templates

import com.intellij.openapi.project.Project
import com.intellij.testFramework.fixtures.BasePlatformTestCase
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.table.JBTable
import org.mockito.Mockito.*
import java.awt.event.ActionEvent
import javax.swing.*
import javax.swing.table.DefaultTableModel

class PromptTemplateDialogTest : BasePlatformTestCase() {
    private lateinit var dialog: PromptTemplateDialog
    private lateinit var mockProject: Project
    private lateinit var templateManager: PromptTemplate

    override fun setUp() {
        super.setUp()
        mockProject = mock(Project::class.java)
        templateManager = PromptTemplate()
        dialog = PromptTemplateDialog(mockProject)
    }

    @Test
    fun `test dialog initialization`() {
        assertNotNull(dialog.nameField)
        assertNotNull(dialog.descriptionField)
        assertNotNull(dialog.contentArea)
        assertNotNull(dialog.categoryField)
        assertNotNull(dialog.variablesField)
        assertNotNull(dialog.tagsField)
        assertNotNull(dialog.authorField)
        assertNotNull(dialog.isPublicCheckBox)
        assertNotNull(dialog.templatesTable)
        assertNotNull(dialog.versionsTable)
        assertNotNull(dialog.sharedTemplatesTable)
    }

    @Test
    fun `test create new template`() {
        // Fill in template fields
        dialog.nameField.text = "Test Template"
        dialog.descriptionField.text = "A test template"
        dialog.contentArea.text = "Hello \${name}!"
        dialog.categoryField.text = "Test"
        dialog.variablesField.text = "name"
        dialog.tagsField.text = "greeting"
        dialog.authorField.text = "Test User"
        dialog.isPublicCheckBox.isSelected = true

        // Trigger OK action
        dialog.doOKAction()

        // Verify template was created
        val template = templateManager.getTemplate("Test Template")
        assertNotNull(template)
        assertEquals("Test Template", template?.name)
        assertEquals("A test template", template?.description)
        assertEquals("Hello \${name}!", template?.content)
        assertEquals("Test", template?.category)
        assertEquals(listOf("name"), template?.variables)
        assertEquals(setOf("greeting"), template?.tags)
        assertEquals("Test User", template?.author)
        assertTrue(template?.isPublic ?: false)
    }

    @Test
    fun `test edit template`() {
        // Create initial template
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "Initial description",
            content = "Initial content",
            category = "Test",
            variables = mutableListOf("name"),
            author = "Test User"
        )
        templateManager.addTemplate(template)

        // Select template in table
        val model = dialog.templatesTable.model as DefaultTableModel
        model.addRow(arrayOf("Test Template", "Initial description", "Test", "Test User"))

        // Edit template
        dialog.editSelectedTemplate()

        // Update fields
        dialog.descriptionField.text = "Updated description"
        dialog.contentArea.text = "Updated content"

        // Save changes
        dialog.doOKAction()

        // Verify template was updated
        val updatedTemplate = templateManager.getTemplate("Test Template")
        assertNotNull(updatedTemplate)
        assertEquals("Updated description", updatedTemplate?.description)
        assertEquals("Updated content", updatedTemplate?.content)
        assertEquals(2, updatedTemplate?.versions?.size)
    }

    @Test
    fun `test delete template`() {
        // Create template
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            author = "Test User"
        )
        templateManager.addTemplate(template)

        // Select template in table
        val model = dialog.templatesTable.model as DefaultTableModel
        model.addRow(arrayOf("Test Template", "A test template", "Test", "Test User"))

        // Delete template
        dialog.deleteSelectedTemplate()

        // Verify template was deleted
        assertNull(templateManager.getTemplate("Test Template"))
    }

    @Test
    fun `test share template`() {
        // Create template
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            author = "Test User",
            isPublic = true
        )
        templateManager.addTemplate(template)

        // Select template in table
        val model = dialog.templatesTable.model as DefaultTableModel
        model.addRow(arrayOf("Test Template", "A test template", "Test", "Test User"))

        // Share template
        dialog.shareSelectedTemplate()

        // Verify template was shared
        val sharedTemplate = templateManager.sharedTemplates.values.first()
        assertEquals("Test Template", sharedTemplate.template.name)
        assertEquals("Test User", sharedTemplate.sharedBy)
        assertTrue(sharedTemplate.isPublic)
    }

    @Test
    fun `test version management`() {
        // Create template with multiple versions
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Version 1",
            category = "Test",
            variables = mutableListOf("name"),
            author = "Test User"
        )
        templateManager.addTemplate(template)

        // Update template to create new version
        val updatedTemplate = template.copy(
            content = "Version 2",
            updatedAt = java.util.Date()
        )
        templateManager.updateTemplate(template.name, updatedTemplate)

        // Select template in table
        val model = dialog.templatesTable.model as DefaultTableModel
        model.addRow(arrayOf("Test Template", "A test template", "Test", "Test User"))

        // Verify versions table
        val versionsModel = dialog.versionsTable.model as DefaultTableModel
        assertEquals(2, versionsModel.rowCount)
        assertEquals("Version 2", versionsModel.getValueAt(0, 1))
        assertEquals("Version 1", versionsModel.getValueAt(1, 1))
    }

    @Test
    fun `test shared templates table`() {
        // Create and share template
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            author = "Test User",
            isPublic = true
        )
        templateManager.addTemplate(template)
        templateManager.shareTemplate(template.name)

        // Add review
        val review = PromptTemplate.Review(
            rating = 5,
            comment = "Great template!",
            reviewer = "Reviewer"
        )
        templateManager.addReview(templateManager.sharedTemplates.values.first().id, review)

        // Verify shared templates table
        val model = dialog.sharedTemplatesTable.model as DefaultTableModel
        assertEquals(1, model.rowCount)
        assertEquals("Test Template", model.getValueAt(0, 0))
        assertEquals("Test User", model.getValueAt(0, 1))
        assertEquals(5.0, model.getValueAt(0, 2))
        assertEquals(1, model.getValueAt(0, 3))
    }

    @Test
    fun `test template filtering`() {
        // Create templates with different categories and tags
        val template1 = PromptTemplate.Template(
            name = "Template 1",
            description = "First template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            tags = mutableSetOf("greeting"),
            author = "User 1"
        )

        val template2 = PromptTemplate.Template(
            name = "Template 2",
            description = "Second template",
            content = "Goodbye \${name}!",
            category = "Other",
            variables = mutableListOf("name"),
            tags = mutableSetOf("farewell"),
            author = "User 2"
        )

        templateManager.addTemplate(template1)
        templateManager.addTemplate(template2)

        // Test category filter
        dialog.categoryFilter.text = "Test"
        dialog.applyFilters()

        val model = dialog.templatesTable.model as DefaultTableModel
        assertEquals(1, model.rowCount)
        assertEquals("Template 1", model.getValueAt(0, 0))

        // Test tag filter
        dialog.categoryFilter.text = ""
        dialog.tagFilter.text = "farewell"
        dialog.applyFilters()

        assertEquals(1, model.rowCount)
        assertEquals("Template 2", model.getValueAt(0, 0))

        // Test author filter
        dialog.tagFilter.text = ""
        dialog.authorFilter.text = "User 1"
        dialog.applyFilters()

        assertEquals(1, model.rowCount)
        assertEquals("Template 1", model.getValueAt(0, 0))
    }
} 