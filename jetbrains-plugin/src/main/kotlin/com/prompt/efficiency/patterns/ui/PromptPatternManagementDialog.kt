package com.prompt.efficiency.patterns.ui

import com.intellij.openapi.project.Project
import com.intellij.openapi.ui.DialogWrapper
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.table.JBTable
import com.intellij.util.ui.JBUI
import com.prompt.efficiency.patterns.PromptPatternLibrary
import java.awt.BorderLayout
import java.awt.Dimension
import javax.swing.*
import javax.swing.table.DefaultTableModel
import java.util.UUID

class PromptPatternManagementDialog(
    private val project: Project
) : DialogWrapper(project) {
    private val patternLibrary = PromptPatternLibrary.getInstance(project)
    private val patternTable = JBTable()
    private val categoryCombo = JComboBox<String>()
    private val modelCombo = JComboBox<String>()
    private val tagField = JTextField()
    private val searchField = JTextField()

    init {
        title = "Prompt Pattern Management"
        init()
        setupUI()
        loadPatterns()
    }

    private fun setupUI() {
        // Create toolbar
        val toolbar = JToolBar().apply {
            isFloatable = false
            add(createButton("Add Pattern", "add") { showAddPatternDialog() })
            add(createButton("Edit Pattern", "edit") { editSelectedPattern() })
            add(createButton("Delete Pattern", "delete") { deleteSelectedPattern() })
            add(createButton("Import", "import") { importPatterns() })
            add(createButton("Export", "export") { exportPatterns() })
        }

        // Create filter panel
        val filterPanel = JPanel().apply {
            layout = BoxLayout(this, BoxLayout.X_AXIS)
            add(JLabel("Category:"))
            add(Box.createHorizontalStrut(5))
            add(categoryCombo)
            add(Box.createHorizontalStrut(10))
            add(JLabel("Model:"))
            add(Box.createHorizontalStrut(5))
            add(modelCombo)
            add(Box.createHorizontalStrut(10))
            add(JLabel("Tags:"))
            add(Box.createHorizontalStrut(5))
            add(tagField)
            add(Box.createHorizontalStrut(10))
            add(JLabel("Search:"))
            add(Box.createHorizontalStrut(5))
            add(searchField)
        }

        // Setup table
        patternTable.model = DefaultTableModel(
            arrayOf("Name", "Category", "Model", "Tags", "Usage", "Success Rate"),
            0
        ).apply {
            isCellEditable = false
        }

        // Add components to main panel
        contentPanel.apply {
            layout = BorderLayout()
            add(toolbar, BorderLayout.NORTH)
            add(filterPanel, BorderLayout.CENTER)
            add(JBScrollPane(patternTable), BorderLayout.SOUTH)
            preferredSize = Dimension(800, 600)
        }

        // Setup filter listeners
        setupFilterListeners()
    }

    private fun setupFilterListeners() {
        categoryCombo.apply {
            addItem("All Categories")
            patternLibrary.state.categories.forEach { addItem(it) }
            addActionListener { loadPatterns() }
        }

        modelCombo.apply {
            addItem("All Models")
            addItem("gpt-4")
            addItem("gpt-3.5-turbo")
            addItem("general")
            addActionListener { loadPatterns() }
        }

        tagField.addActionListener { loadPatterns() }
        searchField.addActionListener { loadPatterns() }
    }

    private fun loadPatterns() {
        val model = patternTable.model as DefaultTableModel
        model.rowCount = 0

        var patterns = patternLibrary.state.patterns

        // Apply filters
        if (categoryCombo.selectedItem != "All Categories") {
            patterns = patterns.filter { it.category == categoryCombo.selectedItem }
        }
        if (modelCombo.selectedItem != "All Models") {
            patterns = patterns.filter { it.model == modelCombo.selectedItem }
        }
        if (tagField.text.isNotEmpty()) {
            val tags = tagField.text.split(",").map { it.trim() }
            patterns = patterns.filter { pattern ->
                tags.any { tag -> pattern.tags.contains(tag) }
            }
        }
        if (searchField.text.isNotEmpty()) {
            val search = searchField.text.lowercase()
            patterns = patterns.filter {
                it.name.lowercase().contains(search) ||
                it.description.lowercase().contains(search) ||
                it.template.lowercase().contains(search)
            }
        }

        // Add patterns to table
        patterns.forEach { pattern ->
            model.addRow(arrayOf(
                pattern.name,
                pattern.category,
                pattern.model,
                pattern.tags.joinToString(", "),
                pattern.usageCount,
                String.format("%.1f%%", pattern.successRate * 100)
            ))
        }
    }

    private fun showAddPatternDialog() {
        val dialog = PromptPatternDialog(project)
        if (dialog.showAndGet()) {
            val pattern = dialog.getPattern()
            patternLibrary.addPattern(pattern)
            loadPatterns()
        }
    }

    private fun editSelectedPattern() {
        val selectedRow = patternTable.selectedRow
        if (selectedRow >= 0) {
            val patternName = patternTable.getValueAt(selectedRow, 0) as String
            val pattern = patternLibrary.state.patterns.find { it.name == patternName }
            pattern?.let {
                val dialog = PromptPatternDialog(project, it)
                if (dialog.showAndGet()) {
                    patternLibrary.updatePattern(dialog.getPattern())
                    loadPatterns()
                }
            }
        }
    }

    private fun deleteSelectedPattern() {
        val selectedRow = patternTable.selectedRow
        if (selectedRow >= 0) {
            val patternName = patternTable.getValueAt(selectedRow, 0) as String
            val pattern = patternLibrary.state.patterns.find { it.name == patternName }
            pattern?.let {
                val result = JOptionPane.showConfirmDialog(
                    this,
                    "Are you sure you want to delete the pattern '${pattern.name}'?",
                    "Confirm Deletion",
                    JOptionPane.YES_NO_OPTION
                )
                if (result == JOptionPane.YES_OPTION) {
                    patternLibrary.deletePattern(pattern.id)
                    loadPatterns()
                }
            }
        }
    }

    private fun importPatterns() {
        val fileChooser = JFileChooser().apply {
            fileSelectionMode = JFileChooser.FILES_ONLY
            fileFilter = object : javax.swing.filechooser.FileFilter() {
                override fun accept(f: java.io.File) = f.isDirectory || f.name.endsWith(".json")
                override fun getDescription() = "JSON Files (*.json)"
            }
        }

        if (fileChooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            try {
                val file = fileChooser.selectedFile
                val json = file.readText()
                // TODO: Implement JSON import
                loadPatterns()
            } catch (e: Exception) {
                JOptionPane.showMessageDialog(
                    this,
                    "Error importing patterns: ${e.message}",
                    "Import Error",
                    JOptionPane.ERROR_MESSAGE
                )
            }
        }
    }

    private fun exportPatterns() {
        val fileChooser = JFileChooser().apply {
            fileSelectionMode = JFileChooser.FILES_ONLY
            fileFilter = object : javax.swing.filechooser.FileFilter() {
                override fun accept(f: java.io.File) = f.isDirectory || f.name.endsWith(".json")
                override fun getDescription() = "JSON Files (*.json)"
            }
        }

        if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            try {
                val file = fileChooser.selectedFile
                // TODO: Implement JSON export
            } catch (e: Exception) {
                JOptionPane.showMessageDialog(
                    this,
                    "Error exporting patterns: ${e.message}",
                    "Export Error",
                    JOptionPane.ERROR_MESSAGE
                )
            }
        }
    }

    private fun createButton(text: String, icon: String, action: () -> Unit): JButton {
        return JButton(text).apply {
            addActionListener { action() }
            // TODO: Add icons
        }
    }
}
