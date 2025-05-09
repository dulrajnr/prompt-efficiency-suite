package com.prompt.efficiency.dev

import com.intellij.testFramework.LightPlatformTestCase
import com.intellij.testFramework.fixtures.LightPlatformCodeInsightFixtureTestCase
import com.prompt.efficiency.analysis.PromptAnalyzer
import com.prompt.efficiency.patterns.PromptPatternLibrary
import com.prompt.efficiency.settings.PromptEfficiencySettings

class DevExperienceTest : LightPlatformCodeInsightFixtureTestCase() {
    private lateinit var analyzer: PromptAnalyzer
    private lateinit var patternLibrary: PromptPatternLibrary
    private lateinit var settings: PromptEfficiencySettings

    override fun setUp() {
        super.setUp()
        analyzer = PromptAnalyzer.getInstance(project)
        patternLibrary = PromptPatternLibrary.getInstance(project)
        settings = PromptEfficiencySettings.getInstance(project)
    }

    fun testCompletionProvider() {
        // Create a test prompt file
        myFixture.configureByText(
            "test.prompt",
            """
            |Write a function that calculates the factorial of a number.
            |
            """.trimMargin()
        )

        // Trigger completion
        myFixture.completeBasic()

        // Verify completion items
        val items = myFixture.lookupElements ?: return
        assertTrue(items.any { it.lookupString.contains("Example") })
        assertTrue(items.any { it.lookupString.contains("Constraints") })
        assertTrue(items.any { it.lookupString.contains("Error Handling") })
    }

    fun testQuickFixes() {
        // Create a test prompt file with issues
        myFixture.configureByText(
            "test.prompt",
            """
            |Write a function that calculates the factorial of a number.
            |
            """.trimMargin()
        )

        // Get quick fixes
        val quickFixes = myFixture.getAvailableIntentions()
        assertTrue(quickFixes.any { it.text.contains("Add examples") })
        assertTrue(quickFixes.any { it.text.contains("Add constraints") })
        assertTrue(quickFixes.any { it.text.contains("Add error handling") })

        // Apply a quick fix
        val addExamplesFix = quickFixes.find { it.text.contains("Add examples") }
        assertNotNull(addExamplesFix)
        addExamplesFix?.invoke(project, myFixture.editor, myFixture.file)

        // Verify the fix was applied
        assertTrue(myFixture.file.text.contains("Here are some examples:"))
    }

    fun testInspections() {
        // Create a test prompt file with issues
        myFixture.configureByText(
            "test.prompt",
            """
            |Write a function that calculates the factorial of a number.
            |
            """.trimMargin()
        )

        // Run inspections
        myFixture.enableInspections(PromptInspectionProvider::class.java)
        myFixture.checkHighlighting()

        // Verify inspection results
        val highlights = myFixture.doHighlighting()
        assertTrue(highlights.any { it.description.contains("AMBIGUOUS_INSTRUCTIONS") })
        assertTrue(highlights.any { it.description.contains("INSUFFICIENT_CONTEXT") })
        assertTrue(highlights.any { it.description.contains("INSUFFICIENT_CONSTRAINTS") })
    }

    fun testPatternSuggestions() {
        // Add a test pattern
        val patternId = patternLibrary.addPattern(
            PromptPatternLibrary.PromptPattern(
                name = "Function Documentation",
                description = "Template for documenting functions",
                template = """
                    |Function: [function name]
                    |Purpose: [purpose]
                    |Parameters:
                    |- [param1]: [description]
                    |- [param2]: [description]
                    |Returns: [return value description]
                    |Examples:
                    |1. [example 1]
                    |2. [example 2]
                    |
                """.trimMargin(),
                category = "Documentation",
                model = "gpt-4",
                tags = setOf("function", "documentation")
            )
        )

        // Create a test prompt file
        myFixture.configureByText(
            "test.prompt",
            """
            |Document the following function:
            |def calculate_factorial(n):
            |    if n == 0:
            |        return 1
            |    return n * calculate_factorial(n - 1)
            |
            """.trimMargin()
        )

        // Run inspections
        myFixture.enableInspections(PromptInspectionProvider::class.java)
        myFixture.checkHighlighting()

        // Verify pattern suggestion
        val highlights = myFixture.doHighlighting()
        assertTrue(highlights.any { it.description.contains("Consider using pattern: Function Documentation") })
    }

    fun testModelCompatibility() {
        // Set model settings
        settings.setDefaultModel("gpt-4")
        settings.addModelSettings(
            PromptEfficiencySettings.ModelSettings(
                model = "gpt-4",
                maxTokens = 100,
                temperature = 0.7,
                topP = 1.0
            )
        )

        // Create a test prompt file that exceeds token limit
        myFixture.configureByText(
            "test.prompt",
            "x".repeat(200) // This will exceed the token limit
        )

        // Run inspections
        myFixture.enableInspections(PromptInspectionProvider::class.java)
        myFixture.checkHighlighting()

        // Verify model compatibility warning
        val highlights = myFixture.doHighlighting()
        assertTrue(highlights.any { it.description.contains("exceeds model's token limit") })
    }
} 