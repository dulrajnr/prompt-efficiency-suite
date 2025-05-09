package com.prompt.efficiency.analytics.ui

import com.intellij.openapi.project.Project
import com.intellij.ui.components.JBScrollPane
import com.intellij.ui.table.JBTable
import com.prompt.efficiency.analytics.CostAnalytics
import org.jfree.chart.ChartFactory
import org.jfree.chart.ChartPanel
import org.jfree.chart.JFreeChart
import org.jfree.chart.plot.PlotOrientation
import org.jfree.data.category.DefaultCategoryDataset
import org.jfree.data.time.Millisecond
import org.jfree.data.time.TimeSeries
import org.jfree.data.time.TimeSeriesCollection
import java.awt.BorderLayout
import java.awt.FlowLayout
import java.awt.GridLayout
import java.time.LocalDateTime
import java.time.ZoneOffset
import java.time.format.DateTimeFormatter
import javax.swing.*
import javax.swing.table.DefaultTableModel

class CostAnalyticsPanel(private val project: Project) : JPanel() {
    private val costAnalytics = CostAnalytics.getInstance(project)
    private val costChart: ChartPanel
    private val usageChart: ChartPanel
    private val timeSeriesChart: ChartPanel
    private val modelTable: JBTable
    private val dateRangeCombo: JComboBox<String>
    private val refreshButton: JButton
    private val exportButton: JButton

    init {
        layout = BorderLayout()

        // Create charts
        costChart = createCostChart()
        usageChart = createUsageChart()
        timeSeriesChart = createTimeSeriesChart()

        // Create model table
        modelTable = JBTable(DefaultTableModel(
            arrayOf("Model", "Usage Count", "Success Rate", "Average Cost"),
            0
        ))
        modelTable.isEnabled = false

        // Create control panel
        val controlPanel = createControlPanel()

        // Layout components
        val chartsPanel = JPanel(GridLayout(3, 1))
        chartsPanel.add(costChart)
        chartsPanel.add(usageChart)
        chartsPanel.add(timeSeriesChart)

        val rightPanel = JPanel(BorderLayout())
        rightPanel.add(JBScrollPane(modelTable), BorderLayout.CENTER)
        rightPanel.add(controlPanel, BorderLayout.SOUTH)

        add(chartsPanel, BorderLayout.CENTER)
        add(rightPanel, BorderLayout.EAST)

        // Initial data load
        refreshData()
    }

    private fun createControlPanel(): JPanel {
        val panel = JPanel(BorderLayout())

        dateRangeCombo = JComboBox(arrayOf(
            "Last 7 days",
            "Last 30 days",
            "Last 90 days"
        ))

        refreshButton = JButton("Refresh").apply {
            addActionListener { refreshData() }
        }

        exportButton = JButton("Export CSV").apply {
            addActionListener { exportToCsv() }
        }

        val buttonPanel = JPanel(FlowLayout(FlowLayout.RIGHT))
        buttonPanel.add(refreshButton)
        buttonPanel.add(exportButton)

        panel.add(dateRangeCombo, BorderLayout.CENTER)
        panel.add(buttonPanel, BorderLayout.EAST)

        return panel
    }

    private fun createCostChart(): ChartPanel {
        val dataset = DefaultCategoryDataset()
        val chart = ChartFactory.createLineChart(
            "Cost Over Time",
            "Date",
            "Cost (USD)",
            dataset,
            PlotOrientation.VERTICAL,
            true,
            true,
            false
        )

        return ChartPanel(chart)
    }

    private fun createUsageChart(): ChartPanel {
        val dataset = DefaultCategoryDataset()
        val chart = ChartFactory.createLineChart(
            "Usage Over Time",
            "Date",
            "Token Count",
            dataset,
            PlotOrientation.VERTICAL,
            true,
            true,
            false
        )

        return ChartPanel(chart)
    }

    private fun createTimeSeriesChart(): ChartPanel {
        val dataset = TimeSeriesCollection()
        val chart = ChartFactory.createTimeSeriesChart(
            "Cost and Usage Over Time",
            "Time",
            "Value",
            dataset,
            true,
            true,
            false
        )

        return ChartPanel(chart)
    }

    private fun refreshData() {
        val daysToShow = when (dateRangeCombo.selectedItem as String) {
            "Last 7 days" -> 7
            "Last 30 days" -> 30
            else -> 90
        }

        val startDate = LocalDateTime.now().minusDays(daysToShow.toLong())
        val records = costAnalytics.getUsageRecords(startDate)

        updateCharts(records)
        updateModelTable(records)
    }

    private fun updateCharts(records: List<CostAnalytics.UsageRecord>) {
        val costDataset = DefaultCategoryDataset()
        val usageDataset = DefaultCategoryDataset()
        val timeSeriesDataset = TimeSeriesCollection()
        val dateFormat = DateTimeFormatter.ofPattern("MM-dd")

        // Create time series for cost and usage
        val costSeries = TimeSeries("Cost")
        val usageSeries = TimeSeries("Usage")

        records.sortedBy { it.timestamp }.forEach { record ->
            val date = record.timestamp.toInstant(ZoneOffset.UTC).toEpochMilli()
            costSeries.add(Millisecond(date), record.cost)
            usageSeries.add(Millisecond(date), record.totalTokens.toDouble())
        }

        timeSeriesDataset.addSeries(costSeries)
        timeSeriesDataset.addSeries(usageSeries)

        // Update existing charts
        records.groupBy { it.timestamp.format(dateFormat) }
            .forEach { (date, dayRecords) ->
                costDataset.addValue(
                    dayRecords.sumOf { it.cost },
                    "Daily Cost",
                    date
                )
                usageDataset.addValue(
                    dayRecords.sumOf { it.tokenCount },
                    "Daily Usage",
                    date
                )
            }

        (costChart.chart.plot.dataset as DefaultCategoryDataset).clear()
        (usageChart.chart.plot.dataset as DefaultCategoryDataset).clear()
        (timeSeriesChart.chart.plot.dataset as TimeSeriesCollection).removeAllSeries()

        (costChart.chart.plot.dataset as DefaultCategoryDataset).addValue(
            costDataset.getValue("Daily Cost", costDataset.getColumnKey(0)),
            "Daily Cost",
            costDataset.getColumnKey(0)
        )
        (usageChart.chart.plot.dataset as DefaultCategoryDataset).addValue(
            usageDataset.getValue("Daily Usage", usageDataset.getColumnKey(0)),
            "Daily Usage",
            usageDataset.getColumnKey(0)
        )
        (timeSeriesChart.chart.plot.dataset as TimeSeriesCollection).addSeries(costSeries)
        (timeSeriesChart.chart.plot.dataset as TimeSeriesCollection).addSeries(usageSeries)
    }

    private fun updateModelTable(records: List<CostAnalytics.UsageRecord>) {
        val model = modelTable.model as DefaultTableModel
        model.rowCount = 0

        records.groupBy { it.model }
            .forEach { (modelName, modelRecords) ->
                val usageCount = modelRecords.size
                val successRate = modelRecords.count { it.success }.toDouble() / usageCount * 100
                val avgCost = modelRecords.sumOf { it.cost } / usageCount

                model.addRow(arrayOf(
                    modelName,
                    usageCount,
                    String.format("%.1f%%", successRate),
                    String.format("$%.4f", avgCost)
                ))
            }
    }

    private fun exportToCsv() {
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
                val writer = java.io.FileWriter(file)
                val csvWriter = com.opencsv.CSVWriter(writer)

                // Write header
                csvWriter.writeNext(arrayOf(
                    "Timestamp",
                    "Model",
                    "Prompt Tokens",
                    "Completion Tokens",
                    "Total Tokens",
                    "Cost",
                    "Currency",
                    "Success"
                ))

                // Write data
                val records = costAnalytics.getUsageRecords(
                    LocalDateTime.now().minusDays(
                        when (dateRangeCombo.selectedItem as String) {
                            "Last 7 days" -> 7
                            "Last 30 days" -> 30
                            else -> 90
                        }.toLong()
                    )
                )

                records.forEach { record ->
                    csvWriter.writeNext(arrayOf(
                        record.timestamp.toString(),
                        record.model,
                        record.promptTokens.toString(),
                        record.completionTokens.toString(),
                        record.totalTokens.toString(),
                        record.cost.toString(),
                        record.currency,
                        record.success.toString()
                    ))
                }

                csvWriter.close()
                writer.close()

                JOptionPane.showMessageDialog(
                    this,
                    "Data exported successfully to ${file.absolutePath}",
                    "Export Complete",
                    JOptionPane.INFORMATION_MESSAGE
                )
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
} 