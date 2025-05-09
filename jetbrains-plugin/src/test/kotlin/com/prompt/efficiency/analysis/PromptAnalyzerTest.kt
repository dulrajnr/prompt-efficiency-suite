package com.prompt.efficiency.analysis

import com.intellij.testFramework.LightPlatformTestCase
import com.prompt.efficiency.api.PromptEfficiencyApiClient
import com.prompt.efficiency.patterns.PromptPatternLibrary
import com.prompt.efficiency.settings.PromptEfficiencySettings
import org.mockito.Mockito.*
import org.mockito.Mockito.`when` as whenever

class PromptAnalyzerTest : LightPlatformTestCase() {
    private lateinit var analyzer: PromptAnalyzer
    private lateinit var apiClient: PromptEfficiencyApiClient
    private lateinit var settings: PromptEfficiencySettings
    private lateinit var patternLibrary: PromptPatternLibrary

    override fun setUp() {
        super.setUp()
        apiClient = mock(PromptEfficiencyApiClient::class.java)
        settings = mock(PromptEfficiencySettings::class.java)
        patternLibrary = mock(PromptPatternLibrary::class.java)
        analyzer = PromptAnalyzer(project)
    }

    fun testAnalyzePrompt() {
        // Given
        val prompt = """
            Task: Analyze the following code for potential bugs.
            Context: This is a critical production system.
            Expected Output: List of potential issues with severity levels.
        """.trimIndent()

        val context = PromptContext(
            projectType = "java",
            currentTask = "code review",
            selectedModel = "gpt-4",
            availableContext = mapOf(
                "domain_terms" to "bug,issue,error,exception",
                "project_context" to "production,critical,high-availability"
            )
        )

        val basicAnalysis = PromptEfficiencyApiClient.AnalysisResult(
            tokenCount = 50,
            estimatedCost = 0.01,
            suggestions = emptyList(),
            complexity = "medium",
            readability = "high"
        )

        whenever(apiClient.analyzePrompt(prompt)).thenReturn(basicAnalysis)
        whenever(patternLibrary.findPatterns(prompt, "general", "gpt-4")).thenReturn(emptyList())

        // When
        val result = analyzer.analyzePrompt(prompt, context)

        // Then
        assertNotNull(result)
        assertEquals(50, result.basicMetrics.tokenCount)
        assertEquals(0.01, result.basicMetrics.estimatedCost)
        assertEquals("medium", result.basicMetrics.complexity)
        assertEquals("high", result.basicMetrics.readability)
    }

    fun testQualityMetrics() {
        // Given
        val prompt = """
            Task: Write a function to calculate the Fibonacci sequence.
            Context: This is for a performance-critical application.
            Expected Output: Optimized implementation with time complexity analysis.
        """.trimIndent()

        // When
        val result = analyzer.analyzePrompt(prompt, createTestContext())

        // Then
        assertTrue(result.qualityMetrics.clarity > 0.7)
        assertTrue(result.qualityMetrics.specificity > 0.6)
        assertTrue(result.qualityMetrics.consistency > 0.7)
        assertTrue(result.qualityMetrics.completeness > 0.7)
        assertTrue(result.qualityMetrics.suggestions.isEmpty())
    }

    fun testContextMetrics() {
        // Given
        val prompt = """
            Task: Fix the bug in the production system.
            Context: The system is experiencing high latency.
            Expected Output: Root cause analysis and fix.
        """.trimIndent()

        val context = PromptContext(
            projectType = "java",
            currentTask = "bug fix",
            selectedModel = "gpt-4",
            availableContext = mapOf(
                "domain_terms" to "bug,latency,performance",
                "project_context" to "production,high-availability"
            )
        )

        // When
        val result = analyzer.analyzePrompt(prompt, context)

        // Then
        assertTrue(result.contextMetrics.domainRelevance > 0.7)
        assertTrue(result.contextMetrics.taskAlignment > 0.7)
        assertTrue(result.contextMetrics.modelCompatibility > 0.6)
        assertTrue(result.contextMetrics.contextAwareness > 0.7)
    }

    fun testBestPractices() {
        // Given
        val prompt = "maybe you could help me with this task"

        // When
        val result = analyzer.analyzePrompt(prompt, createTestContext())

        // Then
        assertTrue(result.bestPractices.any { it.name == "Clear Task Definition" })
        assertTrue(result.bestPractices.any { it.name == "Clear Instructions" })
        assertTrue(result.bestPractices.any { it.severity == PromptAnalyzer.Severity.ERROR })
    }

    fun testPatternMatching() {
        // Given
        val prompt = """
            Task: Implement a sorting algorithm.
            Context: Need to sort a large dataset efficiently.
            Expected Output: Implementation with performance analysis.
        """.trimIndent()

        val pattern = PromptPatternLibrary.PromptPattern(
            name = "Algorithm Implementation",
            description = "Template for implementing algorithms",
            template = "Task: Implement a {algorithm} algorithm. Context: {context}. Expected Output: {output}",
            category = "general",
            model = "gpt-4"
        )

        whenever(patternLibrary.findPatterns(prompt, "general", "gpt-4"))
            .thenReturn(listOf(pattern))

        // When
        val result = analyzer.analyzePrompt(prompt, createTestContext())

        // Then
        assertTrue(result.patterns.isNotEmpty())
        assertTrue(result.patterns.any { it.pattern == "Algorithm Implementation" })
        assertTrue(result.patterns.any { it.confidence > 0.5 })
    }

    fun testLowQualityPrompt() {
        // Given
        val prompt = "help me with this"

        // When
        val result = analyzer.analyzePrompt(prompt, createTestContext())

        // Then
        assertTrue(result.qualityMetrics.clarity < 0.5)
        assertTrue(result.qualityMetrics.specificity < 0.5)
        assertTrue(result.qualityMetrics.completeness < 0.5)
        assertTrue(result.qualityMetrics.suggestions.isNotEmpty())
    }

    fun testModelSpecificBestPractices() {
        // Given
        val longPrompt = "Task: " + "a".repeat(1000)
        val context = PromptContext(
            projectType = "java",
            currentTask = "code review",
            selectedModel = "gpt-3.5-turbo",
            availableContext = emptyMap()
        )

        // When
        val result = analyzer.analyzePrompt(longPrompt, context)

        // Then
        assertTrue(result.bestPractices.any { it.name == "Conciseness" })
        assertTrue(result.contextMetrics.modelCompatibility < 0.5)
    }

    private fun createTestContext() = PromptContext(
        projectType = "java",
        currentTask = "code review",
        selectedModel = "gpt-4",
        availableContext = mapOf(
            "domain_terms" to "code,review,analysis",
            "project_context" to "development,testing"
        )
    )
} 