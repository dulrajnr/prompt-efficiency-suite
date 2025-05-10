package com.prompt.efficiency.collab

import com.intellij.openapi.components.Service
import com.intellij.openapi.components.service
import com.intellij.openapi.project.Project
import com.prompt.efficiency.settings.PromptEfficiencySettings
import java.time.LocalDateTime
import java.util.*

@Service(Service.Level.PROJECT)
class TeamPatternManager(private val project: Project) {
    private val patterns = mutableMapOf<String, TeamPattern>()
    private val reviews = mutableMapOf<String, MutableList<PatternReview>>()
    private val settings = project.service<PromptEfficiencySettings>()

    fun addPattern(pattern: TeamPattern) {
        patterns[pattern.id] = pattern
    }

    fun updatePattern(pattern: TeamPattern) {
        if (!patterns.containsKey(pattern.id)) {
            throw IllegalArgumentException("Pattern with ID ${pattern.id} does not exist")
        }
        patterns[pattern.id] = pattern
    }

    fun deletePattern(patternId: String) {
        patterns.remove(patternId)
        reviews.remove(patternId)
    }

    fun getPattern(patternId: String): TeamPattern? {
        return patterns[patternId]
    }

    fun getAllPatterns(): List<TeamPattern> {
        return patterns.values.toList()
    }

    fun getPatternsByCategory(category: String): List<TeamPattern> {
        return patterns.values.filter { it.category == category }
    }

    fun getPatternsByModel(model: String): List<TeamPattern> {
        return patterns.values.filter { it.model == model }
    }

    fun addReview(review: PatternReview) {
        reviews.getOrPut(review.patternId) { mutableListOf() }.add(review)
    }

    fun getReviews(patternId: String): List<PatternReview> {
        return reviews[patternId] ?: emptyList()
    }

    fun getLatestReview(patternId: String): PatternReview? {
        return reviews[patternId]?.maxByOrNull { it.reviewDate }
    }

    fun getPatternsNeedingReview(): List<TeamPattern> {
        return patterns.values.filter { pattern ->
            val latestReview = getLatestReview(pattern.id)
            latestReview == null || latestReview.status == ReviewStatus.PENDING
        }
    }

    fun getPatternsByAuthor(authorId: String): List<TeamPattern> {
        return patterns.values.filter { it.authorId == authorId }
    }

    fun getPatternsByVersion(version: String): List<TeamPattern> {
        return patterns.values.filter { it.version == version }
    }

    fun getPatternsByUsageCount(minCount: Int): List<TeamPattern> {
        return patterns.values.filter { it.usageCount >= minCount }
    }

    fun getPatternsBySuccessRate(minRate: Double): List<TeamPattern> {
        return patterns.values.filter { it.successRate >= minRate }
    }

    fun incrementUsage(patternId: String, success: Boolean) {
        patterns[patternId]?.let { pattern ->
            val newUsageCount = pattern.usageCount + 1
            val newSuccessCount = pattern.successCount + if (success) 1 else 0
            val newSuccessRate = newSuccessCount.toDouble() / newUsageCount

            patterns[patternId] = pattern.copy(
                usageCount = newUsageCount,
                successCount = newSuccessCount,
                successRate = newSuccessRate,
                lastUsed = LocalDateTime.now()
            )
        }
    }

    data class TeamPattern(
        val id: String = UUID.randomUUID().toString(),
        val name: String,
        val category: String,
        val model: String,
        val template: String,
        val description: String,
        val authorId: String,
        val version: String = "1.0",
        val usageCount: Int = 0,
        val successCount: Int = 0,
        val successRate: Double = 0.0,
        val createdAt: LocalDateTime = LocalDateTime.now(),
        val updatedAt: LocalDateTime = LocalDateTime.now(),
        val lastUsed: LocalDateTime? = null
    )

    data class PatternReview(
        val id: String = UUID.randomUUID().toString(),
        val patternId: String,
        val reviewerId: String,
        val status: ReviewStatus,
        val comments: String,
        val reviewDate: LocalDateTime = LocalDateTime.now()
    )

    enum class ReviewStatus {
        PENDING,
        APPROVED,
        REJECTED,
        NEEDS_REVISION
    }

    companion object {
        fun getInstance(project: Project): TeamPatternManager {
            return project.service()
        }
    }
}
