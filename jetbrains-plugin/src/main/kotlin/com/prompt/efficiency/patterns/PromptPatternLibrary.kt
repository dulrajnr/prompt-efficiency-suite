package com.prompt.efficiency.patterns

import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.util.xmlb.XmlSerializerUtil
import java.util.regex.Pattern

@Service
@State(
    name = "PromptPatternLibrary",
    storages = [Storage("prompt-patterns.xml")]
)
class PromptPatternLibrary(private val project: Project) : PersistentStateComponent<PromptPatternLibrary.State> {
    private var state = State()

    data class State(
        var patterns: MutableList<PromptPattern> = mutableListOf(),
        var categories: MutableSet<String> = mutableSetOf("general", "code", "documentation", "testing"),
        var modelSpecificPatterns: MutableMap<String, MutableList<String>> = mutableMapOf()
    )

    data class PromptPattern(
        val id: String,
        var name: String,
        var description: String,
        var template: String,
        var category: String,
        var model: String,
        var tags: MutableSet<String> = mutableSetOf(),
        var usageCount: Int = 0,
        var successRate: Double = 0.0,
        var lastUsed: Long = 0
    )

    override fun getState(): State = state

    override fun loadState(state: State) {
        XmlSerializerUtil.copyBean(state, this.state)
    }

    fun findPatterns(prompt: String, category: String, model: String): List<PromptPattern> {
        return state.patterns.filter { pattern ->
            pattern.category == category &&
            (pattern.model == model || pattern.model == "general") &&
            matchesPattern(prompt, pattern)
        }.sortedByDescending { it.successRate }
    }

    fun addPattern(pattern: PromptPattern) {
        state.patterns.add(pattern)
        state.categories.add(pattern.category)
        state.modelSpecificPatterns.getOrPut(pattern.model) { mutableListOf() }.add(pattern.id)
    }

    fun updatePattern(pattern: PromptPattern) {
        val index = state.patterns.indexOfFirst { it.id == pattern.id }
        if (index != -1) {
            state.patterns[index] = pattern
        }
    }

    fun deletePattern(patternId: String) {
        state.patterns.removeIf { it.id == patternId }
        state.modelSpecificPatterns.values.forEach { it.remove(patternId) }
    }

    fun getPatternsByCategory(category: String): List<PromptPattern> {
        return state.patterns.filter { it.category == category }
    }

    fun getPatternsByModel(model: String): List<PromptPattern> {
        return state.patterns.filter { it.model == model || it.model == "general" }
    }

    fun getPatternsByTags(tags: Set<String>): List<PromptPattern> {
        return state.patterns.filter { pattern ->
            tags.any { tag -> pattern.tags.contains(tag) }
        }
    }

    fun updatePatternStats(patternId: String, success: Boolean) {
        state.patterns.find { it.id == patternId }?.let { pattern ->
            pattern.usageCount++
            pattern.successRate = ((pattern.successRate * (pattern.usageCount - 1) +
                if (success) 1.0 else 0.0) / pattern.usageCount)
            pattern.lastUsed = System.currentTimeMillis()
        }
    }

    private fun matchesPattern(prompt: String, pattern: PromptPattern): Boolean {
        // Convert template to regex pattern
        val regexPattern = pattern.template
            .replace("{", "(?<")
            .replace("}", ">[^}]+)")
            .replace(" ", "\\s+")

        return try {
            val matcher = Pattern.compile(regexPattern, Pattern.CASE_INSENSITIVE).matcher(prompt)
            matcher.matches()
        } catch (e: Exception) {
            false
        }
    }

    fun extractVariables(prompt: String, pattern: PromptPattern): Map<String, String> {
        val regexPattern = pattern.template
            .replace("{", "(?<")
            .replace("}", ">[^}]+)")
            .replace(" ", "\\s+")

        return try {
            val matcher = Pattern.compile(regexPattern, Pattern.CASE_INSENSITIVE).matcher(prompt)
            if (matcher.matches()) {
                pattern.template.split("\\s+".toRegex())
                    .filter { it.startsWith("{") && it.endsWith("}") }
                    .map { it.substring(1, it.length - 1) }
                    .associateWith { matcher.group(it) }
            } else {
                emptyMap()
            }
        } catch (e: Exception) {
            emptyMap()
        }
    }

    fun suggestPatterns(prompt: String, model: String): List<PatternSuggestion> {
        return state.patterns
            .filter { it.model == model || it.model == "general" }
            .map { pattern ->
                val confidence = calculatePatternConfidence(prompt, pattern)
                PatternSuggestion(
                    pattern = pattern,
                    confidence = confidence,
                    variables = extractVariables(prompt, pattern)
                )
            }
            .filter { it.confidence > 0.5 }
            .sortedByDescending { it.confidence }
    }

    private fun calculatePatternConfidence(prompt: String, pattern: PromptPattern): Double {
        val templateWords = pattern.template.split("\\s+".toRegex())
        val promptWords = prompt.split("\\s+".toRegex())

        val matchingWords = templateWords.count { templateWord ->
            promptWords.any { promptWord ->
                promptWord.contains(templateWord, ignoreCase = true)
            }
        }

        return (matchingWords.toDouble() / templateWords.size).coerceIn(0.0, 1.0)
    }

    data class PatternSuggestion(
        val pattern: PromptPattern,
        val confidence: Double,
        val variables: Map<String, String>
    )

    companion object {
        fun getInstance(project: Project): PromptPatternLibrary {
            return project.getService(PromptPatternLibrary::class.java)
        }
    }
}
