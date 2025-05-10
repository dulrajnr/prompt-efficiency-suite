package com.prompt.efficiency.integration

import com.intellij.testFramework.LightPlatformTestCase
import com.prompt.efficiency.analytics.CostAnalytics
import com.prompt.efficiency.collab.TeamPatternManager
import com.prompt.efficiency.patterns.PromptPatternLibrary
import java.time.LocalDateTime
import java.util.*
import kotlin.system.measureTimeMillis

class PerformanceTest : LightPlatformTestCase() {
    private lateinit var patternLibrary: PromptPatternLibrary
    private lateinit var teamPatternManager: TeamPatternManager
    private lateinit var costAnalytics: CostAnalytics

    override fun setUp() {
        super.setUp()
        patternLibrary = PromptPatternLibrary.getInstance(project)
        teamPatternManager = TeamPatternManager.getInstance(project)
        costAnalytics = CostAnalytics.getInstance(project)
    }

    fun testLargePatternLibrary() {
        val numPatterns = 1000
        val time = measureTimeMillis {
            // Add patterns
            repeat(numPatterns) { i ->
                val pattern = TeamPatternManager.TeamPattern(
                    name = "Pattern $i",
                    description = "Description $i",
                    template = "Template $i",
                    category = "Category ${i % 10}",
                    model = if (i % 2 == 0) "gpt-4" else "gpt-3.5-turbo",
                    tags = setOf("tag${i % 5}"),
                    author = "User ${i % 3}"
                )
                teamPatternManager.addTeamPattern(pattern)
            }

            // Test pattern retrieval
            val patterns = teamPatternManager.getTeamPatterns()
            assertEquals(numPatterns, patterns.size)

            // Test filtering
            val filteredPatterns = teamPatternManager.getTeamPatterns(
                category = "Category 0",
                model = "gpt-4"
            )
            assertTrue(filteredPatterns.isNotEmpty())
        }

        println("Large pattern library test completed in $time ms")
        assertTrue("Operation should complete within 5 seconds", time < 5000)
    }

    fun testLargeUsageHistory() {
        val numRecords = 10000
        val patternId = UUID.randomUUID().toString()
        val time = measureTimeMillis {
            // Add usage records
            repeat(numRecords) { i ->
                costAnalytics.addUsageRecord(
                    CostAnalytics.UsageRecord(
                        model = if (i % 2 == 0) "gpt-4" else "gpt-3.5-turbo",
                        promptTokens = 100,
                        completionTokens = 50,
                        cost = 0.006,
                        patternId = patternId,
                        timestamp = LocalDateTime.now().minusDays(i.toLong())
                    )
                )
            }

            // Test statistics calculation
            val stats = costAnalytics.getUsageStats()
            assertEquals(numRecords, stats.totalPrompts)
            assertEquals(numRecords * 0.006, stats.totalCost)
            assertEquals(numRecords * 150, stats.totalTokens)

            // Test pattern usage
            assertEquals(numRecords, stats.usageByPattern[patternId])

            // Test model usage
            assertEquals(numRecords / 2, stats.usageByModel["gpt-4"])
            assertEquals(numRecords / 2, stats.usageByModel["gpt-3.5-turbo"])
        }

        println("Large usage history test completed in $time ms")
        assertTrue("Operation should complete within 10 seconds", time < 10000)
    }

    fun testConcurrentOperations() {
        val numThreads = 10
        val operationsPerThread = 100
        val time = measureTimeMillis {
            val threads = List(numThreads) { threadId ->
                Thread {
                    repeat(operationsPerThread) { i ->
                        // Add pattern
                        val pattern = TeamPatternManager.TeamPattern(
                            name = "Pattern $threadId-$i",
                            description = "Description $threadId-$i",
                            template = "Template $threadId-$i",
                            category = "Category $threadId",
                            model = "gpt-4",
                            tags = setOf("tag$threadId"),
                            author = "User $threadId"
                        )
                        teamPatternManager.addTeamPattern(pattern)

                        // Add usage record
                        costAnalytics.addUsageRecord(
                            CostAnalytics.UsageRecord(
                                model = "gpt-4",
                                promptTokens = 100,
                                completionTokens = 50,
                                cost = 0.006,
                                patternId = pattern.id,
                                timestamp = LocalDateTime.now()
                            )
                        )
                    }
                }
            }

            // Start all threads
            threads.forEach { it.start() }

            // Wait for all threads to complete
            threads.forEach { it.join() }

            // Verify results
            val patterns = teamPatternManager.getTeamPatterns()
            assertEquals(numThreads * operationsPerThread, patterns.size)

            val stats = costAnalytics.getUsageStats()
            assertEquals(numThreads * operationsPerThread, stats.totalPrompts)
        }

        println("Concurrent operations test completed in $time ms")
        assertTrue("Operation should complete within 15 seconds", time < 15000)
    }

    fun testPatternSearchPerformance() {
        // Add patterns with various names and categories
        repeat(1000) { i ->
            val pattern = TeamPatternManager.TeamPattern(
                name = "Pattern ${UUID.randomUUID()}",
                description = "Description $i",
                template = "Template $i",
                category = "Category ${i % 20}",
                model = "gpt-4",
                tags = setOf("tag${i % 10}"),
                author = "User ${i % 5}"
            )
            teamPatternManager.addTeamPattern(pattern)
        }

        val time = measureTimeMillis {
            // Test various search combinations
            val results1 = teamPatternManager.getTeamPatterns(category = "Category 0")
            val results2 = teamPatternManager.getTeamPatterns(model = "gpt-4")
            val results3 = teamPatternManager.getTeamPatterns(
                category = "Category 0",
                model = "gpt-4"
            )

            assertTrue(results1.isNotEmpty())
            assertTrue(results2.isNotEmpty())
            assertTrue(results3.isNotEmpty())
        }

        println("Pattern search test completed in $time ms")
        assertTrue("Search should complete within 1 second", time < 1000)
    }
}
