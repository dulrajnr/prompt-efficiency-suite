package com.prompt.efficiency.analysis

import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import com.prompt.efficiency.api.PromptEfficiencyApiClient
import com.prompt.efficiency.patterns.PromptPatternLibrary
import com.prompt.efficiency.settings.PromptEfficiencySettings
import java.util.regex.Pattern

@Service
class PromptAnalyzer(private val project: Project) {
    private val apiClient = PromptEfficiencyApiClient.getInstance()
    private val settings = PromptEfficiencySettings.getInstance()
    private val patternLibrary = PromptPatternLibrary(project)

    data class AdvancedAnalysisResult(
        val basicMetrics: BasicMetrics,
        val qualityMetrics: QualityMetrics,
        val contextMetrics: ContextMetrics,
        val bestPractices: List<BestPractice>,
        val patterns: List<PatternMatch>
    )

    data class BasicMetrics(
        val tokenCount: Int,
        val estimatedCost: Double,
        val complexity: String,
        val readability: String
    )

    data class QualityMetrics(
        val clarity: Double, // 0-1 score
        val specificity: Double,
        val consistency: Double,
        val completeness: Double,
        val suggestions: List<String>
    )

    data class ContextMetrics(
        val domainRelevance: Double,
        val taskAlignment: Double,
        val modelCompatibility: Double,
        val contextAwareness: Double
    )

    data class BestPractice(
        val name: String,
        val description: String,
        val severity: Severity,
        val suggestion: String
    )

    data class PatternMatch(
        val pattern: String,
        val confidence: Double,
        val improvement: String
    )

    enum class Severity {
        INFO, WARNING, ERROR
    }

    private val clarityIndicators = listOf(
        "clearly", "specifically", "exactly", "precisely",
        "in detail", "as follows", "to be specific"
    )

    private val specificityIndicators = listOf(
        "for example", "such as", "like", "including",
        "specifically", "in particular", "notably"
    )

    private val consistencyIndicators = listOf(
        "first", "second", "then", "finally",
        "moreover", "furthermore", "additionally"
    )

    private val completenessIndicators = listOf(
        "all", "complete", "entire", "full",
        "comprehensive", "thorough", "exhaustive"
    )

    private val bestPractices = mapOf(
        "structure" to listOf(
            BestPractice(
                name = "Clear Task Definition",
                description = "Start with a clear task definition",
                severity = Severity.ERROR,
                suggestion = "Begin with 'Task:' followed by a clear description"
            ),
            BestPractice(
                name = "Context Setting",
                description = "Provide necessary context",
                severity = Severity.WARNING,
                suggestion = "Add context before the main task"
            ),
            BestPractice(
                name = "Output Format",
                description = "Specify expected output format",
                severity = Severity.INFO,
                suggestion = "Include 'Expected Output:' section"
            )
        ),
        "language" to listOf(
            BestPractice(
                name = "Clear Instructions",
                description = "Use clear and direct language",
                severity = Severity.WARNING,
                suggestion = "Avoid ambiguous terms and be specific"
            ),
            BestPractice(
                name = "Consistent Tone",
                description = "Maintain consistent tone",
                severity = Severity.INFO,
                suggestion = "Keep the same level of formality throughout"
            )
        ),
        "model" to mapOf(
            "gpt-4" to listOf(
                BestPractice(
                    name = "Complex Reasoning",
                    description = "Leverage GPT-4's reasoning capabilities",
                    severity = Severity.INFO,
                    suggestion = "Include step-by-step reasoning when needed"
                )
            ),
            "gpt-3.5-turbo" to listOf(
                BestPractice(
                    name = "Conciseness",
                    description = "Keep prompts concise",
                    severity = Severity.WARNING,
                    suggestion = "Focus on essential information"
                )
            )
        )
    )

    fun analyzePrompt(prompt: String, context: PromptContext): AdvancedAnalysisResult {
        // Get basic analysis from API
        val basicAnalysis = apiClient.analyzePrompt(prompt)

        // Analyze quality metrics
        val qualityMetrics = analyzeQualityMetrics(prompt)

        // Analyze context metrics
        val contextMetrics = analyzeContextMetrics(prompt, context)

        // Check best practices
        val bestPractices = checkBestPractices(prompt, context)

        // Match patterns
        val patterns = matchPatterns(prompt)

        return AdvancedAnalysisResult(
            basicMetrics = BasicMetrics(
                tokenCount = basicAnalysis.tokenCount,
                estimatedCost = basicAnalysis.estimatedCost,
                complexity = basicAnalysis.complexity,
                readability = basicAnalysis.readability
            ),
            qualityMetrics = qualityMetrics,
            contextMetrics = contextMetrics,
            bestPractices = bestPractices,
            patterns = patterns
        )
    }

    private fun analyzeQualityMetrics(prompt: String): QualityMetrics {
        val words = prompt.split("\\s+".toRegex())
        val sentences = prompt.split("[.!?]+".toRegex())

        val clarity = calculateClarityScore(prompt, sentences)
        val specificity = calculateSpecificityScore(prompt, words)
        val consistency = calculateConsistencyScore(sentences)
        val completeness = calculateCompletenessScore(prompt, words)

        val suggestions = generateQualitySuggestions(clarity, specificity, consistency, completeness)

        return QualityMetrics(
            clarity = clarity,
            specificity = specificity,
            consistency = consistency,
            completeness = completeness,
            suggestions = suggestions
        )
    }

    private fun calculateClarityScore(prompt: String, sentences: List<String>): Double {
        val clarityCount = clarityIndicators.count { prompt.contains(it, ignoreCase = true) }
        val sentenceCount = sentences.size
        val avgSentenceLength = sentences.map { it.length }.average()

        return when {
            sentenceCount == 0 -> 0.0
            avgSentenceLength > 50 -> 0.3 // Long sentences reduce clarity
            clarityCount > 0 -> 0.7 + (clarityCount * 0.1).coerceAtMost(0.3)
            else -> 0.5
        }
    }

    private fun calculateSpecificityScore(prompt: String, words: List<String>): Double {
        val specificityCount = specificityIndicators.count { prompt.contains(it, ignoreCase = true) }
        val uniqueWords = words.distinct().size
        val totalWords = words.size

        return when {
            totalWords == 0 -> 0.0
            specificityCount > 0 -> 0.6 + (specificityCount * 0.1).coerceAtMost(0.4)
            uniqueWords.toDouble() / totalWords > 0.7 -> 0.5 // High vocabulary diversity
            else -> 0.3
        }
    }

    private fun calculateConsistencyScore(sentences: List<String>): Double {
        val consistencyCount = consistencyIndicators.count {
            sentences.any { sentence -> sentence.contains(it, ignoreCase = true) }
        }

        return when {
            sentences.size <= 1 -> 1.0 // Single sentence is always consistent
            consistencyCount > 0 -> 0.7 + (consistencyCount * 0.1).coerceAtMost(0.3)
            else -> 0.5
        }
    }

    private fun calculateCompletenessScore(prompt: String, words: List<String>): Double {
        val completenessCount = completenessIndicators.count { prompt.contains(it, ignoreCase = true) }
        val hasTask = prompt.contains("task", ignoreCase = true)
        val hasOutput = prompt.contains("output", ignoreCase = true)

        return when {
            !hasTask -> 0.3
            !hasOutput -> 0.5
            completenessCount > 0 -> 0.7 + (completenessCount * 0.1).coerceAtMost(0.3)
            else -> 0.6
        }
    }

    private fun generateQualitySuggestions(
        clarity: Double,
        specificity: Double,
        consistency: Double,
        completeness: Double
    ): List<String> {
        val suggestions = mutableListOf<String>()

        if (clarity < 0.7) {
            suggestions.add("Improve clarity by using more specific terms and shorter sentences")
        }
        if (specificity < 0.7) {
            suggestions.add("Add more specific examples or details")
        }
        if (consistency < 0.7) {
            suggestions.add("Maintain consistent structure and tone throughout")
        }
        if (completeness < 0.7) {
            suggestions.add("Ensure all necessary components (task, context, output) are included")
        }

        return suggestions
    }

    private fun analyzeContextMetrics(prompt: String, context: PromptContext): ContextMetrics {
        val domainRelevance = calculateDomainRelevance(prompt, context)
        val taskAlignment = calculateTaskAlignment(prompt, context)
        val modelCompatibility = calculateModelCompatibility(prompt, context)
        val contextAwareness = calculateContextAwareness(prompt, context)

        return ContextMetrics(
            domainRelevance = domainRelevance,
            taskAlignment = taskAlignment,
            modelCompatibility = modelCompatibility,
            contextAwareness = contextAwareness
        )
    }

    private fun calculateDomainRelevance(prompt: String, context: PromptContext): Double {
        val domainTerms = context.availableContext["domain_terms"]?.split(",") ?: emptyList()
        val domainTermCount = domainTerms.count { prompt.contains(it, ignoreCase = true) }

        return when {
            domainTerms.isEmpty() -> 0.5
            domainTermCount > 0 -> 0.5 + (domainTermCount * 0.1).coerceAtMost(0.5)
            else -> 0.3
        }
    }

    private fun calculateTaskAlignment(prompt: String, context: PromptContext): Double {
        val taskTerms = context.currentTask.split("\\s+".toRegex())
        val taskTermCount = taskTerms.count { prompt.contains(it, ignoreCase = true) }

        return when {
            taskTerms.isEmpty() -> 0.5
            taskTermCount > 0 -> 0.5 + (taskTermCount * 0.1).coerceAtMost(0.5)
            else -> 0.3
        }
    }

    private fun calculateModelCompatibility(prompt: String, context: PromptContext): Double {
        val model = context.selectedModel
        val modelPatterns = patternLibrary.findPatterns(prompt, "general", model)

        return when {
            modelPatterns.isNotEmpty() -> 0.8
            prompt.length > 1000 && model == "gpt-3.5-turbo" -> 0.4
            else -> 0.6
        }
    }

    private fun calculateContextAwareness(prompt: String, context: PromptContext): Double {
        val contextTerms = context.availableContext.values.flatMap { it.split("\\s+".toRegex()) }
        val contextTermCount = contextTerms.count { prompt.contains(it, ignoreCase = true) }

        return when {
            contextTerms.isEmpty() -> 0.5
            contextTermCount > 0 -> 0.5 + (contextTermCount * 0.1).coerceAtMost(0.5)
            else -> 0.3
        }
    }

    private fun checkBestPractices(prompt: String, context: PromptContext): List<BestPractice> {
        val violations = mutableListOf<BestPractice>()

        // Check structure best practices
        bestPractices["structure"]?.forEach { practice ->
            if (!matchesBestPractice(prompt, practice)) {
                violations.add(practice)
            }
        }

        // Check language best practices
        bestPractices["language"]?.forEach { practice ->
            if (!matchesBestPractice(prompt, practice)) {
                violations.add(practice)
            }
        }

        // Check model-specific best practices
        bestPractices["model"]?.get(context.selectedModel)?.forEach { practice ->
            if (!matchesBestPractice(prompt, practice)) {
                violations.add(practice)
            }
        }

        return violations
    }

    private fun matchesBestPractice(prompt: String, practice: BestPractice): Boolean {
        return when (practice.name) {
            "Clear Task Definition" -> prompt.contains("task:", ignoreCase = true)
            "Context Setting" -> prompt.contains("context:", ignoreCase = true)
            "Output Format" -> prompt.contains("expected output:", ignoreCase = true)
            "Clear Instructions" -> !prompt.contains("maybe", ignoreCase = true) &&
                                  !prompt.contains("perhaps", ignoreCase = true)
            "Consistent Tone" -> {
                val formalTerms = listOf("please", "kindly", "would you")
                val informalTerms = listOf("hey", "thanks", "cool")
                val hasFormal = formalTerms.any { prompt.contains(it, ignoreCase = true) }
                val hasInformal = informalTerms.any { prompt.contains(it, ignoreCase = true) }
                !(hasFormal && hasInformal)
            }
            else -> true
        }
    }

    private fun matchPatterns(prompt: String): List<PatternMatch> {
        val patterns = patternLibrary.findPatterns(prompt, "general", "gpt-4")
        return patterns.map { pattern ->
            val confidence = calculatePatternConfidence(prompt, pattern)
            PatternMatch(
                pattern = pattern.name,
                confidence = confidence,
                improvement = generatePatternImprovement(prompt, pattern)
            )
        }.filter { it.confidence > 0.5 }
    }

    private fun calculatePatternConfidence(prompt: String, pattern: PromptPatternLibrary.PromptPattern): Double {
        val templateWords = pattern.template.split("\\s+".toRegex())
        val promptWords = prompt.split("\\s+".toRegex())

        val matchingWords = templateWords.count { templateWord ->
            promptWords.any { promptWord ->
                promptWord.contains(templateWord, ignoreCase = true)
            }
        }

        return (matchingWords.toDouble() / templateWords.size).coerceIn(0.0, 1.0)
    }

    private fun generatePatternImprovement(prompt: String, pattern: PromptPatternLibrary.PromptPattern): String {
        return "Consider using the ${pattern.name} pattern: ${pattern.description}"
    }
}

data class PromptContext(
    val projectType: String,
    val currentTask: String,
    val selectedModel: String,
    val availableContext: Map<String, String>
)
