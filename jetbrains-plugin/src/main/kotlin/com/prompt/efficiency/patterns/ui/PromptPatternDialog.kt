package com.prompt.efficiency.patterns.ui

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.DialogWrapper
import com.intellij.ui.components.JBScrollPane
import com.prompt.efficiency.patterns.PromptPatternLibrary
import java.awt.BorderLayout
import java.awt.Dimension
import java.awt.FlowLayout
import javax.swing.*
import java.util.UUID

class PromptPatternDialog(
    private val project: Project,
    private val existingPattern: PromptPatternLibrary.PromptPattern? = null
) : DialogWrapper(project) {
    private val patternLibrary = PromptPatternLibrary.getInstance(project)
    private val nameField = JTextField()
    private val descriptionField = JTextField()
    private val templateField = JTextArea()
    private val categoryCombo = JComboBox<String>()
    private val modelCombo = JComboBox<String>()
    private val tagsField = JTextField()

    init {
        title = if (existingPattern == null) "Add Pattern" else "Edit Pattern"
        init()
        setupUI()
        if (existingPattern != null) {
            loadPattern(existingPattern)
        }
    }

    private fun setupUI() {
        // Create form panel
        val formPanel = JPanel().apply {
            layout = BoxLayout(this, BoxLayout.Y_AXIS)
            border = BorderFactory.createEmptyBorder(10, 10, 10, 10)

            // Name field
            add(createFormField("Name:", nameField))
            add(Box.createVerticalStrut(10))

            // Description field
            add(createFormField("Description:", descriptionField))
            add(Box.createVerticalStrut(10))

            // Template field
            add(JLabel("Template:"))
            add(Box.createVerticalStrut(5))
            add(JBScrollPane(templateField).apply {
                preferredSize = Dimension(400, 100)
            })
            add(Box.createVerticalStrut(10))

            // Category combo
            add(createFormField("Category:", categoryCombo))
            add(Box.createVerticalStrut(10))

            // Model combo
            add(createFormField("Model:", modelCombo))
            add(Box.createVerticalStrut(10))

            // Tags field
            add(createFormField("Tags (comma-separated):", tagsField))
        }

        // Setup category combo
        categoryCombo.apply {
            patternLibrary.state.categories.forEach { addItem(it) }
            isEditable = true
        }

        // Setup model combo
        modelCombo.apply {
            addItem("gpt-4")
            addItem("gpt-3.5-turbo")
            addItem("general")
        }

        // Add components to main panel
        contentPanel.apply {
            layout = BorderLayout()
            add(formPanel, BorderLayout.CENTER)
            preferredSize = Dimension(500, 400)
        }
    }

    private fun createFormField(label: String, component: JComponent): JPanel {
        return JPanel(FlowLayout(FlowLayout.LEFT)).apply {
            add(JLabel(label))
            add(component)
        }
    }

    private fun loadPattern(pattern: PromptPatternLibrary.PromptPattern) {
        nameField.text = pattern.name
        descriptionField.text = pattern.description
        templateField.text = pattern.template
        categoryCombo.selectedItem = pattern.category
        modelCombo.selectedItem = pattern.model
        tagsField.text = pattern.tags.joinToString(", ")
    }

    fun getPattern(): PromptPatternLibrary.PromptPattern {
        val id = existingPattern?.id ?: UUID.randomUUID().toString()
        val tags = tagsField.text.split(",")
            .map { it.trim() }
            .filter { it.isNotEmpty() }
            .toMutableSet()

        return PromptPatternLibrary.PromptPattern(
            id = id,
            name = nameField.text,
            description = descriptionField.text,
            template = templateField.text,
            category = categoryCombo.selectedItem.toString(),
            model = modelCombo.selectedItem.toString(),
            tags = tags,
            usageCount = existingPattern?.usageCount ?: 0,
            successRate = existingPattern?.successRate ?: 0.0,
            lastUsed = existingPattern?.lastUsed ?: 0
        )
    }

    override fun doOKAction() {
        if (validateInput()) {
            super.doOKAction()
        }
    }

    private fun validateInput(): Boolean {
        if (nameField.text.isBlank()) {
            showError("Name is required")
            return false
        }
        if (templateField.text.isBlank()) {
            showError("Template is required")
            return false
        }
        if (categoryCombo.selectedItem == null) {
            showError("Category is required")
            return false
        }
        if (modelCombo.selectedItem == null) {
            showError("Model is required")
            return false
        }
        return true
    }

    private fun showError(message: String) {
        JOptionPane.showMessageDialog(
            this,
            message,
            "Validation Error",
            JOptionPane.ERROR_MESSAGE
        )
    }
}
