package com.prompt.efficiency.api

import com.intellij.openapi.components.Service
import com.intellij.openapi.components.ServiceManager
import com.prompt.efficiency.settings.PromptEfficiencySettings
import okhttp3.*
import org.json.JSONObject
import java.io.IOException
import java.util.concurrent.TimeUnit

@Service
class PromptEfficiencyApiClient {
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    private val settings: PromptEfficiencySettings = PromptEfficiencySettings.getInstance()

    fun analyzePrompt(prompt: String): AnalysisResult {
        val request = createRequest("analyze", mapOf("prompt" to prompt))
        return executeRequest(request) { response ->
            val json = JSONObject(response)
            AnalysisResult(
                tokenCount = json.getInt("tokenCount"),
                estimatedCost = json.getDouble("estimatedCost"),
                suggestions = json.getJSONArray("suggestions").map { it.toString() },
                complexity = json.getString("complexity"),
                readability = json.getString("readability")
            )
        }
    }

    fun optimizePrompt(prompt: String): OptimizationResult {
        val request = createRequest("optimize", mapOf("prompt" to prompt))
        return executeRequest(request) { response ->
            val json = JSONObject(response)
            OptimizationResult(
                optimizedPrompt = json.getString("optimizedPrompt"),
                tokenReduction = json.getInt("tokenReduction"),
                costReduction = json.getDouble("costReduction"),
                improvements = json.getJSONArray("improvements").map { it.toString() }
            )
        }
    }

    fun estimateCost(prompt: String, model: String): CostEstimate {
        val request = createRequest("estimate", mapOf(
            "prompt" to prompt,
            "model" to model
        ))
        return executeRequest(request) { response ->
            val json = JSONObject(response)
            CostEstimate(
                tokenCount = json.getInt("tokenCount"),
                estimatedCost = json.getDouble("estimatedCost"),
                currency = json.getString("currency"),
                model = json.getString("model")
            )
        }
    }

    fun scanRepository(path: String): RepositoryAnalysis {
        val request = createRequest("scan", mapOf("path" to path))
        return executeRequest(request) { response ->
            val json = JSONObject(response)
            RepositoryAnalysis(
                totalPrompts = json.getInt("totalPrompts"),
                totalTokens = json.getInt("totalTokens"),
                estimatedCost = json.getDouble("estimatedCost"),
                promptsByFile = json.getJSONObject("promptsByFile").toMap(),
                suggestions = json.getJSONArray("suggestions").map { it.toString() }
            )
        }
    }

    fun translatePrompt(prompt: String, targetLanguage: String): TranslationResult {
        val request = createRequest("translate", mapOf(
            "prompt" to prompt,
            "target_language" to targetLanguage
        ))
        return executeRequest(request) { response ->
            val json = JSONObject(response)
            TranslationResult(
                translatedPrompt = json.getString("translatedPrompt"),
                sourceLanguage = json.getString("sourceLanguage"),
                targetLanguage = json.getString("targetLanguage"),
                confidence = json.getDouble("confidence")
            )
        }
    }

    private fun createRequest(endpoint: String, params: Map<String, String>): Request {
        val urlBuilder = HttpUrl.Builder()
            .scheme("https")
            .host("api.prompt.com")
            .addPathSegment("v1")
            .addPathSegment(endpoint)

        params.forEach { (key, value) ->
            urlBuilder.addQueryParameter(key, value)
        }

        return Request.Builder()
            .url(urlBuilder.build())
            .addHeader("Authorization", "Bearer ${settings.apiKey}")
            .build()
    }

    private fun <T> executeRequest(request: Request, responseHandler: (String) -> T): T {
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) {
                throw IOException("API request failed: ${response.code}")
            }

            val responseBody = response.body?.string()
                ?: throw IOException("Empty response body")

            return responseHandler(responseBody)
        }
    }

    data class AnalysisResult(
        val tokenCount: Int,
        val estimatedCost: Double,
        val suggestions: List<String>,
        val complexity: String,
        val readability: String
    )

    data class OptimizationResult(
        val optimizedPrompt: String,
        val tokenReduction: Int,
        val costReduction: Double,
        val improvements: List<String>
    )

    data class CostEstimate(
        val tokenCount: Int,
        val estimatedCost: Double,
        val currency: String,
        val model: String
    )

    data class RepositoryAnalysis(
        val totalPrompts: Int,
        val totalTokens: Int,
        val estimatedCost: Double,
        val promptsByFile: Map<String, Int>,
        val suggestions: List<String>
    )

    data class TranslationResult(
        val translatedPrompt: String,
        val sourceLanguage: String,
        val targetLanguage: String,
        val confidence: Double
    )

    companion object {
        fun getInstance(): PromptEfficiencyApiClient {
            return ServiceManager.getService(PromptEfficiencyApiClient::class.java)
        }
    }
} 