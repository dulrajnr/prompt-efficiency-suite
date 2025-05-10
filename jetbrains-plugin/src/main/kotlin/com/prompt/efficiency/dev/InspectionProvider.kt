package com.prompt.efficiency.dev

import com.intellij.codeInspection.*
import com.intellij.openapi.project.Project
import com.intellij.psi.PsiElement
import com.intellij.psi.PsiFile
import com.prompt.efficiency.analysis.PromptAnalyzer
import com.prompt.efficiency.analysis.PromptBestPractices
import com.prompt.efficiency.patterns.PromptPatternLibrary
import com.prompt.efficiency.settings.PromptEfficiencySettings

class PromptInspectionProvider : LocalInspectionTool() {
    override fun buildVisitor(
        holder: ProblemsHolder,
        isOnTheFly: Boolean
    ): PsiElementVisitor {
        return object : PsiElementVisitor() {
            override fun visitFile(file: PsiFile) {
                if (!isPromptFile(file)) return

                val project = file.project
                val analyzer = PromptAnalyzer.getInstance(project)
                val patternLibrary = PromptPatternLibrary.getInstance(project)
                val settings = PromptEfficiencySettings.getInstance(project)

                // Analyze prompt
                val analysis = analyzer.analyzePrompt(file.text)

                // Check best practices
                analysis.bestPractices.violations.forEach { violation ->
                    val quickFix = when (violation) {
                        PromptBestPractices.Violation.AMBIGUOUS_INSTRUCTIONS -> PromptQuickFixProvider.AddExamplesFix()
                        PromptBestPractices.Violation.INSUFFICIENT_CONTEXT -> PromptQuickFixProvider.AddContextFix()
                        PromptBestPractices.Violation.INCONSISTENT_FORMAT -> null
                        PromptBestPractices.Violation.OVERLY_COMPLEX -> null
                        PromptBestPractices.Violation.INSUFFICIENT_CONSTRAINTS -> PromptQuickFixProvider.AddConstraintsFix()
                        PromptBestPractices.Violation.POOR_ERROR_HANDLING -> PromptQuickFixProvider.AddErrorHandlingFix()
                        PromptBestPractices.Violation.INSUFFICIENT_EXAMPLES -> PromptQuickFixProvider.AddExamplesFix()
                        PromptBestPractices.Violation.INCONSISTENT_TERMINOLOGY -> null
                        PromptBestPractices.Violation.INSUFFICIENT_VALIDATION -> PromptQuickFixProvider.AddValidationFix()
                        PromptBestPractices.Violation.POOR_STRUCTURE -> null
                    }

                    if (quickFix != null) {
                        holder.registerProblem(
                            file,
                            violation.toString(),
                            ProblemHighlightType.WEAK_WARNING,
                            quickFix
                        )
                    }
                }

                // Check context metrics
                if (analysis.contextMetrics.domainRelevance < 0.7) {
                    holder.registerProblem(
                        file,
                        "Low domain relevance",
                        ProblemHighlightType.WEAK_WARNING,
                        PromptQuickFixProvider.AddContextFix()
                    )
                }

                if (analysis.contextMetrics.taskAlignment < 0.7) {
                    holder.registerProblem(
                        file,
                        "Low task alignment",
                        ProblemHighlightType.WEAK_WARNING,
                        PromptQuickFixProvider.AddTaskRequirementsFix()
                    )
                }

                // Check for pattern matches
                patternLibrary.findPatterns(file.text).forEach { pattern ->
                    holder.registerProblem(
                        file,
                        "Consider using pattern: ${pattern.name}",
                        ProblemHighlightType.INFORMATION,
                        PromptQuickFixProvider.ApplyPatternFix(pattern.id)
                    )
                }

                // Check model compatibility
                val currentModel = settings.getDefaultModel()
                val modelSettings = settings.getModelSettings().find { it.model == currentModel }
                if (modelSettings != null) {
                    val tokenCount = analysis.qualityMetrics.tokenCount
                    if (tokenCount > modelSettings.maxTokens) {
                        holder.registerProblem(
                            file,
                            "Prompt exceeds model's token limit",
                            ProblemHighlightType.WARNING
                        )
                    }
                }
            }
        }
    }

    private fun isPromptFile(file: PsiFile): Boolean {
        // Check if file is a prompt file based on extension or content
        return file.name.endsWith(".prompt") || file.name.endsWith(".txt")
    }
}
