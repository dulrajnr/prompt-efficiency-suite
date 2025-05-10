package com.prompt.efficiency.collab.ui

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.DialogWrapper
import com.intellij.openapi.ui.ValidationInfo
import com.intellij.ui.components.JBScrollPane
import com.prompt.efficiency.collab.TeamPatternManager
import com.prompt.efficiency.collab.model.PatternReview
import com.prompt.efficiency.collab.model.ReviewStatus
import java.awt.BorderLayout
import java.awt.Dimension
import java.time.LocalDateTime
import java.util.*
import javax.swing.*

class PatternReviewDialog(
    private val project: Project,
    private val patternManager: TeamPatternManager,
    private val patternId: String
) : DialogWrapper(project) {

    private val statusCombo = JComboBox(ReviewStatus.values())
    private val commentsField = JTextArea(5, 40)

    init {
        title = "Review Pattern: ${patternManager.getPattern(patternId)?.name ?: patternId}"
        init()
    }

    override fun createCenterPanel(): JComponent {
        val panel = JPanel(BorderLayout())
        panel.add(createPatternInfoPanel(), BorderLayout.NORTH)
        panel.add(createReviewPanel(), BorderLayout.CENTER)
        return panel
    }

    private fun createPatternInfoPanel(): JComponent {
        val pattern = patternManager.getPattern(patternId) ?: return JPanel()
        val panel = JPanel(BorderLayout())

        val infoPanel = JPanel()
        infoPanel.layout = BoxLayout(infoPanel, BoxLayout.Y_AXIS)

        infoPanel.add(JLabel("Name: ${pattern.name}"))
        infoPanel.add(JLabel("Category: ${pattern.category}"))
        infoPanel.add(JLabel("Model: ${pattern.model}"))
        infoPanel.add(JLabel("Author: ${pattern.author}"))
        infoPanel.add(JLabel("Version: ${pattern.version}"))
        infoPanel.add(JLabel("Usage Count: ${pattern.usageCount}"))
        infoPanel.add(JLabel("Success Rate: ${pattern.successRate}%"))

        val templateArea = JTextArea(pattern.template)
        templateArea.isEditable = false
        templateArea.lineWrap = true
        templateArea.wrapStyleWord = true

        val scrollPane = JBScrollPane(templateArea)
        scrollPane.preferredSize = Dimension(400, 200)

        panel.add(infoPanel, BorderLayout.NORTH)
        panel.add(scrollPane, BorderLayout.CENTER)

        return panel
    }

    private fun createReviewPanel(): JComponent {
        val panel = JPanel(BorderLayout())

        val formPanel = JPanel()
        formPanel.layout = BoxLayout(formPanel, BoxLayout.Y_AXIS)

        val statusLabel = JLabel("Review Status:")
        statusCombo.selectedItem = ReviewStatus.PENDING

        val commentsLabel = JLabel("Comments:")
        commentsField.lineWrap = true
        commentsField.wrapStyleWord = true

        val commentsScroll = JBScrollPane(commentsField)
        commentsScroll.preferredSize = Dimension(400, 100)

        formPanel.add(statusLabel)
        formPanel.add(statusCombo)
        formPanel.add(Box.createVerticalStrut(10))
        formPanel.add(commentsLabel)
        formPanel.add(commentsScroll)

        panel.add(formPanel, BorderLayout.CENTER)
        return panel
    }

    fun getReview(): PatternReview {
        return PatternReview(
            id = UUID.randomUUID().toString(),
            patternId = patternId,
            reviewerId = patternManager.getCurrentUserId(),
            status = statusCombo.selectedItem as ReviewStatus,
            comments = commentsField.text,
            date = LocalDateTime.now()
        )
    }

    override fun doValidate(): ValidationInfo? {
        if (commentsField.text.isBlank()) {
            return ValidationInfo("Please provide comments for the review")
        }
        return null
    }
}
