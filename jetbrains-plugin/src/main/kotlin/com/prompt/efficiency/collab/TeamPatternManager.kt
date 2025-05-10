package com.prompt.efficiency.collab

import com.intellij.openapi.components.Service
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.openapi.project.Project
import com.intellij.util.xmlb.XmlSerializerUtil
import com.prompt.efficiency.patterns.PromptPatternLibrary
import java.time.LocalDateTime
import java.util.*

@Service(Service.Level.PROJECT)
@State(
    name = "PromptEfficiencyTeamPatterns",
    storages = [Storage("prompt-efficiency-team-patterns.xml")]
)
class TeamPatternManager(private val project: Project) {
    @State
    var state = State()

    data class State(
        var teamPatterns: MutableList<TeamPattern> = mutableListOf(),
        var teamMembers: MutableList<TeamMember> = mutableListOf(),
        var patternReviews: MutableList<PatternReview> = mutableListOf()
    )

    data class TeamPattern(
        val id: String = UUID.randomUUID().toString(),
        val name: String,
        val description: String,
        val template: String,
        val category: String,
        val model: String,
        val tags: Set<String>,
        val author: String,
        val createdAt: LocalDateTime = LocalDateTime.now(),
        val updatedAt: LocalDateTime = LocalDateTime.now(),
        val status: PatternStatus = PatternStatus.DRAFT,
        val version: Int = 1,
        val usageCount: Int = 0,
        val successRate: Double = 0.0,
        val reviews: MutableList<PatternReview> = mutableListOf()
    )

    data class TeamMember(
        val id: String = UUID.randomUUID().toString(),
        val name: String,
        val email: String,
        val role: TeamRole,
        val joinedAt: LocalDateTime = LocalDateTime.now()
    )

    data class PatternReview(
        val id: String = UUID.randomUUID().toString(),
        val patternId: String,
        val reviewerId: String,
        val status: ReviewStatus,
        val comments: String,
        val createdAt: LocalDateTime = LocalDateTime.now()
    )

    enum class PatternStatus {
        DRAFT,
        PENDING_REVIEW,
        APPROVED,
        REJECTED,
        DEPRECATED
    }

    enum class TeamRole {
        ADMIN,
        REVIEWER,
        CONTRIBUTOR
    }

    enum class ReviewStatus {
        APPROVED,
        REJECTED,
        NEEDS_REVISION
    }

    fun addTeamPattern(pattern: TeamPattern) {
        state.teamPatterns.add(pattern)
    }

    fun updateTeamPattern(pattern: TeamPattern) {
        val index = state.teamPatterns.indexOfFirst { it.id == pattern.id }
        if (index != -1) {
            state.teamPatterns[index] = pattern.copy(
                updatedAt = LocalDateTime.now(),
                version = pattern.version + 1
            )
        }
    }

    fun deleteTeamPattern(patternId: String) {
        state.teamPatterns.removeIf { it.id == patternId }
    }

    fun getTeamPattern(patternId: String): TeamPattern? {
        return state.teamPatterns.find { it.id == patternId }
    }

    fun getTeamPatterns(
        category: String? = null,
        model: String? = null,
        status: PatternStatus? = null,
        author: String? = null
    ): List<TeamPattern> {
        return state.teamPatterns.filter { pattern ->
            (category == null || pattern.category == category) &&
            (model == null || pattern.model == model) &&
            (status == null || pattern.status == status) &&
            (author == null || pattern.author == author)
        }
    }

    fun addTeamMember(member: TeamMember) {
        state.teamMembers.add(member)
    }

    fun removeTeamMember(memberId: String) {
        state.teamMembers.removeIf { it.id == memberId }
    }

    fun getTeamMember(memberId: String): TeamMember? {
        return state.teamMembers.find { it.id == memberId }
    }

    fun getTeamMembers(role: TeamRole? = null): List<TeamMember> {
        return state.teamMembers.filter { member ->
            role == null || member.role == role
        }
    }

    fun addPatternReview(review: PatternReview) {
        state.patternReviews.add(review)
        val pattern = getTeamPattern(review.patternId)
        if (pattern != null) {
            pattern.reviews.add(review)
            updatePatternStatus(pattern.id, review.status)
        }
    }

    fun getPatternReviews(patternId: String): List<PatternReview> {
        return state.patternReviews.filter { it.patternId == patternId }
    }

    private fun updatePatternStatus(patternId: String, reviewStatus: ReviewStatus) {
        val pattern = getTeamPattern(patternId) ?: return
        val newStatus = when (reviewStatus) {
            ReviewStatus.APPROVED -> PatternStatus.APPROVED
            ReviewStatus.REJECTED -> PatternStatus.REJECTED
            ReviewStatus.NEEDS_REVISION -> PatternStatus.DRAFT
        }
        updateTeamPattern(pattern.copy(status = newStatus))
    }

    fun syncWithPatternLibrary() {
        val patternLibrary = PromptPatternLibrary.getInstance(project)
        state.teamPatterns.filter { it.status == PatternStatus.APPROVED }.forEach { teamPattern ->
            patternLibrary.addPattern(
                PromptPatternLibrary.PromptPattern(
                    name = teamPattern.name,
                    description = teamPattern.description,
                    template = teamPattern.template,
                    category = teamPattern.category,
                    model = teamPattern.model,
                    tags = teamPattern.tags
                )
            )
        }
    }

    companion object {
        fun getInstance(project: Project): TeamPatternManager {
            return project.getService(TeamPatternManager::class.java)
        }
    }
}
