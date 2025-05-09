package com.prompt.efficiency.analytics.ui

import com.intellij.openapi.project.Project
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.table.JBTable
import com.intellij.util.ui.JBUI
import com.prompt.efficiency.analytics.CostAnalytics
import org.jfree.chart.ChartFactory
import org.jfree.chart.ChartPanel
import org.jfree.chart.JFreeChart
import org.jfree.chart.plot.PlotOrientation
import org.jfree.data.category.DefaultCategoryDataset
import org.jfree.data.time.TimeSeriesCollection
import org.jfree.data.time.Day
import java.awt.BorderLayout
import java.awt.Dimension
import java.awt.FlowLayout
import javax.swing.*
import javax.swing.table.DefaultTableModel
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

class CostAnalyticsPanel(private val project: Project) : JPanel() {
    private val costAnalytics = CostAnalytics.getInstance(project)
    private val timeRangeCombo = JComboBox<CostAnalytics.TimeRange>()
    private val costTable = JBTable()
    private val alertsTable = JBTable()
    private val chartPanel = ChartPanel(null)

    init {
        layout = BorderLayout()
        setupUI()
        loadData()
    }

    private fun setupUI() {
        // Create toolbar
        val toolbar = JToolBar().apply {
            isFloatable = false
            add(JLabel("Time Range:"))
            add(Box.createHorizontalStrut(5))
            add(timeRangeCombo)
            add(Box.createHorizontalStrut(10))
            add(createButton("Refresh", "refresh") { loadData() })
            add(createButton("Export", "export") { exportData() })
        }

        // Setup time range combo
        timeRangeCombo.apply {
            CostAnalytics.TimeRange.values().forEach { addItem(it) }
            selectedItem = CostAnalytics.TimeRange.DAILY
            addActionListener { loadData() }
        }

        // Create cost summary panel
        val costSummaryPanel = JPanel(BorderLayout()).apply {
            border = JBUI.Borders.empty(10)
            add(createCostSummaryTable(), BorderLayout.CENTER)
        }

        // Create charts panel
        val chartsPanel = JPanel(BorderLayout()).apply {
            border = JBUI.Borders.empty(10)
            add(createCharts(), BorderLayout.CENTER)
        }

        // Create alerts panel
        val alertsPanel = JPanel(BorderLayout()).apply {
            border = JBUI.Borders.empty(10)
            add(createAlertsTable(), BorderLayout.CENTER)
        }

        // Create main content panel
        val contentPanel = JPanel(BorderLayout()).apply {
            add(costSummaryPanel, BorderLayout.NORTH)
            add(chartsPanel, BorderLayout.CENTER)
            add(alertsPanel, BorderLayout.SOUTH)
        }

        // Add components to main panel
        add(toolbar, BorderLayout.NORTH)
        add(JBScrollPane(contentPanel), BorderLayout.CENTER)
    }

    private fun createCostSummaryTable(): JTable {
        costTable.model = DefaultTableModel(
            arrayOf("Metric", "Value"),
            0
        ).apply {
            isCellEditable = false
        }
        return costTable
    }

    private fun createCharts(): JPanel {
        return JPanel(BorderLayout()).apply {
            add(chartPanel, BorderLayout.CENTER)
        }
    }

    private fun createAlertsTable(): JTable {
        alertsTable.model = DefaultTableModel(
            arrayOf("Time", "Type", "Message", "Threshold", "Current Value"),
            0
        ).apply {
            isCellEditable = false
        }
        return alertsTable
    }

    private fun loadData() {
        val timeRange = timeRangeCombo.selectedItem as CostAnalytics.TimeRange
        val stats = costAnalytics.getUsageStats(timeRange)
        val alerts = costAnalytics.getAlerts(timeRange)

        // Update cost summary table
        val costModel = costTable.model as DefaultTableModel
        costModel.rowCount = 0
        costModel.addRow(arrayOf("Total Cost", String.format("%.2f", stats.totalCost)))
        costModel.addRow(arrayOf("Total Tokens", stats.totalTokens))
        costModel.addRow(arrayOf("Average Cost per Token", String.format("%.4f", stats.averageCostPerToken)))

        // Update charts
        updateCharts(stats)

        // Update alerts table
        val alertsModel = alertsTable.model as DefaultTableModel
        alertsModel.rowCount = 0
        alerts.forEach { alert ->
            alertsModel.addRow(arrayOf(
                alert.timestamp.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")),
                alert.type.name,
                alert.message,
                String.format("%.2f", alert.threshold),
                String.format("%.2f", alert.currentValue)
            ))
        }
    }

    private fun updateCharts(stats: CostAnalytics.UsageStats) {
        // Create cost by model chart
        val modelDataset = DefaultCategoryDataset()
        stats.usageByModel.forEach { (model, cost) ->
            modelDataset.addValue(cost, "Cost", model)
        }
        val modelChart = ChartFactory.createBarChart(
            "Cost by Model",
            "Model",
            "Cost",
            modelDataset,
            PlotOrientation.VERTICAL,
            true,
            true,
            false
        )

        // Create cost by pattern chart
        val patternDataset = DefaultCategoryDataset()
        stats.usageByPattern.forEach { (pattern, cost) ->
            patternDataset.addValue(cost, "Cost", pattern ?: "Unknown")
        }
        val patternChart = ChartFactory.createBarChart(
            "Cost by Pattern",
            "Pattern",
            "Cost",
            patternDataset,
            PlotOrientation.VERTICAL,
            true,
            true,
            false
        )

        // Create time series chart
        val timeSeriesDataset = TimeSeriesCollection()
        // TODO: Implement time series data collection and chart creation

        // Update chart panel
        chartPanel.chart = modelChart
    }

    private fun exportData() {
        val fileChooser = JFileChooser().apply {
            fileSelectionMode = JFileChooser.FILES_ONLY
            fileFilter = object : javax.swing.filechooser.FileFilter() {
                override fun accept(f: java.io.File) = f.isDirectory || f.name.endsWith(".csv")
                override fun getDescription() = "CSV Files (*.csv)"
            }
        }

        if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            try {
                val file = fileChooser.selectedFile
                // TODO: Implement CSV export
            } catch (e: Exception) {
                JOptionPane.showMessageDialog(
                    this,
                    "Error exporting data: ${e.message}",
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