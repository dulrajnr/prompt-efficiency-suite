package com.prompt.efficiency.analytics.ui

import com.intellij.testFramework.LightPlatformTestCase
import com.prompt.efficiency.analytics.CostAnalytics
import java.time.LocalDateTime
import javax.swing.JComboBox
import javax.swing.JTable
import javax.swing.table.DefaultTableModel

class CostAnalyticsPanelTest : LightPlatformTestCase() {
    private lateinit var panel: CostAnalyticsPanel
    private lateinit var costAnalytics: CostAnalytics

    override fun setUp() {
        super.setUp()
        costAnalytics = CostAnalytics.getInstance(project)
        panel = CostAnalyticsPanel(project)
    }

    fun testInitialState() {
        // Verify initial state of panel components
        assertNotNull(panel)
        assertTrue(panel.isVisible)
        assertTrue(panel.isShowing)

        // Verify time range combo
        val timeRangeCombo = findComboBox(panel, "Time Range")
        assertNotNull(timeRangeCombo)
        assertEquals(CostAnalytics.TimeRange.DAILY, timeRangeCombo.selectedItem)

        // Verify tables
        val costTable = findTable(panel, "Cost")
        val alertsTable = findTable(panel, "Alerts")
        assertNotNull(costTable)
        assertNotNull(alertsTable)
    }

    fun testLoadData() {
        // Add test data
        costAnalytics.addUsageRecord(
            CostAnalytics.UsageRecord(
                model = "gpt-4",
                promptTokens = 100,
                completionTokens = 50,
                totalTokens = 150,
                cost = 0.03,
                currency = "USD"
            )
        )

        // Trigger data load
        panel.loadData()

        // Verify cost table
        val costTable = findTable(panel, "Cost")
        assertNotNull(costTable)
        val costModel = costTable.model as DefaultTableModel
        assertEquals(3, costModel.rowCount)
        assertEquals("Total Cost", costModel.getValueAt(0, 0))
        assertEquals("0.03", costModel.getValueAt(0, 1))
        assertEquals("Total Tokens", costModel.getValueAt(1, 0))
        assertEquals("150", costModel.getValueAt(1, 1))
        assertEquals("Average Cost per Token", costModel.getValueAt(2, 0))
        assertEquals("0.0002", costModel.getValueAt(2, 1))

        // Verify alerts table
        val alertsTable = findTable(panel, "Alerts")
        assertNotNull(alertsTable)
        val alertsModel = alertsTable.model as DefaultTableModel
        assertEquals(0, alertsModel.rowCount) // No alerts for normal usage
    }

    fun testTimeRangeChange() {
        // Add test data for different time periods
        val now = LocalDateTime.now()

        // Daily record
        costAnalytics.addUsageRecord(
            CostAnalytics.UsageRecord(
                timestamp = now,
                model = "gpt-4",
                promptTokens = 100,
                completionTokens = 50,
                totalTokens = 150,
                cost = 0.03,
                currency = "USD"
            )
        )

        // Weekly record
        costAnalytics.addUsageRecord(
            CostAnalytics.UsageRecord(
                timestamp = now.minusDays(3),
                model = "gpt-4",
                promptTokens = 200,
                completionTokens = 100,
                totalTokens = 300,
                cost = 0.06,
                currency = "USD"
            )
        )

        // Change time range to daily
        val timeRangeCombo = findComboBox(panel, "Time Range")
        assertNotNull(timeRangeCombo)
        timeRangeCombo.selectedItem = CostAnalytics.TimeRange.DAILY
        panel.loadData()

        // Verify daily data
        val costTable = findTable(panel, "Cost")
        assertNotNull(costTable)
        val costModel = costTable.model as DefaultTableModel
        assertEquals("0.03", costModel.getValueAt(0, 1)) // Total Cost
        assertEquals("150", costModel.getValueAt(1, 1)) // Total Tokens

        // Change time range to weekly
        timeRangeCombo.selectedItem = CostAnalytics.TimeRange.WEEKLY
        panel.loadData()

        // Verify weekly data
        assertEquals("0.09", costModel.getValueAt(0, 1)) // Total Cost
        assertEquals("450", costModel.getValueAt(1, 1)) // Total Tokens
    }

    fun testAlertsDisplay() {
        // Set cost limit and exceed it
        costAnalytics.setCostLimit("gpt-4", 0.05)
        costAnalytics.addUsageRecord(
            CostAnalytics.UsageRecord(
                model = "gpt-4",
                promptTokens = 200,
                completionTokens = 100,
                totalTokens = 300,
                cost = 0.06,
                currency = "USD"
            )
        )

        // Load data
        panel.loadData()

        // Verify alerts table
        val alertsTable = findTable(panel, "Alerts")
        assertNotNull(alertsTable)
        val alertsModel = alertsTable.model as DefaultTableModel
        assertTrue(alertsModel.rowCount > 0)
        assertTrue(alertsModel.getValueAt(0, 1).toString().contains("DAILY_LIMIT_EXCEEDED"))
    }

    private fun findComboBox(component: java.awt.Component, name: String): JComboBox<*>? {
        if (component is JComboBox<*> && component.name == name) {
            return component
        }
        if (component is java.awt.Container) {
            for (child in component.components) {
                val found = findComboBox(child, name)
                if (found != null) {
                    return found
                }
            }
        }
        return null
    }

    private fun findTable(component: java.awt.Component, name: String): JTable? {
        if (component is JTable && component.name == name) {
            return component
        }
        if (component is java.awt.Container) {
            for (child in component.components) {
                val found = findTable(child, name)
                if (found != null) {
                    return found
                }
            }
        }
        return null
    }
}
