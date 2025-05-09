package com.prompt.efficiency.integration

import com.intellij.testFramework.LightPlatformTestCase
import com.prompt.efficiency.analytics.CostAnalytics
import com.prompt.efficiency.collab.TeamPatternManager
import com.prompt.efficiency.patterns.PromptPatternLibrary
import com.prompt.efficiency.settings.PromptEfficiencySettings
import java.time.LocalDateTime
import java.util.*

class PromptEfficiencyIntegrationTest : LightPlatformTestCase() {
    private lateinit var settings: PromptEfficiencySettings
    private lateinit var patternLibrary: PromptPatternLibrary
    private lateinit var teamPatternManager: TeamPatternManager
    private lateinit var costAnalytics: CostAnalytics

    override fun setUp() {
        super.setUp()
        settings = PromptEfficiencySettings.getInstance(project)
        patternLibrary = PromptPatternLibrary.getInstance(project)
        teamPatternManager = TeamPatternManager.getInstance(project)
        costAnalytics = CostAnalytics.getInstance(project)

        // Configure settings
        settings.setModelSettings(listOf(
            PromptEfficiencySettings.ModelSetting("gpt-4", 8192, 0.03, 0.06),
            PromptEfficiencySettings.ModelSetting("gpt-3.5-turbo", 4096, 0.0015, 0.002)
        ))
        settings.setCostLimits(
            dailyLimit = 10.0,
            monthlyLimit = 100.0
        )
    }

    fun testCompleteWorkflow() {
        // 1. Add a team pattern
        val teamPattern = TeamPatternManager.TeamPattern(
            name = "Test Pattern",
            description = "Test Description",
            template = "You are a helpful assistant. Please help with: {{task}}",
            category = "General",
            model = "gpt-4",
            tags = setOf("test", "general"),
            author = "Test User"
        )
        teamPatternManager.addTeamPattern(teamPattern)

        // 2. Submit for review
        teamPatternManager.updateTeamPattern(teamPattern.copy(
            status = TeamPatternManager.PatternStatus.PENDING_REVIEW
        ))

        // 3. Add a review
        val review = TeamPatternManager.PatternReview(
            patternId = teamPattern.id,
            reviewerId = "Reviewer",
            status = TeamPatternManager.ReviewStatus.APPROVED,
            comments = "Good pattern"
        )
        teamPatternManager.addPatternReview(review)

        // 4. Sync with pattern library
        teamPatternManager.syncWithPatternLibrary()

        // 5. Verify pattern in library
        val libraryPattern = patternLibrary.getPatterns().find { it.name == teamPattern.name }
        assertNotNull("Pattern should be in library", libraryPattern)
        assertEquals(teamPattern.template, libraryPattern?.template)

        // 6. Record usage
        val usageRecord = CostAnalytics.UsageRecord(
            model = "gpt-4",
            promptTokens = 100,
            completionTokens = 50,
            cost = 0.006,
            patternId = teamPattern.id,
            timestamp = LocalDateTime.now()
        )
        costAnalytics.addUsageRecord(usageRecord)

        // 7. Check usage stats
        val stats = costAnalytics.getUsageStats()
        assertEquals(1, stats.totalPrompts)
        assertEquals(0.006, stats.totalCost)
        assertEquals(150, stats.totalTokens)
        assertEquals(1, stats.usageByPattern[teamPattern.id])

        // 8. Check cost alerts
        val alerts = costAnalytics.getAlerts()
        assertTrue("No alerts should be present", alerts.isEmpty())

        // 9. Add more usage to trigger alert
        repeat(10) {
            costAnalytics.addUsageRecord(usageRecord)
        }

        // 10. Check for alerts
        val newAlerts = costAnalytics.getAlerts()
        assertTrue("Should have alerts", newAlerts.isNotEmpty())
        assertTrue("Should have cost limit alert", newAlerts.any { it.type == CostAnalytics.AlertType.COST_LIMIT })
    }

    fun testPatternLifecycle() {
        // 1. Create pattern
        val pattern = TeamPatternManager.TeamPattern(
            name = "Lifecycle Pattern",
            description = "Test lifecycle",
            template = "Test template",
            category = "Test",
            model = "gpt-4",
            tags = setOf("test"),
            author = "Test User"
        )
        teamPatternManager.addTeamPattern(pattern)

        // 2. Update pattern
        val updatedPattern = pattern.copy(
            description = "Updated description",
            version = 2
        )
        teamPatternManager.updateTeamPattern(updatedPattern)

        // 3. Verify update
        val retrievedPattern = teamPatternManager.getTeamPattern(pattern.id)
        assertEquals("Updated description", retrievedPattern?.description)
        assertEquals(2, retrievedPattern?.version)

        // 4. Delete pattern
        teamPatternManager.deleteTeamPattern(pattern.id)

        // 5. Verify deletion
        assertNull(teamPatternManager.getTeamPattern(pattern.id))
    }

    fun testCostTracking() {
        // 1. Add usage records
        val patternId = UUID.randomUUID().toString()
        repeat(5) {
            costAnalytics.addUsageRecord(
                CostAnalytics.UsageRecord(
                    model = "gpt-4",
                    promptTokens = 100,
                    completionTokens = 50,
                    cost = 0.006,
                    patternId = patternId,
                    timestamp = LocalDateTime.now()
                )
            )
        }

        // 2. Check total usage
        val stats = costAnalytics.getUsageStats()
        assertEquals(5, stats.totalPrompts)
        assertEquals(0.03, stats.totalCost)
        assertEquals(750, stats.totalTokens)

        // 3. Check pattern usage
        assertEquals(5, stats.usageByPattern[patternId])

        // 4. Check model usage
        assertEquals(5, stats.usageByModel["gpt-4"])
    }

    fun testTeamMemberManagement() {
        // 1. Add team members
        val admin = TeamPatternManager.TeamMember(
            name = "Admin User",
            email = "admin@test.com",
            role = TeamPatternManager.TeamRole.ADMIN
        )
        val reviewer = TeamPatternManager.TeamMember(
            name = "Reviewer User",
            email = "reviewer@test.com",
            role = TeamPatternManager.TeamRole.REVIEWER
        )
        teamPatternManager.addTeamMember(admin)
        teamPatternManager.addTeamMember(reviewer)

        // 2. Verify members
        val members = teamPatternManager.getTeamMembers()
        assertEquals(2, members.size)
        assertTrue(members.any { it.role == TeamPatternManager.TeamRole.ADMIN })
        assertTrue(members.any { it.role == TeamPatternManager.TeamRole.REVIEWER })

        // 3. Remove member
        teamPatternManager.removeTeamMember(reviewer.id)

        // 4. Verify removal
        val updatedMembers = teamPatternManager.getTeamMembers()
        assertEquals(1, updatedMembers.size)
        assertEquals(admin.id, updatedMembers[0].id)
    }
} 