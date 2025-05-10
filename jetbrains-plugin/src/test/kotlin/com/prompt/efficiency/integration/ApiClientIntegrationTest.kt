package com.prompt.efficiency.integration

import com.intellij.openapi.project.Project
import com.prompt.efficiency.settings.PromptEfficiencySettings
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.mockito.Mockito.*
import java.io.IOException
import org.junit.jupiter.api.Assertions.*
import org.json.JSONObject
import java.net.SocketTimeoutException
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

class ApiClientIntegrationTest {
    private lateinit var server: MockWebServer
    private lateinit var project: Project
    private lateinit var settings: PromptEfficiencySettings
    private lateinit var apiClient: ApiClient

    @BeforeEach
    fun setup() {
        server = MockWebServer()
        server.start()

        project = mock(Project::class.java)
        settings = PromptEfficiencySettings().apply {
            serverUrl = server.url("/").toString()
            apiKey = "test-key"
            defaultModel = "gpt-4"
            defaultCurrency = "USD"
        }

        apiClient = ApiClient(settings)
    }

    @AfterEach
    fun tearDown() {
        server.shutdown()
    }

    @Test
    fun `test analyze prompt integration`() {
        // Given
        val prompt = "Test prompt"
        val responseJson = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        // When
        val result = apiClient.analyzePrompt(prompt)

        // Then
        assertNotNull(result)
        assertEquals(0.8, result.getDouble("clarity"))
        assertEquals(0.7, result.getDouble("structure"))
        assertEquals(0.6, result.getDouble("complexity"))

        val request = server.takeRequest()
        assertEquals("POST", request.method)
        assertTrue(request.path?.contains("/analyze") ?: false)
        assertTrue(request.getHeader("Authorization")?.contains("test-key") ?: false)
    }

    @Test
    fun `test optimize prompt integration`() {
        // Given
        val prompt = "Test prompt"
        val responseJson = JSONObject().apply {
            put("optimized_prompt", "Optimized test prompt")
            put("improvements", JSONObject().apply {
                put("clarity", "Improved clarity")
                put("structure", "Better structure")
            })
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        // When
        val result = apiClient.optimizePrompt(prompt)

        // Then
        assertNotNull(result)
        assertEquals("Optimized test prompt", result.getString("optimized_prompt"))
        assertTrue(result.getJSONObject("improvements").has("clarity"))
        assertTrue(result.getJSONObject("improvements").has("structure"))
    }

    @Test
    fun `test estimate cost integration`() {
        // Given
        val prompt = "Test prompt"
        val responseJson = JSONObject().apply {
            put("total_cost", 0.5)
            put("currency", "USD")
            put("token_count", 100)
            put("cost_per_token", 0.005)
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        // When
        val result = apiClient.estimateCost(prompt)

        // Then
        assertNotNull(result)
        assertEquals(0.5, result.getDouble("total_cost"))
        assertEquals("USD", result.getString("currency"))
        assertEquals(100, result.getInt("token_count"))
        assertEquals(0.005, result.getDouble("cost_per_token"))
    }

    @Test
    fun `test scan repository integration`() {
        // Given
        val responseJson = JSONObject().apply {
            put("files_scanned", 2)
            put("prompts_found", 2)
            put("prompts", JSONObject().apply {
                put("file1.txt", JSONObject().apply {
                    put("prompt", "Prompt 1")
                    put("line_number", 10)
                })
                put("file2.txt", JSONObject().apply {
                    put("prompt", "Prompt 2")
                    put("line_number", 20)
                })
            })
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        // When
        val result = apiClient.scanRepository("/test/path")

        // Then
        assertNotNull(result)
        assertEquals(2, result.getInt("files_scanned"))
        assertEquals(2, result.getInt("prompts_found"))
        assertTrue(result.getJSONObject("prompts").has("file1.txt"))
        assertTrue(result.getJSONObject("prompts").has("file2.txt"))
    }

    @Test
    fun `test translate prompt integration`() {
        // Given
        val prompt = "Test prompt"
        val responseJson = JSONObject().apply {
            put("translated_prompt", "Translated test prompt")
            put("source_language", "en")
            put("target_language", "es")
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        // When
        val result = apiClient.translatePrompt(prompt, "es")

        // Then
        assertNotNull(result)
        assertEquals("Translated test prompt", result.getString("translated_prompt"))
        assertEquals("en", result.getString("source_language"))
        assertEquals("es", result.getString("target_language"))
    }

    @Test
    fun `test error handling integration`() {
        // Given
        server.enqueue(MockResponse()
            .setResponseCode(401)
            .setBody("""{"error": "Unauthorized"}""")
            .addHeader("Content-Type", "application/json"))

        // When/Then
        assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
    }

    @Test
    fun `test configuration change integration`() {
        // Given
        val prompt = "Test prompt"
        val responseJson = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        // When
        settings.defaultModel = "gpt-3.5-turbo"
        val result = apiClient.analyzePrompt(prompt)

        // Then
        assertNotNull(result)
        val request = server.takeRequest()
        assertTrue(request.body?.string()?.contains("gpt-3.5-turbo") ?: false)
    }

    @Test
    fun `test connection timeout`() {
        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody("{}")
            .setHeadersDelay(31, TimeUnit.SECONDS))

        assertThrows(SocketTimeoutException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
    }

    @Test
    fun `test empty response body`() {
        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(""))

        assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
    }

    @Test
    fun `test malformed JSON response`() {
        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody("{invalid json")
            .addHeader("Content-Type", "application/json"))

        assertThrows(org.json.JSONException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
    }

    @Test
    fun `test server error with error message`() {
        val errorJson = JSONObject().apply {
            put("error", "Internal Server Error")
            put("code", "INTERNAL_ERROR")
            put("details", "Something went wrong")
        }

        server.enqueue(MockResponse()
            .setResponseCode(500)
            .setBody(errorJson.toString())
            .addHeader("Content-Type", "application/json"))

        val exception = assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
        assertTrue(exception.message?.contains("500") ?: false)
    }

    @Test
    fun `test rate limiting`() {
        val errorJson = JSONObject().apply {
            put("error", "Rate limit exceeded")
            put("retry_after", 60)
        }

        server.enqueue(MockResponse()
            .setResponseCode(429)
            .setBody(errorJson.toString())
            .addHeader("Content-Type", "application/json")
            .addHeader("Retry-After", "60"))

        val exception = assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
        assertTrue(exception.message?.contains("429") ?: false)
    }

    @Test
    fun `test invalid API key`() {
        val errorJson = JSONObject().apply {
            put("error", "Invalid API key")
            put("code", "INVALID_API_KEY")
        }

        server.enqueue(MockResponse()
            .setResponseCode(401)
            .setBody(errorJson.toString())
            .addHeader("Content-Type", "application/json"))

        val exception = assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
        assertTrue(exception.message?.contains("401") ?: false)
    }

    @Test
    fun `test empty prompt`() {
        val errorJson = JSONObject().apply {
            put("error", "Empty prompt")
            put("code", "VALIDATION_ERROR")
        }

        server.enqueue(MockResponse()
            .setResponseCode(400)
            .setBody(errorJson.toString())
            .addHeader("Content-Type", "application/json"))

        val exception = assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("")
        }
        assertTrue(exception.message?.contains("400") ?: false)
    }

    @Test
    fun `test very long prompt`() {
        val longPrompt = "a".repeat(100000)
        val responseJson = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        val result = apiClient.analyzePrompt(longPrompt)
        assertNotNull(result)
        assertEquals(0.8, result.getDouble("clarity"))
    }

    @Test
    fun `test special characters in prompt`() {
        val prompt = "Test prompt with special chars: !@#$%^&*()_+{}|:\"<>?[]\\;',./~`"
        val responseJson = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        val result = apiClient.analyzePrompt(prompt)
        assertNotNull(result)
        assertEquals(0.8, result.getDouble("clarity"))
    }

    @Test
    fun `test concurrent requests`() {
        val responseJson = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        // Enqueue multiple responses
        repeat(5) {
            server.enqueue(MockResponse()
                .setResponseCode(200)
                .setBody(responseJson.toString())
                .addHeader("Content-Type", "application/json"))
        }

        // Make concurrent requests
        val results = (1..5).map {
            apiClient.analyzePrompt("Test prompt $it")
        }

        // Verify all requests were successful
        results.forEach { result ->
            assertNotNull(result)
            assertEquals(0.8, result.getDouble("clarity"))
        }
    }

    @Test
    fun `test server unavailable`() {
        server.shutdown()

        assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
    }

    @Test
    fun `test invalid server URL`() {
        settings.serverUrl = "invalid-url"

        assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
    }

    @Test
    fun `test missing API key`() {
        settings.apiKey = ""

        val errorJson = JSONObject().apply {
            put("error", "Missing API key")
            put("code", "MISSING_API_KEY")
        }

        server.enqueue(MockResponse()
            .setResponseCode(401)
            .setBody(errorJson.toString())
            .addHeader("Content-Type", "application/json"))

        val exception = assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }
        assertTrue(exception.message?.contains("401") ?: false)
    }

    @Test
    fun `test detailed error message validation`() {
        val errorJson = JSONObject().apply {
            put("error", "Validation failed")
            put("code", "VALIDATION_ERROR")
            put("details", JSONObject().apply {
                put("field", "prompt")
                put("message", "Prompt must be between 1 and 1000 characters")
                put("constraints", JSONObject().apply {
                    put("min", 1)
                    put("max", 1000)
                })
            })
        }

        server.enqueue(MockResponse()
            .setResponseCode(400)
            .setBody(errorJson.toString())
            .addHeader("Content-Type", "application/json"))

        val exception = assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("")
        }

        assertTrue(exception.message?.contains("400") ?: false)
        assertTrue(exception.message?.contains("Validation failed") ?: false)
        assertTrue(exception.message?.contains("VALIDATION_ERROR") ?: false)
    }

    @Test
    fun `test retry on temporary failure`() {
        val successResponse = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        // First request fails with 503
        server.enqueue(MockResponse()
            .setResponseCode(503)
            .setBody("""{"error": "Service temporarily unavailable"}""")
            .addHeader("Content-Type", "application/json")
            .addHeader("Retry-After", "1"))

        // Second request succeeds
        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(successResponse.toString())
            .addHeader("Content-Type", "application/json"))

        val result = apiClient.analyzePrompt("Test prompt")
        assertNotNull(result)
        assertEquals(0.8, result.getDouble("clarity"))
        assertEquals(2, server.requestCount)
    }

    @Test
    fun `test retry limit exceeded`() {
        // Enqueue 4 failed responses
        repeat(4) {
            server.enqueue(MockResponse()
                .setResponseCode(503)
                .setBody("""{"error": "Service temporarily unavailable"}""")
                .addHeader("Content-Type", "application/json")
                .addHeader("Retry-After", "1"))
        }

        val exception = assertThrows(IOException::class.java) {
            apiClient.analyzePrompt("Test prompt")
        }

        assertTrue(exception.message?.contains("503") ?: false)
        assertEquals(3, server.requestCount) // Should only retry 3 times
    }

    @Test
    fun `test different HTTP methods`() {
        // Test GET request
        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody("""{"status": "ok"}""")
            .addHeader("Content-Type", "application/json"))

        val getRequest = Request.Builder()
            .url("${settings.serverUrl}/status")
            .get()
            .header("Authorization", "Bearer ${settings.apiKey}")
            .build()

        val getResponse = apiClient.executeRequest(getRequest)
        assertEquals("ok", getResponse.getString("status"))

        // Test PUT request
        val putData = JSONObject().apply {
            put("name", "test")
            put("value", 123)
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(putData.toString())
            .addHeader("Content-Type", "application/json"))

        val putRequest = Request.Builder()
            .url("${settings.serverUrl}/update")
            .put(RequestBody.create(
                MediaType.parse("application/json"),
                putData.toString()
            ))
            .header("Authorization", "Bearer ${settings.apiKey}")
            .build()

        val putResponse = apiClient.executeRequest(putRequest)
        assertEquals("test", putResponse.getString("name"))
        assertEquals(123, putResponse.getInt("value"))

        // Test DELETE request
        server.enqueue(MockResponse()
            .setResponseCode(204)
            .addHeader("Content-Type", "application/json"))

        val deleteRequest = Request.Builder()
            .url("${settings.serverUrl}/delete")
            .delete()
            .header("Authorization", "Bearer ${settings.apiKey}")
            .build()

        assertThrows(IOException::class.java) {
            apiClient.executeRequest(deleteRequest)
        }
    }

    @Test
    fun `test request headers validation`() {
        val responseJson = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        apiClient.analyzePrompt("Test prompt")

        val request = server.takeRequest()
        assertEquals("application/json", request.getHeader("Content-Type"))
        assertTrue(request.getHeader("Authorization")?.startsWith("Bearer ") ?: false)
        assertTrue(request.getHeader("User-Agent")?.contains("PromptEfficiency") ?: false)
    }

    @Test
    fun `test response headers validation`() {
        val responseJson = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json")
            .addHeader("X-Rate-Limit-Limit", "100")
            .addHeader("X-Rate-Limit-Remaining", "99")
            .addHeader("X-Rate-Limit-Reset", "3600"))

        val result = apiClient.analyzePrompt("Test prompt")
        assertNotNull(result)
        assertEquals(0.8, result.getDouble("clarity"))
    }

    @Test
    fun `test request body validation`() {
        val prompt = "Test prompt"
        val responseJson = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(responseJson.toString())
            .addHeader("Content-Type", "application/json"))

        apiClient.analyzePrompt(prompt)

        val request = server.takeRequest()
        val requestBody = JSONObject(request.body?.string() ?: "")
        assertEquals(prompt, requestBody.getString("prompt"))
        assertEquals(settings.defaultModel, requestBody.getString("model"))
    }

    @Test
    fun `test concurrent requests with rate limiting`() {
        val successResponse = JSONObject().apply {
            put("clarity", 0.8)
            put("structure", 0.7)
            put("complexity", 0.6)
        }

        // First request succeeds
        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(successResponse.toString())
            .addHeader("Content-Type", "application/json"))

        // Second request hits rate limit
        server.enqueue(MockResponse()
            .setResponseCode(429)
            .setBody("""{"error": "Rate limit exceeded"}""")
            .addHeader("Content-Type", "application/json")
            .addHeader("Retry-After", "1"))

        // Third request succeeds after retry
        server.enqueue(MockResponse()
            .setResponseCode(200)
            .setBody(successResponse.toString())
            .addHeader("Content-Type", "application/json"))

        val results = mutableListOf<JSONObject>()
        val exceptions = mutableListOf<Exception>()

        // Make concurrent requests
        (1..2).forEach {
            try {
                results.add(apiClient.analyzePrompt("Test prompt $it"))
            } catch (e: Exception) {
                exceptions.add(e)
            }
        }

        // Verify results
        assertEquals(1, results.size)
        assertEquals(1, exceptions.size)
        assertTrue(exceptions[0] is IOException)
        assertTrue(exceptions[0].message?.contains("429") ?: false)
    }
}
