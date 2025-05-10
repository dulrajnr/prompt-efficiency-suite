package com.prompt.efficiency.collab.ui

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.DialogWrapper
import com.intellij.openapi.ui.ValidationInfo
import com.intellij.ui.components.JBScrollPane
import com.prompt.efficiency.collab.TeamPatternManager
import com.prompt.efficiency.collab.model.TeamPattern
import com.prompt.efficiency.settings.PromptEfficiencySettings
import java.awt.BorderLayout
import java.awt.Dimension
import java.util.*
import javax.swing.*

class TeamPatternDialog(
    private val project: Project,
    private val patternManager: TeamPatternManager,
    private val pattern: TeamPattern? = null
) : DialogWrapper(project) {

    private val nameField = JTextField()
    private val categoryField = JTextField()
    private val modelCombo = JComboBox<String>()
    private val templateArea = JTextArea(10, 40)
    private val descriptionArea = JTextArea(3, 40)

    init {
        title = if (pattern == null) "Add Team Pattern" else "Edit Team Pattern"
        init()
        setupUI()
    }

    override fun createCenterPanel(): JComponent {
        val panel = JPanel(BorderLayout())
        panel.add(createFormPanel(), BorderLayout.CENTER)
        return panel
    }

    private fun setupUI() {
        val settings = PromptEfficiencySettings.getInstance()
        val models = settings.getModelSettings().keys.toTypedArray()
        modelCombo.model = DefaultComboBoxModel(models)

        pattern?.let {
            nameField.text = it.name
            categoryField.text = it.category
            modelCombo.selectedItem = it.model
            templateArea.text = it.template
            descriptionArea.text = it.description
        }
    }

    private fun createFormPanel(): JComponent {
        val panel = JPanel(BorderLayout())

        val formPanel = JPanel()
        formPanel.layout = BoxLayout(formPanel, BoxLayout.Y_AXIS)

        // Name field
        val nameLabel = JLabel("Name:")
        nameField.maximumSize = Dimension(400, nameField.preferredSize.height)

        // Category field
        val categoryLabel = JLabel("Category:")
        categoryField.maximumSize = Dimension(400, categoryField.preferredSize.height)

        // Model combo
        val modelLabel = JLabel("Model:")
        modelCombo.maximumSize = Dimension(400, modelCombo.preferredSize.height)

        // Template area
        val templateLabel = JLabel("Template:")
        templateArea.lineWrap = true
        templateArea.wrapStyleWord = true
        val templateScroll = JBScrollPane(templateArea)
        templateScroll.preferredSize = Dimension(400, 200)

        // Description area
        val descriptionLabel = JLabel("Description:")
        descriptionArea.lineWrap = true
        descriptionArea.wrapStyleWord = true
        val descriptionScroll = JBScrollPane(descriptionArea)
        descriptionScroll.preferredSize = Dimension(400, 100)

        // Add components to form
        formPanel.add(nameLabel)
        formPanel.add(nameField)
        formPanel.add(Box.createVerticalStrut(10))

        formPanel.add(categoryLabel)
        formPanel.add(categoryField)
        formPanel.add(Box.createVerticalStrut(10))

        formPanel.add(modelLabel)
        formPanel.add(modelCombo)
        formPanel.add(Box.createVerticalStrut(10))

        formPanel.add(templateLabel)
        formPanel.add(templateScroll)
        formPanel.add(Box.createVerticalStrut(10))

        formPanel.add(descriptionLabel)
        formPanel.add(descriptionScroll)

        panel.add(formPanel, BorderLayout.CENTER)
        return panel
    }

    fun getPattern(): TeamPattern {
        val id = pattern?.id ?: UUID.randomUUID().toString()
        return TeamPattern(
            id = id,
            name = nameField.text,
            category = categoryField.text,
            model = modelCombo.selectedItem as String,
            template = templateArea.text,
            description = descriptionArea.text,
            author = patternManager.getCurrentUserId(),
            version = pattern?.version ?: 1,
            usageCount = pattern?.usageCount ?: 0,
            successRate = pattern?.successRate ?: 0.0
        )
    }

    override fun doValidate(): ValidationInfo? {
        if (nameField.text.isBlank()) {
            return ValidationInfo("Name is required")
        }
        if (categoryField.text.isBlank()) {
            return ValidationInfo("Category is required")
        }
        if (modelCombo.selectedItem == null) {
            return ValidationInfo("Model is required")
        }
        if (templateArea.text.isBlank()) {
            return ValidationInfo("Template is required")
        }
        return null
    }
}
