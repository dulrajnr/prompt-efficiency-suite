package com.prompt.efficiency.collab.ui

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.DialogWrapper
import com.intellij.ui.components.JBScrollPane
import com.prompt.efficiency.collab.TeamPatternManager
import com.prompt.efficiency.settings.PromptEfficiencySettings
import java.awt.BorderLayout
import java.awt.FlowLayout
import javax.swing.*
import java.util.*

class TeamPatternDialog(
    private val project: Project,
    private val existingPattern: TeamPatternManager.TeamPattern? = null
) : DialogWrapper(project) {
    private val nameField = JTextField()
    private val descriptionField = JTextArea()
    private val templateField = JTextArea()
    private val categoryField = JTextField()
    private val modelCombo = JComboBox<String>()
    private val tagsField = JTextField()

    init {
        title = if (existingPattern == null) "Add Team Pattern" else "Edit Team Pattern"
        init()
        setupUI()
        if (existingPattern != null) {
            loadPattern(existingPattern)
        }
    }

    private fun setupUI() {
        // Create form panel
        val formPanel = JPanel(BorderLayout()).apply {
            border = BorderFactory.createEmptyBorder(10, 10, 10, 10)
        }

        // Create fields panel
        val fieldsPanel = JPanel(BorderLayout()).apply {
            add(createFieldPanel(), BorderLayout.NORTH)
            add(createTemplatePanel(), BorderLayout.CENTER)
        }

        // Add to form panel
        formPanel.add(fieldsPanel, BorderLayout.CENTER)

        // Set content pane
        setContentPane(formPanel)
    }

    private fun createFieldPanel(): JPanel {
        return JPanel(BorderLayout()).apply {
            val panel = JPanel(FlowLayout(FlowLayout.LEFT))
            panel.layout = BoxLayout(panel, BoxLayout.Y_AXIS)

            // Name field
            panel.add(createLabeledField("Name:", nameField))

            // Description field
            descriptionField.rows = 3
            panel.add(createLabeledField("Description:", JBScrollPane(descriptionField)))

            // Category field
            panel.add(createLabeledField("Category:", categoryField))

            // Model combo
            modelCombo.apply {
                PromptEfficiencySettings.getInstance(project).getModelSettings().forEach {
                    addItem(it.model)
                }
            }
            panel.add(createLabeledField("Model:", modelCombo))

            // Tags field
            panel.add(createLabeledField("Tags (comma-separated):", tagsField))

            add(panel, BorderLayout.CENTER)
        }
    }

    private fun createTemplatePanel(): JPanel {
        return JPanel(BorderLayout()).apply {
            templateField.rows = 10
            add(createLabeledField("Template:", JBScrollPane(templateField)), BorderLayout.CENTER)
        }
    }

    private fun createLabeledField(label: String, field: JComponent): JPanel {
        return JPanel(FlowLayout(FlowLayout.LEFT)).apply {
            add(JLabel(label))
            add(field)
        }
    }

    private fun loadPattern(pattern: TeamPatternManager.TeamPattern) {
        nameField.text = pattern.name
        descriptionField.text = pattern.description
        templateField.text = pattern.template
        categoryField.text = pattern.category
        modelCombo.selectedItem = pattern.model
        tagsField.text = pattern.tags.joinToString(",")
    }

    fun getPattern(): TeamPatternManager.TeamPattern {
        val tags = tagsField.text.split(",")
            .map { it.trim() }
            .filter { it.isNotEmpty() }
            .toSet()

        return TeamPatternManager.TeamPattern(
            id = existingPattern?.id ?: UUID.randomUUID().toString(),
            name = nameField.text,
            description = descriptionField.text,
            template = templateField.text,
            category = categoryField.text,
            model = modelCombo.selectedItem as String,
            tags = tags,
            author = existingPattern?.author ?: "Current User", // TODO: Get actual user
            status = existingPattern?.status ?: TeamPatternManager.PatternStatus.DRAFT,
            version = existingPattern?.version ?: 1,
            usageCount = existingPattern?.usageCount ?: 0,
            successRate = existingPattern?.successRate ?: 0.0,
            reviews = existingPattern?.reviews ?: mutableListOf()
        )
    }

    override fun doValidate(): ValidationInfo? {
        if (nameField.text.isBlank()) {
            return ValidationInfo("Name is required", nameField)
        }
        if (descriptionField.text.isBlank()) {
            return ValidationInfo("Description is required", descriptionField)
        }
        if (templateField.text.isBlank()) {
            return ValidationInfo("Template is required", templateField)
        }
        if (categoryField.text.isBlank()) {
            return ValidationInfo("Category is required", categoryField)
        }
        if (modelCombo.selectedItem == null) {
            return ValidationInfo("Model is required", modelCombo)
        }
        return null
    }
} 