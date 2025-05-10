package com.prompt.efficiency.analytics

import com.intellij.openapi.components.Service
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.openapi.project.Project
import com.intellij.util.xmlb.XmlSerializerUtil
import java.time.LocalDateTime
import java.time.temporal.ChronoUnit
import java.util.*

@Service(Service.Level.PROJECT)
@State(
    name = "PromptEfficiencyCostAnalytics",
    storages = [Storage("prompt-efficiency-cost-analytics.xml")]
)
class CostAnalytics(private val project: Project) {
    @State
    var state = State()

    data class State(
        var usageRecords: MutableList<UsageRecord> = mutableListOf(),
        var costLimits: MutableMap<String, Double> = mutableMapOf(),
        var alerts: MutableList<CostAlert> = mutableListOf()
    )

    data class UsageRecord(
        val id: String = UUID.randomUUID().toString(),
        val timestamp: LocalDateTime = LocalDateTime.now(),
        val model: String,
        val promptTokens: Int,
        val completionTokens: Int,
        val totalTokens: Int,
        val cost: Double,
        val currency: String,
        val promptId: String? = null,
        val patternId: String? = null
    )

    data class CostAlert(
        val id: String = UUID.randomUUID().toString(),
        val timestamp: LocalDateTime = LocalDateTime.now(),
        val type: AlertType,
        val message: String,
        val threshold: Double,
        val currentValue: Double
    )

    enum class AlertType {
        DAILY_LIMIT_EXCEEDED,
        MONTHLY_LIMIT_EXCEEDED,
        UNUSUAL_USAGE,
        HIGH_COST_PATTERN
    }

    fun addUsageRecord(record: UsageRecord) {
        state.usageRecords.add(record)
        checkCostLimits(record)
        checkUnusualUsage(record)
    }

    fun getUsageStats(timeRange: TimeRange): UsageStats {
        val records = filterRecordsByTimeRange(timeRange)
        return UsageStats(
            totalCost = records.sumOf { it.cost },
            totalTokens = records.sumOf { it.totalTokens },
            averageCostPerToken = records.sumOf { it.cost } / records.sumOf { it.totalTokens },
            usageByModel = records.groupBy { it.model }
                .mapValues { it.value.sumOf { record -> record.cost } },
            usageByPattern = records.filter { it.patternId != null }
                .groupBy { it.patternId }
                .mapValues { it.value.sumOf { record -> record.cost } }
        )
    }

    fun setCostLimit(model: String, limit: Double) {
        state.costLimits[model] = limit
    }

    fun getCostLimit(model: String): Double? = state.costLimits[model]

    fun getAlerts(timeRange: TimeRange): List<CostAlert> {
        return state.alerts.filter {
            it.timestamp.isAfter(timeRange.start) &&
            it.timestamp.isBefore(timeRange.end)
        }
    }

    private fun checkCostLimits(record: UsageRecord) {
        val limit = state.costLimits[record.model] ?: return

        // Check daily limit
        val dailyCost = getUsageStats(TimeRange.DAILY).totalCost
        if (dailyCost > limit) {
            state.alerts.add(CostAlert(
                type = AlertType.DAILY_LIMIT_EXCEEDED,
                message = "Daily cost limit exceeded for ${record.model}",
                threshold = limit,
                currentValue = dailyCost
            ))
        }

        // Check monthly limit
        val monthlyCost = getUsageStats(TimeRange.MONTHLY).totalCost
        if (monthlyCost > limit * 30) {
            state.alerts.add(CostAlert(
                type = AlertType.MONTHLY_LIMIT_EXCEEDED,
                message = "Monthly cost limit exceeded for ${record.model}",
                threshold = limit * 30,
                currentValue = monthlyCost
            ))
        }
    }

    private fun checkUnusualUsage(record: UsageRecord) {
        val recentRecords = filterRecordsByTimeRange(TimeRange.DAILY)
        val averageCost = recentRecords.map { it.cost }.average()
        val standardDeviation = calculateStandardDeviation(recentRecords.map { it.cost })

        if (record.cost > averageCost + (2 * standardDeviation)) {
            state.alerts.add(CostAlert(
                type = AlertType.UNUSUAL_USAGE,
                message = "Unusual usage detected for ${record.model}",
                threshold = averageCost + (2 * standardDeviation),
                currentValue = record.cost
            ))
        }
    }

    private fun filterRecordsByTimeRange(timeRange: TimeRange): List<UsageRecord> {
        val now = LocalDateTime.now()
        return state.usageRecords.filter { record ->
            when (timeRange) {
                TimeRange.DAILY -> record.timestamp.isAfter(now.minus(1, ChronoUnit.DAYS))
                TimeRange.WEEKLY -> record.timestamp.isAfter(now.minus(7, ChronoUnit.DAYS))
                TimeRange.MONTHLY -> record.timestamp.isAfter(now.minus(30, ChronoUnit.DAYS))
                TimeRange.ALL -> true
            }
        }
    }

    private fun calculateStandardDeviation(values: List<Double>): Double {
        if (values.isEmpty()) return 0.0
        val mean = values.average()
        val variance = values.map { (it - mean) * (it - mean) }.average()
        return kotlin.math.sqrt(variance)
    }

    enum class TimeRange {
        DAILY, WEEKLY, MONTHLY, ALL
    }

    data class UsageStats(
        val totalCost: Double,
        val totalTokens: Int,
        val averageCostPerToken: Double,
        val usageByModel: Map<String, Double>,
        val usageByPattern: Map<String?, Double>
    )

    companion object {
        fun getInstance(project: Project): CostAnalytics {
            return project.getService(CostAnalytics::class.java)
        }
    }
}
