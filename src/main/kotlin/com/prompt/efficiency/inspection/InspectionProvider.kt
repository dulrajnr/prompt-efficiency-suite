package com.prompt.efficiency.inspection

import com.intellij.codeInspection.*
import com.intellij.openapi.project.Project
import com.intellij.psi.*
import com.prompt.efficiency.settings.PromptEfficiencySettings

class PromptEfficiencyInspection : LocalInspectionTool() {
    override fun buildVisitor(holder: ProblemsHolder, isOnTheFly: Boolean): PsiElementVisitor {
        return object : PsiElementVisitor() {
            override fun visitFile(file: PsiFile) {
                try {
                    if (!isPromptFile(file)) return
                    
                    val text = file.text
                    val settings = PromptEfficiencySettings.getInstance(file.project)
                    
                    // Check prompt complexity
                    val complexity = calculateComplexity(text)
                    if (complexity > settings.maxComplexity) {
                        holder.registerProblem(
                            file,
                            "Prompt is too complex (score: $complexity). Consider simplifying.",
                            ProblemHighlightType.WEAK_WARNING
                        )
                    }
                    
                    // Check token count
                    val tokenCount = estimateTokenCount(text)
                    if (tokenCount > settings.maxTokens) {
                        holder.registerProblem(
                            file,
                            "Prompt exceeds token limit ($tokenCount tokens). Maximum allowed: ${settings.maxTokens}",
                            ProblemHighlightType.WARNING
                        )
                    }
                    
                    // Check clarity
                    val clarity = analyzeClarity(text)
                    if (clarity < settings.minClarity) {
                        holder.registerProblem(
                            file,
                            "Prompt clarity is low (score: $clarity). Consider adding more context or examples.",
                            ProblemHighlightType.WEAK_WARNING
                        )
                    }
                    
                    // Check cost estimate
                    val costEstimate = estimateCost(text, settings.selectedModel)
                    if (costEstimate > settings.maxCost) {
                        holder.registerProblem(
                            file,
                            "Estimated cost ($costEstimate) exceeds maximum allowed (${settings.maxCost})",
                            ProblemHighlightType.WARNING
                        )
                    }
                } catch (e: Exception) {
                    holder.registerProblem(
                        file,
                        "Error analyzing prompt: ${e.message}",
                        ProblemHighlightType.ERROR
                    )
                }
            }
        }
    }
    
    private fun isPromptFile(file: PsiFile): Boolean {
        return file.name.endsWith(".prompt") || file.name.endsWith(".txt")
    }
    
    private fun calculateComplexity(text: String): Double {
        // Simple complexity calculation based on length, special characters, and structure
        val length = text.length
        val specialChars = text.count { it in "{}[]()<>$@#" }
        val sections = text.split("\n\n").size
        return (length * 0.01 + specialChars * 0.5 + sections * 2.0)
    }
    
    private fun estimateTokenCount(text: String): Int {
        // Rough estimation: average English word is 4 characters
        return text.split(Regex("\\s+")).size + (text.length / 4)
    }
    
    private fun analyzeClarity(text: String): Double {
        // Simple clarity score based on presence of key elements
        var score = 1.0
        if (!text.contains("example", ignoreCase = true)) score -= 0.2
        if (!text.contains("context", ignoreCase = true)) score -= 0.2
        if (!text.contains("expected", ignoreCase = true)) score -= 0.2
        if (text.contains("please", ignoreCase = true)) score -= 0.1
        if (text.split("\n").size < 3) score -= 0.3
        return score.coerceIn(0.0, 1.0)
    }
    
    private fun estimateCost(text: String, model: String): Double {
        // Simple cost estimation based on token count and model
        val tokenCount = estimateTokenCount(text)
        return when (model.lowercase()) {
            "gpt-4" -> tokenCount * 0.00003
            "gpt-3.5-turbo" -> tokenCount * 0.000002
            else -> tokenCount * 0.000005
        }
    }
} 