package com.prompt.efficiency.collab.ui

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.DialogWrapper
import com.intellij.ui.components.JBScrollPane
import com.prompt.efficiency.collab.TeamPatternManager
import com.prompt.efficiency.collab.model.TeamPattern
import java.awt.BorderLayout
import java.awt.Dimension
import javax.swing.*
import javax.swing.table.DefaultTableModel

class TeamPatternManagementDialog(
    private val project: Project,
    private val patternManager: TeamPatternManager
) : DialogWrapper(project) {

    private val tableModel = DefaultTableModel(
        arrayOf("Name", "Category", "Model", "Author", "Version", "Usage", "Success Rate"),
        0
    )
    private val table = JTable(tableModel)
    private var selectedPattern: TeamPattern? = null

    init {
        title = "Team Pattern Management"
        init()
        setupUI()
        loadPatterns()
    }

    override fun createCenterPanel(): JComponent {
        val panel = JPanel(BorderLayout())

        // Table setup
        table.selectionModel.addListSelectionListener {
            if (!it.valueIsAdjusting) {
                val selectedRow = table.selectedRow
                if (selectedRow >= 0) {
                    val patternName = table.getValueAt(selectedRow, 0) as String
                    selectedPattern = patternManager.getPatterns().find { it.name == patternName }
                } else {
                    selectedPattern = null
                }
            }
        }

        val scrollPane = JBScrollPane(table)
        scrollPane.preferredSize = Dimension(800, 400)

        // Button panel
        val buttonPanel = JPanel()
        val addButton = JButton("Add")
        val editButton = JButton("Edit")
        val deleteButton = JButton("Delete")
        val reviewButton = JButton("Review")

        addButton.addActionListener { addPattern() }
        editButton.addActionListener { editPattern() }
        deleteButton.addActionListener { deletePattern() }
        reviewButton.addActionListener { reviewPattern() }

        buttonPanel.add(addButton)
        buttonPanel.add(editButton)
        buttonPanel.add(deleteButton)
        buttonPanel.add(reviewButton)

        panel.add(scrollPane, BorderLayout.CENTER)
        panel.add(buttonPanel, BorderLayout.SOUTH)

        return panel
    }

    private fun setupUI() {
        table.model = object : DefaultTableModel(
            arrayOf("Name", "Category", "Model", "Author", "Version", "Usage", "Success Rate"),
            0
        ) {
            override fun isCellEditable(row: Int, column: Int): Boolean = false
        }
    }

    private fun loadPatterns() {
        tableModel.rowCount = 0
        patternManager.getPatterns().forEach { pattern ->
            tableModel.addRow(arrayOf(
                pattern.name,
                pattern.category,
                pattern.model,
                pattern.author,
                pattern.version.toString(),
                pattern.usageCount.toString(),
                "${pattern.successRate}%"
            ))
        }
    }

    private fun addPattern() {
        val dialog = TeamPatternDialog(project, patternManager)
        if (dialog.showAndGet()) {
            val pattern = dialog.getPattern()
            patternManager.addPattern(pattern)
            loadPatterns()
        }
    }

    private fun editPattern() {
        val pattern = selectedPattern ?: return
        val dialog = TeamPatternDialog(project, patternManager, pattern)
        if (dialog.showAndGet()) {
            val updatedPattern = dialog.getPattern()
            patternManager.updatePattern(updatedPattern)
            loadPatterns()
        }
    }

    private fun deletePattern() {
        val pattern = selectedPattern ?: return
        val result = JOptionPane.showConfirmDialog(
            this,
            "Are you sure you want to delete pattern '${pattern.name}'?",
            "Confirm Delete",
            JOptionPane.YES_NO_OPTION
        )
        if (result == JOptionPane.YES_OPTION) {
            patternManager.deletePattern(pattern.id)
            loadPatterns()
        }
    }

    private fun reviewPattern() {
        val pattern = selectedPattern ?: return
        val dialog = PatternReviewDialog(project, patternManager, pattern.id)
        if (dialog.showAndGet()) {
            val review = dialog.getReview()
            patternManager.addReview(review)
        }
    }
}
