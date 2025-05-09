package com.prompt.efficiency.collab.ui

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.DialogWrapper
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.table.JBTable
import com.intellij.util.ui.JBUI
import com.prompt.efficiency.collab.TeamPatternManager
import java.awt.BorderLayout
import java.awt.Dimension
import java.awt.FlowLayout
import javax.swing.*
import javax.swing.table.DefaultTableModel
import java.time.format.DateTimeFormatter

class TeamPatternManagementDialog(
    private val project: Project
) : DialogWrapper(project) {
    private val teamPatternManager = TeamPatternManager.getInstance(project)
    private val patternTable = JBTable()
    private val reviewTable = JBTable()
    private val statusCombo = JComboBox<TeamPatternManager.PatternStatus>()
    private val categoryCombo = JComboBox<String>()
    private val modelCombo = JComboBox<String>()
    private val authorCombo = JComboBox<String>()

    init {
        title = "Team Pattern Management"
        init()
        setupUI()
        loadData()
    }

    private fun setupUI() {
        // Create toolbar
        val toolbar = JToolBar().apply {
            isFloatable = false
            add(createButton("Add Pattern", "add") { showAddPatternDialog() })
            add(createButton("Edit Pattern", "edit") { showEditPatternDialog() })
            add(createButton("Delete Pattern", "delete") { deleteSelectedPattern() })
            add(createButton("Submit for Review", "review") { submitForReview() })
            add(createButton("Sync with Library", "sync") { syncWithLibrary() })
        }

        // Create filter panel
        val filterPanel = JPanel(FlowLayout(FlowLayout.LEFT)).apply {
            add(JLabel("Status:"))
            add(statusCombo)
            add(Box.createHorizontalStrut(10))
            add(JLabel("Category:"))
            add(categoryCombo)
            add(Box.createHorizontalStrut(10))
            add(JLabel("Model:"))
            add(modelCombo)
            add(Box.createHorizontalStrut(10))
            add(JLabel("Author:"))
            add(authorCombo)
            add(Box.createHorizontalStrut(10))
            add(createButton("Apply Filters", "filter") { loadData() })
        }

        // Setup combo boxes
        statusCombo.apply {
            TeamPatternManager.PatternStatus.values().forEach { addItem(it) }
            selectedItem = null
        }

        // Create pattern table
        patternTable.model = DefaultTableModel(
            arrayOf("Name", "Category", "Model", "Author", "Status", "Version", "Usage", "Success Rate"),
            0
        ).apply {
            isCellEditable = false
        }

        // Create review table
        reviewTable.model = DefaultTableModel(
            arrayOf("Reviewer", "Status", "Comments", "Date"),
            0
        ).apply {
            isCellEditable = false
        }

        // Create main content panel
        val contentPanel = JPanel(BorderLayout()).apply {
            add(filterPanel, BorderLayout.NORTH)
            add(JBScrollPane(patternTable), BorderLayout.CENTER)
            add(JBScrollPane(reviewTable), BorderLayout.SOUTH)
        }

        // Add components to dialog
        setContentPane(JPanel(BorderLayout()).apply {
            add(toolbar, BorderLayout.NORTH)
            add(contentPanel, BorderLayout.CENTER)
        })

        // Setup table selection listener
        patternTable.selectionModel.addListSelectionListener {
            if (!it.valueIsAdjusting) {
                loadReviews()
            }
        }
    }

    private fun loadData() {
        val patterns = teamPatternManager.getTeamPatterns(
            category = categoryCombo.selectedItem as? String,
            model = modelCombo.selectedItem as? String,
            status = statusCombo.selectedItem as? TeamPatternManager.PatternStatus,
            author = authorCombo.selectedItem as? String
        )

        val model = patternTable.model as DefaultTableModel
        model.rowCount = 0
        patterns.forEach { pattern ->
            model.addRow(arrayOf(
                pattern.name,
                pattern.category,
                pattern.model,
                pattern.author,
                pattern.status,
                pattern.version,
                pattern.usageCount,
                String.format("%.1f%%", pattern.successRate * 100)
            ))
        }

        // Update filter options
        updateFilterOptions(patterns)
    }

    private fun loadReviews() {
        val selectedRow = patternTable.selectedRow
        if (selectedRow == -1) return

        val patternName = patternTable.getValueAt(selectedRow, 0) as String
        val pattern = teamPatternManager.getTeamPatterns().find { it.name == patternName } ?: return

        val model = reviewTable.model as DefaultTableModel
        model.rowCount = 0
        pattern.reviews.forEach { review ->
            val reviewer = teamPatternManager.getTeamMember(review.reviewerId)
            model.addRow(arrayOf(
                reviewer?.name ?: "Unknown",
                review.status,
                review.comments,
                review.createdAt.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"))
            ))
        }
    }

    private fun updateFilterOptions(patterns: List<TeamPatternManager.TeamPattern>) {
        // Update category combo
        val categories = patterns.map { it.category }.distinct()
        categoryCombo.removeAllItems()
        categoryCombo.addItem(null)
        categories.forEach { categoryCombo.addItem(it) }

        // Update model combo
        val models = patterns.map { it.model }.distinct()
        modelCombo.removeAllItems()
        modelCombo.addItem(null)
        models.forEach { modelCombo.addItem(it) }

        // Update author combo
        val authors = patterns.map { it.author }.distinct()
        authorCombo.removeAllItems()
        authorCombo.addItem(null)
        authors.forEach { authorCombo.addItem(it) }
    }

    private fun showAddPatternDialog() {
        val dialog = TeamPatternDialog(project)
        if (dialog.showAndGet()) {
            val pattern = dialog.getPattern()
            teamPatternManager.addTeamPattern(pattern)
            loadData()
        }
    }

    private fun showEditPatternDialog() {
        val selectedRow = patternTable.selectedRow
        if (selectedRow == -1) return

        val patternName = patternTable.getValueAt(selectedRow, 0) as String
        val pattern = teamPatternManager.getTeamPatterns().find { it.name == patternName } ?: return

        val dialog = TeamPatternDialog(project, pattern)
        if (dialog.showAndGet()) {
            val updatedPattern = dialog.getPattern()
            teamPatternManager.updateTeamPattern(updatedPattern)
            loadData()
        }
    }

    private fun deleteSelectedPattern() {
        val selectedRow = patternTable.selectedRow
        if (selectedRow == -1) return

        val patternName = patternTable.getValueAt(selectedRow, 0) as String
        val pattern = teamPatternManager.getTeamPatterns().find { it.name == patternName } ?: return

        val result = JOptionPane.showConfirmDialog(
            this,
            "Are you sure you want to delete pattern '${pattern.name}'?",
            "Confirm Delete",
            JOptionPane.YES_NO_OPTION
        )

        if (result == JOptionPane.YES_OPTION) {
            teamPatternManager.deleteTeamPattern(pattern.id)
            loadData()
        }
    }

    private fun submitForReview() {
        val selectedRow = patternTable.selectedRow
        if (selectedRow == -1) return

        val patternName = patternTable.getValueAt(selectedRow, 0) as String
        val pattern = teamPatternManager.getTeamPatterns().find { it.name == patternName } ?: return

        teamPatternManager.updateTeamPattern(pattern.copy(status = TeamPatternManager.PatternStatus.PENDING_REVIEW))
        loadData()
    }

    private fun syncWithLibrary() {
        teamPatternManager.syncWithPatternLibrary()
        JOptionPane.showMessageDialog(
            this,
            "Patterns synchronized with library",
            "Sync Complete",
            JOptionPane.INFORMATION_MESSAGE
        )
    }

    private fun createButton(text: String, icon: String, action: () -> Unit): JButton {
        return JButton(text).apply {
            addActionListener { action() }
            // TODO: Add icons
        }
    }
} 