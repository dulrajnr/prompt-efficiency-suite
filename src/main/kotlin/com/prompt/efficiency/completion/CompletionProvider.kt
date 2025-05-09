package com.prompt.efficiency.completion

import com.intellij.codeInsight.completion.*
import com.intellij.codeInsight.lookup.LookupElementBuilder
import com.intellij.patterns.PlatformPatterns
import com.intellij.util.ProcessingContext
import com.prompt.efficiency.collab.TeamPatternManager
import com.prompt.efficiency.settings.PromptEfficiencySettings
import com.prompt.efficiency.templates.PromptTemplate

class CompletionProvider : CompletionContributor() {
    init {
        extend(
            CompletionType.BASIC,
            PlatformPatterns.psiElement(),
            object : CompletionProvider<CompletionParameters>() {
                override fun addCompletions(
                    parameters: CompletionParameters,
                    context: ProcessingContext,
                    result: CompletionResultSet
                ) {
                    val project = parameters.editor.project ?: return
                    val settings = PromptEfficiencySettings.getInstance(project)
                    val patternManager = TeamPatternManager.getInstance(project)
                    
                    // Get patterns based on current context
                    val patterns = patternManager.getPatterns()
                        .filter { it.model == settings.selectedModel }
                    
                    // Add pattern completions
                    patterns.forEach { pattern ->
                        val element = LookupElementBuilder.create(pattern.name)
                            .withPresentableText(pattern.name)
                            .withTypeText(pattern.category)
                            .withInsertHandler { context, _ ->
                                val editor = context.editor
                                val document = editor.document
                                val caretOffset = editor.caretModel.offset
                                
                                // Insert pattern template
                                document.insertString(caretOffset, pattern.template)
                                
                                // Move caret to end of inserted text
                                editor.caretModel.moveToOffset(caretOffset + pattern.template.length)
                            }
                        
                        result.addElement(element)
                    }

                    // Add best practices completions
                    addBestPracticesCompletions(result, project)
                    
                    // Add model-specific completions
                    addModelSpecificCompletions(result, settings.selectedModel)
                }
            }
        )
    }

    private fun addBestPracticesCompletions(result: CompletionResultSet, project: Project) {
        val bestPractices = listOf(
            "Add examples to improve clarity",
            "Include error handling instructions",
            "Specify output format",
            "Add context about the task",
            "Include constraints and limitations",
            "Specify success criteria",
            "Add fallback options"
        )

        bestPractices.forEach { practice ->
            val element = LookupElementBuilder.create(practice)
                .withPresentableText(practice)
                .withTypeText("Best Practice")
                .withInsertHandler { context, _ ->
                    val editor = context.editor
                    val document = editor.document
                    val caretOffset = editor.caretModel.offset
                    
                    // Insert best practice template
                    val template = when (practice) {
                        "Add examples to improve clarity" -> "\n\nExample:\nInput: <example_input>\nOutput: <example_output>"
                        "Include error handling instructions" -> "\n\nError Handling:\n- If <condition>, then <action>\n- Handle <error_case> by <solution>"
                        "Specify output format" -> "\n\nOutput Format:\n- Format: <format_type>\n- Required fields: <fields>\n- Optional fields: <fields>"
                        "Add context about the task" -> "\n\nContext:\n- Purpose: <purpose>\n- Background: <background>\n- Related tasks: <tasks>"
                        "Include constraints and limitations" -> "\n\nConstraints:\n- Time limit: <limit>\n- Resource limits: <limits>\n- Technical constraints: <constraints>"
                        "Specify success criteria" -> "\n\nSuccess Criteria:\n- Must include: <criteria>\n- Must not include: <criteria>\n- Performance metrics: <metrics>"
                        "Add fallback options" -> "\n\nFallback Options:\n- Primary approach: <approach>\n- Alternative approach: <approach>\n- Emergency fallback: <fallback>"
                        else -> "\n\n$practice: <details>"
                    }
                    
                    document.insertString(caretOffset, template)
                    editor.caretModel.moveToOffset(caretOffset + template.length)
                }
            
            result.addElement(element)
        }
    }

    private fun addModelSpecificCompletions(result: CompletionResultSet, model: String) {
        val modelSpecificCompletions = when (model.lowercase()) {
            "gpt-4" -> listOf(
                "Use system message for context",
                "Specify temperature",
                "Set max tokens",
                "Enable function calling"
            )
            "gpt-3.5-turbo" -> listOf(
                "Optimize for token efficiency",
                "Use concise instructions",
                "Enable streaming",
                "Set presence penalty"
            )
            else -> emptyList()
        }

        modelSpecificCompletions.forEach { completion ->
            val element = LookupElementBuilder.create(completion)
                .withPresentableText(completion)
                .withTypeText("Model-Specific")
                .withInsertHandler { context, _ ->
                    val editor = context.editor
                    val document = editor.document
                    val caretOffset = editor.caretModel.offset
                    
                    // Insert model-specific template
                    val template = when (completion) {
                        "Use system message for context" -> "\n\nSystem: <system_message>"
                        "Specify temperature" -> "\n\nTemperature: <value>"
                        "Set max tokens" -> "\n\nMax Tokens: <value>"
                        "Enable function calling" -> "\n\nFunctions: [<function_specs>]"
                        "Optimize for token efficiency" -> "\n\nToken Optimization:\n- Use abbreviations where possible\n- Minimize redundant text\n- Focus on essential information"
                        "Use concise instructions" -> "\n\nInstructions:\n- Be concise\n- Use bullet points\n- Avoid unnecessary context"
                        "Enable streaming" -> "\n\nStreaming: true"
                        "Set presence penalty" -> "\n\nPresence Penalty: <value>"
                        else -> "\n\n$completion: <details>"
                    }
                    
                    document.insertString(caretOffset, template)
                    editor.caretModel.moveToOffset(caretOffset + template.length)
                }
            
            result.addElement(element)
        }
    }
} 