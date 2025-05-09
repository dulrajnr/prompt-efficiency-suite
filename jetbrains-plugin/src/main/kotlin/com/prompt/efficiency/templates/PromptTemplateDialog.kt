package com.prompt.efficiency.templates

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.DialogWrapper
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.table.JBTable
import com.intellij.util.ui.FormBuilder
import java.awt.BorderLayout
import java.awt.Dimension
import javax.swing.*
import javax.swing.table.DefaultTableModel
import java.util.*

class PromptTemplateDialog(
    private val project: Project,
    private val template: PromptTemplate.Template? = null
) : DialogWrapper(project) {
    private val nameField = JTextField()
    private val descriptionField = JTextField()
    private val contentArea = JTextArea()
    private val categoryField = JTextField()
    private val variablesField = JTextField()
    private val tagsField = JTextField()
    private val authorField = JTextField()
    private val isPublicCheckbox = JCheckBox("Public")
    private val templatesTable = JBTable(DefaultTableModel(arrayOf("Name", "Description", "Category", "Author", "Last Used"), 0))
    private val versionsTable = JBTable(DefaultTableModel(arrayOf("Version", "Description", "Created By", "Created At"), 0))
    private val sharedTemplatesTable = JBTable(DefaultTableModel(arrayOf("Name", "Author", "Rating", "Downloads"), 0))
    private val templateManager = PromptTemplate.getInstance()
    private val tabbedPane = JTabbedPane()

    init {
        title = if (template == null) "New Template" else "Edit Template"
        init()
        setupUI()
        if (template != null) {
            loadTemplate(template)
        }
        updateTemplatesTable()
        updateSharedTemplatesTable()
    }

    private fun setupUI() {
        contentArea.preferredSize = Dimension(400, 200)
        val scrollPane = JBScrollPane(contentArea)
        scrollPane.preferredSize = Dimension(400, 200)

        val form = FormBuilder.createFormBuilder()
            .addLabeledComponent("Name:", nameField)
            .addLabeledComponent("Description:", descriptionField)
            .addLabeledComponent("Content:", scrollPane)
            .addLabeledComponent("Category:", categoryField)
            .addLabeledComponent("Variables (comma-separated):", variablesField)
            .addLabeledComponent("Tags (comma-separated):", tagsField)
            .addLabeledComponent("Author:", authorField)
            .addComponent(isPublicCheckbox)
            .panel

        // Create tabs
        val templatesPanel = createTemplatesPanel()
        val versionsPanel = createVersionsPanel()
        val sharedPanel = createSharedTemplatesPanel()
        val marketplacePanel = createMarketplacePanel()

        tabbedPane.addTab("Templates", templatesPanel)
        tabbedPane.addTab("Versions", versionsPanel)
        tabbedPane.addTab("Shared", sharedPanel)
        tabbedPane.addTab("Marketplace", marketplacePanel)

        val mainPanel = JPanel(BorderLayout())
        mainPanel.add(form, BorderLayout.NORTH)
        mainPanel.add(tabbedPane, BorderLayout.CENTER)

        contentPanel = mainPanel
    }

    private fun createTemplatesPanel(): JPanel {
        val panel = JPanel(BorderLayout())
        val scrollPane = JBScrollPane(templatesTable)
        panel.add(scrollPane, BorderLayout.CENTER)
        panel.add(createButtonsPanel(), BorderLayout.SOUTH)
        return panel
    }

    private fun createVersionsPanel(): JPanel {
        val panel = JPanel(BorderLayout())
        val scrollPane = JBScrollPane(versionsTable)
        panel.add(scrollPane, BorderLayout.CENTER)
        panel.add(createVersionButtonsPanel(), BorderLayout.SOUTH)
        return panel
    }

    private fun createSharedTemplatesPanel(): JPanel {
        val panel = JPanel(BorderLayout())
        val scrollPane = JBScrollPane(sharedTemplatesTable)
        panel.add(scrollPane, BorderLayout.CENTER)
        panel.add(createSharedButtonsPanel(), BorderLayout.SOUTH)
        return panel
    }

    private fun createMarketplacePanel(): JPanel {
        val panel = JPanel(BorderLayout())
        val scrollPane = JBScrollPane(sharedTemplatesTable)
        panel.add(scrollPane, BorderLayout.CENTER)
        panel.add(createMarketplaceButtonsPanel(), BorderLayout.SOUTH)
        return panel
    }

    private fun createButtonsPanel(): JPanel {
        val panel = JPanel()
        val newButton = JButton("New")
        val editButton = JButton("Edit")
        val deleteButton = JButton("Delete")
        val exportButton = JButton("Export")
        val importButton = JButton("Import")
        val shareButton = JButton("Share")

        newButton.addActionListener { createNewTemplate() }
        editButton.addActionListener { editSelectedTemplate() }
        deleteButton.addActionListener { deleteSelectedTemplate() }
        exportButton.addActionListener { exportTemplates() }
        importButton.addActionListener { importTemplates() }
        shareButton.addActionListener { shareSelectedTemplate() }

        panel.add(newButton)
        panel.add(editButton)
        panel.add(deleteButton)
        panel.add(exportButton)
        panel.add(importButton)
        panel.add(shareButton)

        return panel
    }

    private fun createVersionButtonsPanel(): JPanel {
        val panel = JPanel()
        val viewButton = JButton("View Version")
        val restoreButton = JButton("Restore Version")
        val compareButton = JButton("Compare Versions")

        viewButton.addActionListener { viewSelectedVersion() }
        restoreButton.addActionListener { restoreSelectedVersion() }
        compareButton.addActionListener { compareVersions() }

        panel.add(viewButton)
        panel.add(restoreButton)
        panel.add(compareButton)

        return panel
    }

    private fun createSharedButtonsPanel(): JPanel {
        val panel = JPanel()
        val downloadButton = JButton("Download")
        val reviewButton = JButton("Review")
        val updateButton = JButton("Update")

        downloadButton.addActionListener { downloadSelectedTemplate() }
        reviewButton.addActionListener { reviewSelectedTemplate() }
        updateButton.addActionListener { updateSharedTemplate() }

        panel.add(downloadButton)
        panel.add(reviewButton)
        panel.add(updateButton)

        return panel
    }

    private fun createMarketplaceButtonsPanel(): JPanel {
        val panel = JPanel()
        val searchButton = JButton("Search")
        val filterButton = JButton("Filter")
        val sortButton = JButton("Sort")

        searchButton.addActionListener { searchTemplates() }
        filterButton.addActionListener { filterTemplates() }
        sortButton.addActionListener { sortTemplates() }

        panel.add(searchButton)
        panel.add(filterButton)
        panel.add(sortButton)

        return panel
    }

    private fun loadTemplate(template: PromptTemplate.Template) {
        nameField.text = template.name
        descriptionField.text = template.description
        contentArea.text = template.content
        categoryField.text = template.category
        variablesField.text = template.variables.joinToString(",")
        tagsField.text = template.tags.joinToString(",")
        authorField.text = template.author
        isPublicCheckbox.isSelected = template.isPublic
        updateVersionsTable(template)
    }

    private fun updateTemplatesTable() {
        val model = templatesTable.model as DefaultTableModel
        model.rowCount = 0
        templateManager.templates.values.forEach { template ->
            model.addRow(arrayOf(
                template.name,
                template.description,
                template.category,
                template.author,
                template.lastUsed?.toString() ?: "Never"
            ))
        }
    }

    private fun updateVersionsTable(template: PromptTemplate.Template) {
        val model = versionsTable.model as DefaultTableModel
        model.rowCount = 0
        template.versions.forEach { version ->
            model.addRow(arrayOf(
                version.number,
                version.description,
                version.createdBy,
                version.createdAt.toString()
            ))
        }
    }

    private fun updateSharedTemplatesTable() {
        val model = sharedTemplatesTable.model as DefaultTableModel
        model.rowCount = 0
        templateManager.sharedTemplates.values.forEach { sharedTemplate ->
            model.addRow(arrayOf(
                sharedTemplate.template.name,
                sharedTemplate.sharedBy,
                String.format("%.1f", sharedTemplate.rating),
                sharedTemplate.downloadCount
            ))
        }
    }

    private fun createNewTemplate() {
        val template = PromptTemplate.Template(
            name = nameField.text,
            description = descriptionField.text,
            content = contentArea.text,
            category = categoryField.text,
            variables = variablesField.text.split(",").map { it.trim() }.toMutableList(),
            tags = tagsField.text.split(",").map { it.trim() }.toMutableSet(),
            author = authorField.text,
            isPublic = isPublicCheckbox.isSelected
        )
        templateManager.addTemplate(template)
        updateTemplatesTable()
    }

    private fun editSelectedTemplate() {
        val selectedRow = templatesTable.selectedRow
        if (selectedRow >= 0) {
            val templateName = templatesTable.getValueAt(selectedRow, 0) as String
            val template = templateManager.getTemplate(templateName)
            if (template != null) {
                loadTemplate(template)
            }
        }
    }

    private fun deleteSelectedTemplate() {
        val selectedRow = templatesTable.selectedRow
        if (selectedRow >= 0) {
            val templateName = templatesTable.getValueAt(selectedRow, 0) as String
            templateManager.removeTemplate(templateName)
            updateTemplatesTable()
        }
    }

    private fun shareSelectedTemplate() {
        val selectedRow = templatesTable.selectedRow
        if (selectedRow >= 0) {
            val templateName = templatesTable.getValueAt(selectedRow, 0) as String
            templateManager.shareTemplate(templateName, isPublicCheckbox.isSelected)
            updateSharedTemplatesTable()
        }
    }

    private fun viewSelectedVersion() {
        val selectedRow = versionsTable.selectedRow
        if (selectedRow >= 0) {
            val versionNumber = versionsTable.getValueAt(selectedRow, 0) as Int
            val template = templateManager.getTemplate(nameField.text)
            val version = template?.versions?.find { it.number == versionNumber }
            if (version != null) {
                contentArea.text = version.content
            }
        }
    }

    private fun restoreSelectedVersion() {
        val selectedRow = versionsTable.selectedRow
        if (selectedRow >= 0) {
            val versionNumber = versionsTable.getValueAt(selectedRow, 0) as Int
            val template = templateManager.getTemplate(nameField.text)
            val version = template?.versions?.find { it.number == versionNumber }
            if (version != null) {
                contentArea.text = version.content
                // Create new version with restored content
                val newVersion = PromptTemplate.Version(
                    number = template.versions.size + 1,
                    content = version.content,
                    description = "Restored from version $versionNumber",
                    createdAt = Date(),
                    createdBy = template.author
                )
                template.versions.add(newVersion)
                templateManager.updateTemplate(template.name, template)
                updateVersionsTable(template)
            }
        }
    }

    private fun compareVersions() {
        val selectedRows = versionsTable.selectedRows
        if (selectedRows.size == 2) {
            val version1 = versionsTable.getValueAt(selectedRows[0], 0) as Int
            val version2 = versionsTable.getValueAt(selectedRows[1], 0) as Int
            val template = templateManager.getTemplate(nameField.text)
            val v1 = template?.versions?.find { it.number == version1 }
            val v2 = template?.versions?.find { it.number == version2 }
            if (v1 != null && v2 != null) {
                showDiffDialog(v1.content, v2.content)
            }
        }
    }

    private fun showDiffDialog(content1: String, content2: String) {
        val dialog = JDialog(owner, "Version Comparison", true)
        val diffPanel = JPanel(BorderLayout())
        val textArea1 = JTextArea(content1)
        val textArea2 = JTextArea(content2)
        val scrollPane1 = JBScrollPane(textArea1)
        val scrollPane2 = JBScrollPane(textArea2)
        diffPanel.add(scrollPane1, BorderLayout.WEST)
        diffPanel.add(scrollPane2, BorderLayout.EAST)
        dialog.contentPane = diffPanel
        dialog.setSize(800, 600)
        dialog.setLocationRelativeTo(owner)
        dialog.isVisible = true
    }

    private fun downloadSelectedTemplate() {
        val selectedRow = sharedTemplatesTable.selectedRow
        if (selectedRow >= 0) {
            val templateId = sharedTemplatesTable.getValueAt(selectedRow, 0) as String
            val template = templateManager.downloadSharedTemplate(templateId)
            if (template != null) {
                loadTemplate(template)
                updateTemplatesTable()
            }
        }
    }

    private fun reviewSelectedTemplate() {
        val selectedRow = sharedTemplatesTable.selectedRow
        if (selectedRow >= 0) {
            val templateId = sharedTemplatesTable.getValueAt(selectedRow, 0) as String
            showReviewDialog(templateId)
        }
    }

    private fun showReviewDialog(templateId: String) {
        val dialog = JDialog(owner, "Review Template", true)
        val panel = JPanel(BorderLayout())
        val ratingField = JSpinner(SpinnerNumberModel(5, 1, 5, 1))
        val commentArea = JTextArea()
        val submitButton = JButton("Submit")

        submitButton.addActionListener {
            val review = PromptTemplate.Review(
                rating = ratingField.value as Int,
                comment = commentArea.text,
                reviewer = authorField.text
            )
            templateManager.addReview(templateId, review)
            updateSharedTemplatesTable()
            dialog.dispose()
        }

        panel.add(JLabel("Rating:"), BorderLayout.NORTH)
        panel.add(ratingField, BorderLayout.CENTER)
        panel.add(JScrollPane(commentArea), BorderLayout.CENTER)
        panel.add(submitButton, BorderLayout.SOUTH)

        dialog.contentPane = panel
        dialog.setSize(400, 300)
        dialog.setLocationRelativeTo(owner)
        dialog.isVisible = true
    }

    private fun updateSharedTemplate() {
        val selectedRow = sharedTemplatesTable.selectedRow
        if (selectedRow >= 0) {
            val templateId = sharedTemplatesTable.getValueAt(selectedRow, 0) as String
            val template = templateManager.getTemplate(nameField.text)
            if (template != null) {
                templateManager.shareTemplate(template.name, isPublicCheckbox.isSelected)
                updateSharedTemplatesTable()
            }
        }
    }

    private fun searchTemplates() {
        val dialog = JDialog(owner, "Search Templates", true)
        val panel = JPanel(BorderLayout())
        val searchField = JTextField()
        val searchButton = JButton("Search")

        searchButton.addActionListener {
            val query = searchField.text
            // Implement search logic
            dialog.dispose()
        }

        panel.add(searchField, BorderLayout.CENTER)
        panel.add(searchButton, BorderLayout.SOUTH)

        dialog.contentPane = panel
        dialog.setSize(300, 100)
        dialog.setLocationRelativeTo(owner)
        dialog.isVisible = true
    }

    private fun filterTemplates() {
        val dialog = JDialog(owner, "Filter Templates", true)
        val panel = JPanel(BorderLayout())
        val categoryField = JTextField()
        val tagField = JTextField()
        val authorField = JTextField()
        val filterButton = JButton("Filter")

        filterButton.addActionListener {
            // Implement filter logic
            dialog.dispose()
        }

        panel.add(JLabel("Category:"), BorderLayout.NORTH)
        panel.add(categoryField, BorderLayout.NORTH)
        panel.add(JLabel("Tag:"), BorderLayout.CENTER)
        panel.add(tagField, BorderLayout.CENTER)
        panel.add(JLabel("Author:"), BorderLayout.CENTER)
        panel.add(authorField, BorderLayout.CENTER)
        panel.add(filterButton, BorderLayout.SOUTH)

        dialog.contentPane = panel
        dialog.setSize(300, 200)
        dialog.setLocationRelativeTo(owner)
        dialog.isVisible = true
    }

    private fun sortTemplates() {
        val options = arrayOf("Name", "Rating", "Downloads", "Date")
        val choice = JOptionPane.showInputDialog(
            owner,
            "Sort by:",
            "Sort Templates",
            JOptionPane.QUESTION_MESSAGE,
            null,
            options,
            options[0]
        )
        if (choice != null) {
            // Implement sort logic
        }
    }

    private fun exportTemplates() {
        val json = templateManager.exportTemplates()
        val dialog = JDialog(owner, "Export Templates", true)
        val textArea = JTextArea(json)
        textArea.isEditable = false
        val scrollPane = JBScrollPane(textArea)
        dialog.contentPane = scrollPane
        dialog.setSize(400, 300)
        dialog.setLocationRelativeTo(owner)
        dialog.isVisible = true
    }

    private fun importTemplates() {
        val dialog = JDialog(owner, "Import Templates", true)
        val textArea = JTextArea()
        val scrollPane = JBScrollPane(textArea)
        val importButton = JButton("Import")
        importButton.addActionListener {
            try {
                templateManager.importTemplates(textArea.text)
                updateTemplatesTable()
                dialog.dispose()
            } catch (e: Exception) {
                JOptionPane.showMessageDialog(
                    dialog,
                    "Error importing templates: ${e.message}",
                    "Import Error",
                    JOptionPane.ERROR_MESSAGE
                )
            }
        }
        dialog.contentPane = JPanel(BorderLayout()).apply {
            add(scrollPane, BorderLayout.CENTER)
            add(importButton, BorderLayout.SOUTH)
        }
        dialog.setSize(400, 300)
        dialog.setLocationRelativeTo(owner)
        dialog.isVisible = true
    }

    override fun doOKAction() {
        if (template != null) {
            val updatedTemplate = PromptTemplate.Template(
                name = nameField.text,
                description = descriptionField.text,
                content = contentArea.text,
                category = categoryField.text,
                variables = variablesField.text.split(",").map { it.trim() }.toMutableList(),
                tags = tagsField.text.split(",").map { it.trim() }.toMutableSet(),
                author = authorField.text,
                isPublic = isPublicCheckbox.isSelected,
                createdAt = template.createdAt,
                updatedAt = Date()
            )
            templateManager.updateTemplate(template.name, updatedTemplate)
        } else {
            createNewTemplate()
        }
        super.doOKAction()
    }
} 