package com.prompt.efficiency.patterns

import com.intellij.testFramework.LightPlatformTestCase
import java.util.UUID

class PromptPatternLibraryTest : LightPlatformTestCase() {
    private lateinit var library: PromptPatternLibrary

    override fun setUp() {
        super.setUp()
        library = PromptPatternLibrary.getInstance(project)
    }

    fun testAddAndFindPattern() {
        // Given
        val pattern = createTestPattern(
            name = "Code Review",
            template = "Review the following code:\n{code}\nFocus on: {aspects}",
            category = "code",
            model = "gpt-4"
        )

        // When
        library.addPattern(pattern)
        val foundPatterns = library.findPatterns(
            prompt = "Review the following code:\nfunction test() {}\nFocus on: security",
            category = "code",
            model = "gpt-4"
        )

        // Then
        assertTrue(foundPatterns.isNotEmpty())
        assertEquals(pattern.id, foundPatterns.first().id)
    }

    fun testPatternMatching() {
        // Given
        val pattern = createTestPattern(
            name = "Task Definition",
            template = "Task: {task}\nContext: {context}\nExpected Output: {output}",
            category = "general",
            model = "gpt-4"
        )
        library.addPattern(pattern)

        // When
        val prompt = """
            Task: Implement a sorting algorithm
            Context: Need to sort a large dataset
            Expected Output: Optimized implementation
        """.trimIndent()

        val matches = library.findPatterns(prompt, "general", "gpt-4")

        // Then
        assertTrue(matches.isNotEmpty())
        assertEquals(pattern.id, matches.first().id)
    }

    fun testExtractVariables() {
        // Given
        val pattern = createTestPattern(
            name = "Code Analysis",
            template = "Analyze {language} code for {issues}",
            category = "code",
            model = "gpt-4"
        )
        library.addPattern(pattern)

        // When
        val variables = library.extractVariables(
            prompt = "Analyze Python code for security issues",
            pattern = pattern
        )

        // Then
        assertEquals("Python", variables["language"])
        assertEquals("security issues", variables["issues"])
    }

    fun testPatternSuggestions() {
        // Given
        val pattern1 = createTestPattern(
            name = "Code Review",
            template = "Review {language} code for {aspects}",
            category = "code",
            model = "gpt-4"
        )
        val pattern2 = createTestPattern(
            name = "Bug Fix",
            template = "Fix {issue} in {language} code",
            category = "code",
            model = "gpt-4"
        )
        library.addPattern(pattern1)
        library.addPattern(pattern2)

        // When
        val suggestions = library.suggestPatterns(
            prompt = "Review Python code for security issues",
            model = "gpt-4"
        )

        // Then
        assertTrue(suggestions.isNotEmpty())
        assertTrue(suggestions.any { it.pattern.id == pattern1.id })
        assertTrue(suggestions.first().confidence > 0.5)
    }

    fun testUpdatePatternStats() {
        // Given
        val pattern = createTestPattern(
            name = "Test Pattern",
            template = "Test {input}",
            category = "testing",
            model = "gpt-4"
        )
        library.addPattern(pattern)

        // When
        library.updatePatternStats(pattern.id, true)
        library.updatePatternStats(pattern.id, false)
        library.updatePatternStats(pattern.id, true)

        // Then
        val updatedPattern = library.findPatterns("Test something", "testing", "gpt-4").first()
        assertEquals(3, updatedPattern.usageCount)
        assertTrue(updatedPattern.successRate in 0.6..0.7) // 2/3 success rate
    }

    fun testGetPatternsByCategory() {
        // Given
        val pattern1 = createTestPattern(
            name = "Code Pattern",
            template = "Code {action}",
            category = "code",
            model = "gpt-4"
        )
        val pattern2 = createTestPattern(
            name = "Doc Pattern",
            template = "Document {topic}",
            category = "documentation",
            model = "gpt-4"
        )
        library.addPattern(pattern1)
        library.addPattern(pattern2)

        // When
        val codePatterns = library.getPatternsByCategory("code")
        val docPatterns = library.getPatternsByCategory("documentation")

        // Then
        assertEquals(1, codePatterns.size)
        assertEquals(pattern1.id, codePatterns.first().id)
        assertEquals(1, docPatterns.size)
        assertEquals(pattern2.id, docPatterns.first().id)
    }

    fun testGetPatternsByModel() {
        // Given
        val pattern1 = createTestPattern(
            name = "GPT-4 Pattern",
            template = "GPT-4 {task}",
            category = "general",
            model = "gpt-4"
        )
        val pattern2 = createTestPattern(
            name = "General Pattern",
            template = "General {task}",
            category = "general",
            model = "general"
        )
        library.addPattern(pattern1)
        library.addPattern(pattern2)

        // When
        val gpt4Patterns = library.getPatternsByModel("gpt-4")

        // Then
        assertEquals(2, gpt4Patterns.size) // Should include both gpt-4 and general patterns
        assertTrue(gpt4Patterns.any { it.id == pattern1.id })
        assertTrue(gpt4Patterns.any { it.id == pattern2.id })
    }

    fun testGetPatternsByTags() {
        // Given
        val pattern1 = createTestPattern(
            name = "Security Pattern",
            template = "Check {code} for security",
            category = "code",
            model = "gpt-4",
            tags = setOf("security", "code-review")
        )
        val pattern2 = createTestPattern(
            name = "Performance Pattern",
            template = "Optimize {code} for performance",
            category = "code",
            model = "gpt-4",
            tags = setOf("performance", "optimization")
        )
        library.addPattern(pattern1)
        library.addPattern(pattern2)

        // When
        val securityPatterns = library.getPatternsByTags(setOf("security"))
        val performancePatterns = library.getPatternsByTags(setOf("performance"))

        // Then
        assertEquals(1, securityPatterns.size)
        assertEquals(pattern1.id, securityPatterns.first().id)
        assertEquals(1, performancePatterns.size)
        assertEquals(pattern2.id, performancePatterns.first().id)
    }

    private fun createTestPattern(
        name: String,
        template: String,
        category: String,
        model: String,
        tags: Set<String> = emptySet()
    ): PromptPatternLibrary.PromptPattern {
        return PromptPatternLibrary.PromptPattern(
            id = UUID.randomUUID().toString(),
            name = name,
            description = "Test pattern for $name",
            template = template,
            category = category,
            model = model,
            tags = tags.toMutableSet()
        )
    }
} 