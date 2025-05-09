package com.prompt.efficiency.api

import com.prompt.efficiency.settings.PromptEfficiencySettings
import okhttp3.*
import org.json.JSONObject
import java.io.IOException
import java.util.concurrent.TimeUnit

class ApiClient(private val settings: PromptEfficiencySettings) {
    private val client: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()

    fun analyzePrompt(prompt: String): JSONObject {
        val request = Request.Builder()
            .url("${settings.serverUrl}/analyze")
            .post(RequestBody.create(
                MediaType.parse("application/json"),
                JSONObject().apply {
                    put("prompt", prompt)
                    put("model", settings.defaultModel)
                }.toString()
            ))
            .header("Authorization", "Bearer ${settings.apiKey}")
            .build()

        return executeRequest(request)
    }

    fun optimizePrompt(prompt: String): JSONObject {
        val request = Request.Builder()
            .url("${settings.serverUrl}/optimize")
            .post(RequestBody.create(
                MediaType.parse("application/json"),
                JSONObject().apply {
                    put("prompt", prompt)
                    put("model", settings.defaultModel)
                }.toString()
            ))
            .header("Authorization", "Bearer ${settings.apiKey}")
            .build()

        return executeRequest(request)
    }

    fun estimateCost(prompt: String): JSONObject {
        val request = Request.Builder()
            .url("${settings.serverUrl}/estimate")
            .post(RequestBody.create(
                MediaType.parse("application/json"),
                JSONObject().apply {
                    put("prompt", prompt)
                    put("model", settings.defaultModel)
                    put("currency", settings.defaultCurrency)
                }.toString()
            ))
            .header("Authorization", "Bearer ${settings.apiKey}")
            .build()

        return executeRequest(request)
    }

    fun scanRepository(path: String): JSONObject {
        val request = Request.Builder()
            .url("${settings.serverUrl}/scan")
            .post(RequestBody.create(
                MediaType.parse("application/json"),
                JSONObject().apply {
                    put("path", path)
                    put("model", settings.defaultModel)
                }.toString()
            ))
            .header("Authorization", "Bearer ${settings.apiKey}")
            .build()

        return executeRequest(request)
    }

    fun translatePrompt(prompt: String, targetLanguage: String): JSONObject {
        val request = Request.Builder()
            .url("${settings.serverUrl}/translate")
            .post(RequestBody.create(
                MediaType.parse("application/json"),
                JSONObject().apply {
                    put("prompt", prompt)
                    put("target_language", targetLanguage)
                    put("model", settings.defaultModel)
                }.toString()
            ))
            .header("Authorization", "Bearer ${settings.apiKey}")
            .build()

        return executeRequest(request)
    }

    private fun executeRequest(request: Request): JSONObject {
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) {
                throw IOException("Unexpected response code: ${response.code()}")
            }

            val responseBody = response.body()?.string()
                ?: throw IOException("Empty response body")

            return JSONObject(responseBody)
        }
    }
} 