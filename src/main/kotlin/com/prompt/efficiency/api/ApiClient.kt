package com.prompt.efficiency.api

import com.google.gson.Gson
import com.google.gson.JsonObject
import com.intellij.openapi.diagnostic.Logger
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException
import java.time.Duration
import java.util.concurrent.TimeUnit

class ApiClient(
    private val baseUrl: String,
    private val apiKey: String,
    private val timeoutSeconds: Int = 30
) {
    private val client = OkHttpClient.Builder()
        .connectTimeout(timeoutSeconds.toLong(), TimeUnit.SECONDS)
        .readTimeout(timeoutSeconds.toLong(), TimeUnit.SECONDS)
        .writeTimeout(timeoutSeconds.toLong(), TimeUnit.SECONDS)
        .build()
    
    private val gson = Gson()
    private val logger = Logger.getInstance(ApiClient::class.java)
    private val jsonMediaType = "application/json; charset=utf-8".toMediaType()

    fun analyzePrompt(prompt: String, model: String): AnalysisResult {
        val requestBody = JsonObject().apply {
            addProperty("prompt", prompt)
            addProperty("model", model)
        }

        val response = makeRequest("/analyze", requestBody)
        return gson.fromJson(response, AnalysisResult::class.java)
    }

    fun estimateCost(prompt: String, model: String): CostEstimate {
        val requestBody = JsonObject().apply {
            addProperty("prompt", prompt)
            addProperty("model", model)
        }

        val response = makeRequest("/estimate-cost", requestBody)
        return gson.fromJson(response, CostEstimate::class.java)
    }

    fun optimizePrompt(prompt: String, constraints: OptimizationConstraints): OptimizationResult {
        val requestBody = JsonObject().apply {
            addProperty("prompt", prompt)
            add("constraints", gson.toJsonTree(constraints))
        }

        val response = makeRequest("/optimize", requestBody)
        return gson.fromJson(response, OptimizationResult::class.java)
    }

    private fun makeRequest(endpoint: String, requestBody: JsonObject): String {
        val request = Request.Builder()
            .url(baseUrl + endpoint)
            .addHeader("Authorization", "Bearer $apiKey")
            .post(gson.toJson(requestBody).toRequestBody(jsonMediaType))
            .build()

        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) {
                throw ApiException("API request failed with code ${response.code}")
            }

            return response.body?.string() ?: throw ApiException("Empty response body")
        }
    }

    data class AnalysisResult(
        val complexity: Double,
        val tokenCount: Int,
        val clarity: Double,
        val suggestions: List<String>
    )

    data class CostEstimate(
        val estimatedCost: Double,
        val currency: String = "USD",
        val tokenCount: Int
    )

    data class OptimizationConstraints(
        val maxTokens: Int,
        val maxComplexity: Double,
        val minClarity: Double,
        val targetModel: String
    )

    data class OptimizationResult(
        val optimizedPrompt: String,
        val tokenCount: Int,
        val complexity: Double,
        val clarity: Double
    )

    class ApiException(message: String) : Exception(message)
} 