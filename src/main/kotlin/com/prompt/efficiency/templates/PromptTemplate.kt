package com.prompt.efficiency.templates

import com.google.gson.Gson
import com.google.gson.JsonObject
import java.time.LocalDateTime
import java.util.*

data class PromptTemplate(
    val id: String = UUID.randomUUID().toString(),
    val name: String,
    val description: String,
    val category: String,
    val model: String,
    val template: String,
    val variables: List<Variable> = emptyList(),
    val metadata: Map<String, String> = emptyMap(),
    val version: String = "1.0",
    val author: String,
    val createdAt: LocalDateTime = LocalDateTime.now(),
    val updatedAt: LocalDateTime = LocalDateTime.now()
) {
    data class Variable(
        val name: String,
        val description: String,
        val type: VariableType,
        val defaultValue: String? = null,
        val required: Boolean = false,
        val validationRules: List<ValidationRule> = emptyList()
    )

    enum class VariableType {
        STRING,
        NUMBER,
        BOOLEAN,
        LIST,
        OBJECT
    }

    data class ValidationRule(
        val type: ValidationType,
        val value: String,
        val message: String
    )

    enum class ValidationType {
        MIN_LENGTH,
        MAX_LENGTH,
        PATTERN,
        MIN_VALUE,
        MAX_VALUE,
        REQUIRED_VALUES,
        CUSTOM
    }

    fun toJson(): String {
        val gson = Gson()
        val json = JsonObject()

        json.addProperty("id", id)
        json.addProperty("name", name)
        json.addProperty("description", description)
        json.addProperty("category", category)
        json.addProperty("model", model)
        json.addProperty("template", template)
        json.addProperty("version", version)
        json.addProperty("author", author)
        json.addProperty("createdAt", createdAt.toString())
        json.addProperty("updatedAt", updatedAt.toString())

        // Add variables
        val variablesArray = gson.toJsonTree(variables)
        json.add("variables", variablesArray)

        // Add metadata
        val metadataObject = JsonObject()
        metadata.forEach { (key, value) ->
            metadataObject.addProperty(key, value)
        }
        json.add("metadata", metadataObject)

        return gson.toJson(json)
    }

    companion object {
        fun fromJson(json: String): PromptTemplate {
            val gson = Gson()
            val jsonObject = gson.fromJson(json, JsonObject::class.java)

            val variables = jsonObject.getAsJsonArray("variables")?.map { element ->
                gson.fromJson(element, Variable::class.java)
            } ?: emptyList()

            val metadata = jsonObject.getAsJsonObject("metadata")?.let { obj ->
                obj.entrySet().associate { it.key to it.value.asString }
            } ?: emptyMap()

            return PromptTemplate(
                id = jsonObject.get("id").asString,
                name = jsonObject.get("name").asString,
                description = jsonObject.get("description").asString,
                category = jsonObject.get("category").asString,
                model = jsonObject.get("model").asString,
                template = jsonObject.get("template").asString,
                variables = variables,
                metadata = metadata,
                version = jsonObject.get("version").asString,
                author = jsonObject.get("author").asString,
                createdAt = LocalDateTime.parse(jsonObject.get("createdAt").asString),
                updatedAt = LocalDateTime.parse(jsonObject.get("updatedAt").asString)
            )
        }
    }
}
