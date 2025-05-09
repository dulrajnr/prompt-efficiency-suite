package com.prompt.efficiency.dev

import com.intellij.codeInsight.completion.*
import com.intellij.codeInsight.lookup.LookupElementBuilder
import com.intellij.patterns.PlatformPatterns
import com.intellij.util.ProcessingContext
import com.prompt.efficiency.patterns.PromptPatternLibrary
import com.prompt.efficiency.settings.PromptEfficiencySettings
import com.prompt.efficiency.analysis.PromptAnalyzer
import com.prompt.efficiency.analysis.PromptAnalysisResult
import com.prompt.efficiency.analysis.PromptQualityMetrics
import com.prompt.efficiency.analysis.PromptContextMetrics
import com.prompt.efficiency.analysis.PromptBestPractices
import com.prompt.efficiency.analysis.PromptPatternMatch

class PromptCompletionContributor : CompletionContributor() {
    init {
        extend(
            CompletionType.BASIC,
            PlatformPatterns.psiElement(),
            PromptCompletionProvider()
        )
    }
}

class PromptCompletionProvider : CompletionProvider<CompletionParameters>() {
    override fun addCompletions(
        parameters: CompletionParameters,
        context: ProcessingContext,
        result: CompletionResultSet
    ) {
        val project = parameters.editor.project ?: return
        val patternLibrary = PromptPatternLibrary.getInstance(project)
        val settings = PromptEfficiencySettings.getInstance(project)
        val analyzer = PromptAnalyzer.getInstance(project)

        // Get current text
        val editor = parameters.editor
        val document = editor.document
        val caretOffset = editor.caretOffset
        val text = document.text

        // Analyze current prompt
        val analysis = analyzer.analyzePrompt(text)

        // Add pattern suggestions
        patternLibrary.findPatterns(text).forEach { pattern ->
            val element = LookupElementBuilder.create(pattern.template)
                .withPresentableText(pattern.name)
                .withTypeText(pattern.category)
                .withLookupString(pattern.description)
                .withInsertHandler { context, _ ->
                    // Replace current text with pattern template
                    val start = context.startOffset
                    val end = context.tailOffset
                    context.document.replaceString(start, end, pattern.template)
                }
            result.addElement(element)
        }

        // Add best practice suggestions
        analysis.bestPractices.violations.forEach { violation ->
            val suggestion = when (violation) {
                PromptBestPractices.Violation.AMBIGUOUS_INSTRUCTIONS -> "Add specific examples and constraints"
                PromptBestPractices.Violation.INSUFFICIENT_CONTEXT -> "Provide more context about the task"
                PromptBestPractices.Violation.INCONSISTENT_FORMAT -> "Use consistent formatting and structure"
                PromptBestPractices.Violation.OVERLY_COMPLEX -> "Simplify the prompt structure"
                PromptBestPractices.Violation.INSUFFICIENT_CONSTRAINTS -> "Add clear constraints and requirements"
                PromptBestPractices.Violation.POOR_ERROR_HANDLING -> "Add error handling instructions"
                PromptBestPractices.Violation.INSUFFICIENT_EXAMPLES -> "Add more examples"
                PromptBestPractices.Violation.INCONSISTENT_TERMINOLOGY -> "Use consistent terminology"
                PromptBestPractices.Violation.INSUFFICIENT_VALIDATION -> "Add validation requirements"
                PromptBestPractices.Violation.POOR_STRUCTURE -> "Improve prompt structure"
            }
            val element = LookupElementBuilder.create(suggestion)
                .withPresentableText("Fix: $violation")
                .withTypeText("Best Practice")
                .withLookupString(violation.toString())
            result.addElement(element)
        }

        // Add model-specific suggestions
        settings.getModelSettings().forEach { modelSettings ->
            val element = LookupElementBuilder.create("Use ${modelSettings.model}")
                .withPresentableText("Switch to ${modelSettings.model}")
                .withTypeText("Model")
                .withLookupString(modelSettings.model)
            result.addElement(element)
        }

        // Add context-aware suggestions
        if (analysis.contextMetrics.domainRelevance < 0.7) {
            val element = LookupElementBuilder.create("Add domain-specific context")
                .withPresentableText("Improve domain relevance")
                .withTypeText("Context")
                .withLookupString("domain context")
            result.addElement(element)
        }

        if (analysis.contextMetrics.taskAlignment < 0.7) {
            val element = LookupElementBuilder.create("Clarify task requirements")
                .withPresentableText("Improve task alignment")
                .withTypeText("Context")
                .withLookupString("task requirements")
            result.addElement(element)
        }
    }
} 