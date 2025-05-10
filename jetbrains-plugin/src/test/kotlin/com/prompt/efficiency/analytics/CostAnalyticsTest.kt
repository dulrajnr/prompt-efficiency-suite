package com.prompt.efficiency.analytics

import com.intellij.testFramework.LightPlatformTestCase
import java.time.LocalDateTime
import java.util.UUID

class CostAnalyticsTest : LightPlatformTestCase() {
    private lateinit var costAnalytics: CostAnalytics

    override fun setUp() {
        super.setUp()
        costAnalytics = CostAnalytics.getInstance(project)
    }

    fun testAddUsageRecord() {
        val record = CostAnalytics.UsageRecord(
            model = "gpt-4",
            promptTokens = 100,
            completionTokens = 50,
            totalTokens = 150,
            cost = 0.03,
            currency = "USD"
        )

        costAnalytics.addUsageRecord(record)
        val stats = costAnalytics.getUsageStats(CostAnalytics.TimeRange.ALL)

        assertEquals(0.03, stats.totalCost)
        assertEquals(150, stats.totalTokens)
        assertEquals(0.03 / 150, stats.averageCostPerToken)
        assertEquals(mapOf("gpt-4" to 0.03), stats.usageByModel)
    }

    fun testCostLimits() {
        // Set cost limit
        costAnalytics.setCostLimit("gpt-4", 0.05)

        // Add record within limit
        val record1 = CostAnalytics.UsageRecord(
            model = "gpt-4",
            promptTokens = 100,
            completionTokens = 50,
            totalTokens = 150,
            cost = 0.03,
            currency = "USD"
        )
        costAnalytics.addUsageRecord(record1)

        // Add record exceeding limit
        val record2 = CostAnalytics.UsageRecord(
            model = "gpt-4",
            promptTokens = 200,
            completionTokens = 100,
            totalTokens = 300,
            cost = 0.06,
            currency = "USD"
        )
        costAnalytics.addUsageRecord(record2)

        // Check alerts
        val alerts = costAnalytics.getAlerts(CostAnalytics.TimeRange.ALL)
        assertTrue(alerts.any { it.type == CostAnalytics.AlertType.DAILY_LIMIT_EXCEEDED })
    }

    fun testUnusualUsage() {
        // Add normal usage records
        repeat(5) {
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
        }

        // Add unusual usage record
        costAnalytics.addUsageRecord(
            CostAnalytics.UsageRecord(
                model = "gpt-4",
                promptTokens = 1000,
                completionTokens = 500,
                totalTokens = 1500,
                cost = 0.3,
                currency = "USD"
            )
        )

        // Check alerts
        val alerts = costAnalytics.getAlerts(CostAnalytics.TimeRange.ALL)
        assertTrue(alerts.any { it.type == CostAnalytics.AlertType.UNUSUAL_USAGE })
    }

    fun testUsageStatsByTimeRange() {
        // Add records for different time periods
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

        // Monthly record
        costAnalytics.addUsageRecord(
            CostAnalytics.UsageRecord(
                timestamp = now.minusDays(15),
                model = "gpt-4",
                promptTokens = 300,
                completionTokens = 150,
                totalTokens = 450,
                cost = 0.09,
                currency = "USD"
            )
        )

        // Check daily stats
        val dailyStats = costAnalytics.getUsageStats(CostAnalytics.TimeRange.DAILY)
        assertEquals(0.03, dailyStats.totalCost)
        assertEquals(150, dailyStats.totalTokens)

        // Check weekly stats
        val weeklyStats = costAnalytics.getUsageStats(CostAnalytics.TimeRange.WEEKLY)
        assertEquals(0.09, weeklyStats.totalCost)
        assertEquals(450, weeklyStats.totalTokens)

        // Check monthly stats
        val monthlyStats = costAnalytics.getUsageStats(CostAnalytics.TimeRange.MONTHLY)
        assertEquals(0.18, monthlyStats.totalCost)
        assertEquals(900, monthlyStats.totalTokens)
    }

    fun testPatternUsage() {
        val patternId = UUID.randomUUID().toString()

        // Add records with pattern
        repeat(3) {
            costAnalytics.addUsageRecord(
                CostAnalytics.UsageRecord(
                    model = "gpt-4",
                    promptTokens = 100,
                    completionTokens = 50,
                    totalTokens = 150,
                    cost = 0.03,
                    currency = "USD",
                    patternId = patternId
                )
            )
        }

        // Add record without pattern
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

        // Check pattern usage stats
        val stats = costAnalytics.getUsageStats(CostAnalytics.TimeRange.ALL)
        assertEquals(mapOf(patternId to 0.09, null to 0.03), stats.usageByPattern)
    }
}
