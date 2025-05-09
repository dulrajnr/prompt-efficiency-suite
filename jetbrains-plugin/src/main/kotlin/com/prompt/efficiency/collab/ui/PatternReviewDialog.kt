package com.prompt.efficiency.collab.ui

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.DialogWrapper
import com.intellij.ui.components.JBScrollPane
import com.prompt.efficiency.collab.TeamPatternManager
import java.awt.BorderLayout
import java.awt.FlowLayout
import javax.swing.*
import java.util.*

class PatternReviewDialog(
    private val project: Project,
    private val pattern: TeamPatternManager.TeamPattern
) : DialogWrapper(project) {
    private val statusCombo = JComboBox<TeamPatternManager.ReviewStatus>()
    private val commentsField = JTextArea()

    init {
        title = "Review Pattern: ${pattern.name}"
        init()
        setupUI()
    }

    private fun setupUI() {
        // Create form panel
        val formPanel = JPanel(BorderLayout()).apply {
            border = BorderFactory.createEmptyBorder(10, 10, 10, 10)
        }

        // Create pattern info panel
        val infoPanel = createPatternInfoPanel()
        formPanel.add(infoPanel, BorderLayout.NORTH)

        // Create review panel
        val reviewPanel = createReviewPanel()
        formPanel.add(reviewPanel, BorderLayout.CENTER)

        // Set content pane
        setContentPane(formPanel)
    }

    private fun createPatternInfoPanel(): JPanel {
        return JPanel(BorderLayout()).apply {
            val panel = JPanel(FlowLayout(FlowLayout.LEFT))
            panel.layout = BoxLayout(panel, BoxLayout.Y_AXIS)

            // Pattern details
            panel.add(JLabel("Pattern Details:"))
            panel.add(JLabel("Name: ${pattern.name}"))
            panel.add(JLabel("Category: ${pattern.category}"))
            panel.add(JLabel("Model: ${pattern.model}"))
            panel.add(JLabel("Author: ${pattern.author}"))
            panel.add(JLabel("Version: ${pattern.version}"))
            panel.add(JLabel("Usage Count: ${pattern.usageCount}"))
            panel.add(JLabel("Success Rate: ${String.format("%.1f%%", pattern.successRate * 100)}"))

            // Pattern template
            val templateArea = JTextArea(pattern.template)
            templateArea.rows = 5
            templateArea.isEditable = false
            panel.add(JLabel("Template:"))
            panel.add(JBScrollPane(templateArea))

            add(panel, BorderLayout.CENTER)
        }
    }

    private fun createReviewPanel(): JPanel {
        return JPanel(BorderLayout()).apply {
            val panel = JPanel(FlowLayout(FlowLayout.LEFT))
            panel.layout = BoxLayout(panel, BoxLayout.Y_AXIS)

            // Status combo
            statusCombo.apply {
                TeamPatternManager.ReviewStatus.values().forEach { addItem(it) }
                selectedItem = TeamPatternManager.ReviewStatus.PENDING
            }
            panel.add(createLabeledField("Status:", statusCombo))

            // Comments field
            commentsField.rows = 5
            panel.add(createLabeledField("Comments:", JBScrollPane(commentsField)))

            add(panel, BorderLayout.CENTER)
        }
    }

    private fun createLabeledField(label: String, field: JComponent): JPanel {
        return JPanel(FlowLayout(FlowLayout.LEFT)).apply {
            add(JLabel(label))
            add(field)
        }
    }

    fun getReview(): TeamPatternManager.PatternReview {
        return TeamPatternManager.PatternReview(
            id = UUID.randomUUID().toString(),
            patternId = pattern.id,
            reviewerId = "Current User", // TODO: Get actual user
            status = statusCombo.selectedItem as TeamPatternManager.ReviewStatus,
            comments = commentsField.text,
            createdAt = Date()
        )
    }

    override fun doValidate(): ValidationInfo? {
        if (commentsField.text.isBlank()) {
            return ValidationInfo("Comments are required", commentsField)
        }
        return null
    }
} 