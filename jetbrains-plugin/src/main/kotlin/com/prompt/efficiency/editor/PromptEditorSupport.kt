package com.prompt.efficiency.editor

import com.intellij.codeInsight.completion.*
import com.intellij.codeInsight.lookup.LookupElementBuilder
import com.intellij.openapi.components.Service
import com.intellij.openapi.editor.Editor
import com.intellij.openapi.project.Project
import com.intellij.psi.PsiFile
import com.prompt.efficiency.analysis.PromptAnalyzer
import com.prompt.efficiency.patterns.PromptPatternLibrary
import com.prompt.efficiency.analytics.CostAnalytics

@Service
class PromptEditorSupport(private val project: Project) {
    private val analyzer = PromptAnalyzer(project)
    private val patternLibrary = PromptPatternLibrary(project)
    private val costAnalytics = CostAnalytics(project)

    fun getCompletionContributor(): CompletionContributor {
        return object : CompletionContributor() {
            init {
                extend(
                    CompletionType.BASIC,
                    PromptPatternCompletionProvider.pattern,
                    PromptPatternCompletionProvider()
                )
                extend(
                    CompletionType.BASIC,
                    BestPracticesCompletionProvider.pattern,
                    BestPracticesCompletionProvider()
                )
                extend(
                    CompletionType.BASIC,
                    ModelCompletionProvider.pattern,
                    ModelCompletionProvider()
                )
            }
        }
    }

    fun getAnnotator(): PromptAnnotator {
        return PromptAnnotator()
    }

    inner class PromptPatternCompletionProvider : CompletionProvider<CompletionParameters>() {
        companion object {
            val pattern = PlatformPatterns.psiElement()
                .withLanguage(PromptLanguage.INSTANCE)
        }

        override fun addCompletions(
            parameters: CompletionParameters,
            context: ProcessingContext,
            result: CompletionResultSet
        ) {
            val patterns = patternLibrary.findPatterns(
                parameters.editor.document.text,
                "general",
                "gpt-4"
            )

            patterns.forEach { pattern ->
                result.addElement(
                    LookupElementBuilder.create(pattern.name)
                        .withPresentableText(pattern.name)
                        .withTypeText(pattern.description)
                        .withInsertHandler { context, _ ->
                            insertPattern(context.editor, pattern)
                        }
                )
            }
        }

        private fun insertPattern(editor: Editor, pattern: PromptPatternLibrary.PromptPattern) {
            // TODO: Implement pattern insertion with proper formatting
        }
    }

    inner class BestPracticesCompletionProvider : CompletionProvider<CompletionParameters>() {
        companion object {
            val pattern = PlatformPatterns.psiElement()
                .withLanguage(PromptLanguage.INSTANCE)
        }

        override fun addCompletions(
            parameters: CompletionParameters,
            context: ProcessingContext,
            result: CompletionResultSet
        ) {
            val bestPractices = patternLibrary.getBestPractices("general", "gpt-4")

            bestPractices.forEach { practice ->
                result.addElement(
                    LookupElementBuilder.create(practice)
                        .withPresentableText(practice)
                        .withTypeText("Best Practice")
                )
            }
        }
    }

    inner class ModelCompletionProvider : CompletionProvider<CompletionParameters>() {
        companion object {
            val pattern = PlatformPatterns.psiElement()
                .withLanguage(PromptLanguage.INSTANCE)
        }

        override fun addCompletions(
            parameters: CompletionParameters,
            context: ProcessingContext,
            result: CompletionResultSet
        ) {
            val models = listOf("gpt-4", "gpt-3.5-turbo", "claude")

            models.forEach { model ->
                result.addElement(
                    LookupElementBuilder.create(model)
                        .withPresentableText(model)
                        .withTypeText("Model")
                )
            }
        }
    }

    inner class PromptAnnotator : com.intellij.lang.annotation.Annotator {
        override fun annotate(element: com.intellij.psi.PsiElement, holder: com.intellij.lang.annotation.AnnotationHolder) {
            if (element.language != PromptLanguage.INSTANCE) return

            val text = element.text
            val context = PromptContext(
                projectType = "general",
                currentTask = "editing",
                selectedModel = "gpt-4",
                availableContext = emptyMap()
            )

            val analysis = analyzer.analyzePrompt(text, context)

            // Annotate quality issues
            if (analysis.qualityMetrics.clarity < 0.7) {
                holder.createWarningAnnotation(
                    element.textRange,
                    "Prompt clarity could be improved"
                )
            }

            // Annotate best practice violations
            analysis.bestPractices.forEach { practice ->
                when (practice.severity) {
                    Severity.ERROR -> holder.createErrorAnnotation(
                        element.textRange,
                        practice.suggestion
                    )
                    Severity.WARNING -> holder.createWarningAnnotation(
                        element.textRange,
                        practice.suggestion
                    )
                    Severity.INFO -> holder.createInfoAnnotation(
                        element.textRange,
                        practice.suggestion
                    )
                }
            }

            // Annotate cost concerns
            if (analysis.basicMetrics.estimatedCost > 0.1) {
                holder.createWarningAnnotation(
                    element.textRange,
                    "High cost prompt - consider optimization"
                )
            }
        }
    }
}

object PromptLanguage : com.intellij.lang.Language("Prompt") {
    companion object {
        val INSTANCE = PromptLanguage()
    }
}
