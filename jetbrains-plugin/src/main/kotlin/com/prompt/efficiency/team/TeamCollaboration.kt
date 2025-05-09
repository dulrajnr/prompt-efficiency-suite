package com.prompt.efficiency.team

import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import com.prompt.efficiency.analytics.CostAnalytics
import com.prompt.efficiency.patterns.PromptPatternLibrary
import java.time.LocalDateTime
import java.util.concurrent.ConcurrentHashMap

@Service
class TeamCollaboration(private val project: Project) {
    private val costAnalytics = CostAnalytics(project)
    private val patternLibrary = PromptPatternLibrary(project)

    private val teamMembers = ConcurrentHashMap<String, TeamMember>()
    private val teamPatterns = ConcurrentHashMap<String, MutableList<TeamPattern>>()
    private val teamAnalytics = ConcurrentHashMap<String, TeamAnalytics>()

    data class TeamMember(
        val id: String,
        val name: String,
        val role: TeamRole,
        val permissions: Set<Permission>,
        val joinDate: LocalDateTime
    )

    data class TeamPattern(
        val id: String,
        val name: String,
        val description: String,
        val pattern: PromptPatternLibrary.PromptPattern,
        val createdBy: String,
        val createdAt: LocalDateTime,
        val lastModifiedBy: String,
        val lastModifiedAt: LocalDateTime,
        val usageCount: Int,
        val averageCost: Double,
        val ratings: List<Rating>
    )

    data class TeamAnalytics(
        val teamId: String,
        val totalCost: Double,
        val costByMember: Map<String, Double>,
        val costByPattern: Map<String, Double>,
        val usageByMember: Map<String, Int>,
        val usageByPattern: Map<String, Int>,
        val bestPractices: List<BestPractice>,
        val trends: List<TeamTrend>
    )

    data class Rating(
        val userId: String,
        val score: Int,
        val comment: String,
        val timestamp: LocalDateTime
    )

    data class BestPractice(
        val name: String,
        val description: String,
        val impact: Double,
        val implementation: String
    )

    data class TeamTrend(
        val timestamp: LocalDateTime,
        val metric: String,
        val value: Double
    )

    enum class TeamRole {
        ADMIN,
        LEADER,
        MEMBER,
        VIEWER
    }

    enum class Permission {
        CREATE_PATTERN,
        EDIT_PATTERN,
        DELETE_PATTERN,
        SHARE_PATTERN,
        VIEW_ANALYTICS,
        MANAGE_MEMBERS,
        SET_BUDGETS
    }

    fun addTeamMember(member: TeamMember) {
        teamMembers[member.id] = member
        initializeMemberAnalytics(member.id)
    }

    fun sharePattern(pattern: TeamPattern, withMemberId: String) {
        val member = teamMembers[withMemberId] ?: return
        if (Permission.SHARE_PATTERN in member.permissions) {
            teamPatterns.getOrPut(withMemberId) { mutableListOf() }.add(pattern)
        }
    }

    fun getTeamAnalytics(teamId: String): TeamAnalytics {
        return teamAnalytics[teamId] ?: createTeamAnalytics(teamId)
    }

    fun updatePatternRating(patternId: String, rating: Rating) {
        val pattern = findPattern(patternId) ?: return
        pattern.ratings.add(rating)
        updatePatternAnalytics(pattern)
    }

    fun getBestPractices(teamId: String): List<BestPractice> {
        val analytics = getTeamAnalytics(teamId)
        return analytics.bestPractices
    }

    fun getTeamTrends(teamId: String, metric: String): List<TeamTrend> {
        val analytics = getTeamAnalytics(teamId)
        return analytics.trends.filter { it.metric == metric }
    }

    private fun initializeMemberAnalytics(memberId: String) {
        teamAnalytics[memberId] = TeamAnalytics(
            teamId = memberId,
            totalCost = 0.0,
            costByMember = emptyMap(),
            costByPattern = emptyMap(),
            usageByMember = emptyMap(),
            usageByPattern = emptyMap(),
            bestPractices = emptyList(),
            trends = emptyList()
        )
    }

    private fun createTeamAnalytics(teamId: String): TeamAnalytics {
        // TODO: Implement team analytics creation
        return TeamAnalytics(
            teamId = teamId,
            totalCost = 0.0,
            costByMember = emptyMap(),
            costByPattern = emptyMap(),
            usageByMember = emptyMap(),
            usageByPattern = emptyMap(),
            bestPractices = emptyList(),
            trends = emptyList()
        )
    }

    private fun findPattern(patternId: String): TeamPattern? {
        return teamPatterns.values.flatten().find { it.id == patternId }
    }

    private fun updatePatternAnalytics(pattern: TeamPattern) {
        // TODO: Implement pattern analytics update
    }
} 