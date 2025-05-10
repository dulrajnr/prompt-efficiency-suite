package com.prompt.efficiency.api

import com.intellij.testFramework.LightPlatformTestCase
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.After
import org.junit.Before
import org.junit.Test
import java.io.IOException

class PromptEfficiencyApiClientTest : LightPlatformTestCase() {
    private lateinit var mockWebServer: MockWebServer
    private lateinit var apiClient: PromptEfficiencyApiClient

    @Before
    override fun setUp() {
        super.setUp()
        mockWebServer = MockWebServer()
        apiClient = PromptEfficiencyApiClient()
    }

    @After
    fun tearDown() {
        mockWebServer.shutdown()
    }

    @Test
    fun testAnalyzePrompt() {
        val responseJson = """
            {
                "token_count": 100,
                "estimated_cost": 0.002,
                "suggestions": ["Be more specific", "Use fewer tokens"],
                "complexity": "medium",
                "readability": "good"
            }
        """.trimIndent()

        mockWebServer.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson))

        val result = apiClient.analyzePrompt("Test prompt")

        assertEquals(100, result.tokenCount)
        assertEquals(0.002, result.estimatedCost)
        assertEquals(2, result.suggestions.size)
        assertEquals("medium", result.complexity)
        assertEquals("good", result.readability)
    }

    @Test
    fun testOptimizePrompt() {
        val responseJson = """
            {
                "optimized_prompt": "Optimized test prompt",
                "token_reduction": 20,
                "cost_reduction": 0.001,
                "improvements": ["Removed redundancy", "Simplified structure"]
            }
        """.trimIndent()

        mockWebServer.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson))

        val result = apiClient.optimizePrompt("Test prompt")

        assertEquals("Optimized test prompt", result.optimizedPrompt)
        assertEquals(20, result.tokenReduction)
        assertEquals(0.001, result.costReduction)
        assertEquals(2, result.improvements.size)
    }

    @Test
    fun testEstimateCost() {
        val responseJson = """
            {
                "token_count": 150,
                "estimated_cost": 0.003,
                "currency": "USD",
                "model": "gpt-4"
            }
        """.trimIndent()

        mockWebServer.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson))

        val result = apiClient.estimateCost("Test prompt", "gpt-4")

        assertEquals(150, result.tokenCount)
        assertEquals(0.003, result.estimatedCost)
        assertEquals("USD", result.currency)
        assertEquals("gpt-4", result.model)
    }

    @Test
    fun testScanRepository() {
        val responseJson = """
            {
                "total_prompts": 10,
                "total_tokens": 1000,
                "estimated_cost": 0.02,
                "prompts_by_file": {
                    "file1.txt": 5,
                    "file2.txt": 5
                },
                "suggestions": ["Optimize file1.txt", "Review file2.txt"]
            }
        """.trimIndent()

        mockWebServer.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson))

        val result = apiClient.scanRepository("/test/path")

        assertEquals(10, result.totalPrompts)
        assertEquals(1000, result.totalTokens)
        assertEquals(0.02, result.estimatedCost)
        assertEquals(2, result.promptsByFile.size)
        assertEquals(2, result.suggestions.size)
    }

    @Test
    fun testTranslatePrompt() {
        val responseJson = """
            {
                "translated_prompt": "Test prompt translated",
                "source_language": "en",
                "target_language": "es",
                "confidence": 0.95
            }
        """.trimIndent()

        mockWebServer.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson))

        val result = apiClient.translatePrompt("Test prompt", "es")

        assertEquals("Test prompt translated", result.translatedPrompt)
        assertEquals("en", result.sourceLanguage)
        assertEquals("es", result.targetLanguage)
        assertEquals(0.95, result.confidence)
    }

    @Test(expected = IOException::class)
    fun testErrorHandling() {
        mockWebServer.enqueue(MockResponse()
            .setResponseCode(401)
            .setBody("Unauthorized"))

        apiClient.analyzePrompt("Test prompt")
    }

    @Test(expected = IOException::class)
    fun testTimeoutHandling() {
        mockWebServer.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody("{}")
            .setHeadersDelay(31, TimeUnit.SECONDS))

        apiClient.analyzePrompt("Test prompt")
    }

    @Test(expected = IOException::class)
    fun testInvalidResponseHandling() {
        mockWebServer.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody("invalid json"))

        apiClient.analyzePrompt("Test prompt")
    }
}
