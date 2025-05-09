package com.prompt.efficiency.dev

import com.intellij.codeInspection.LocalQuickFix
import com.intellij.codeInspection.ProblemDescriptor
import com.intellij.openapi.project.Project
import com.intellij.openapi.command.WriteCommandAction
import com.prompt.efficiency.analysis.PromptAnalyzer
import com.prompt.efficiency.analysis.PromptBestPractices
import com.prompt.efficiency.patterns.PromptPatternLibrary
import com.prompt.efficiency.settings.PromptEfficiencySettings

class PromptQuickFixProvider {
    class AddExamplesFix : LocalQuickFix {
        override fun getName() = "Add examples to improve clarity"
        override fun getFamilyName() = "Prompt Improvements"
        override fun applyFix(project: Project, descriptor: ProblemDescriptor) {
            WriteCommandAction.runWriteCommandAction(project) {
                val document = descriptor.psiElement.containingFile.viewProvider.document
                val text = document.text
                val examples = """
                    |Here are some examples:
                    |
                    |Example 1:
                    |Input: [describe input]
                    |Output: [describe expected output]
                    |
                    |Example 2:
                    |Input: [describe input]
                    |Output: [describe expected output]
                    |
                """.trimMargin()
                document.insertString(document.textLength, "\n\n$examples")
            }
        }
    }

    class AddConstraintsFix : LocalQuickFix {
        override fun getName() = "Add constraints and requirements"
        override fun getFamilyName() = "Prompt Improvements"
        override fun applyFix(project: Project, descriptor: ProblemDescriptor) {
            WriteCommandAction.runWriteCommandAction(project) {
                val document = descriptor.psiElement.containingFile.viewProvider.document
                val text = document.text
                val constraints = """
                    |Constraints and Requirements:
                    |1. [Add specific constraint]
                    |2. [Add specific constraint]
                    |3. [Add specific constraint]
                    |
                """.trimMargin()
                document.insertString(document.textLength, "\n\n$constraints")
            }
        }
    }

    class AddErrorHandlingFix : LocalQuickFix {
        override fun getName() = "Add error handling instructions"
        override fun getFamilyName() = "Prompt Improvements"
        override fun applyFix(project: Project, descriptor: ProblemDescriptor) {
            WriteCommandAction.runWriteCommandAction(project) {
                val document = descriptor.psiElement.containingFile.viewProvider.document
                val text = document.text
                val errorHandling = """
                    |Error Handling:
                    |1. If [error condition], then [action]
                    |2. If [error condition], then [action]
                    |3. If [error condition], then [action]
                    |
                """.trimMargin()
                document.insertString(document.textLength, "\n\n$errorHandling")
            }
        }
    }

    class AddValidationFix : LocalQuickFix {
        override fun getName() = "Add validation requirements"
        override fun getFamilyName() = "Prompt Improvements"
        override fun applyFix(project: Project, descriptor: ProblemDescriptor) {
            WriteCommandAction.runWriteCommandAction(project) {
                val document = descriptor.psiElement.containingFile.viewProvider.document
                val text = document.text
                val validation = """
                    |Validation Requirements:
                    |1. Verify that [requirement]
                    |2. Ensure that [requirement]
                    |3. Validate that [requirement]
                    |
                """.trimMargin()
                document.insertString(document.textLength, "\n\n$validation")
            }
        }
    }

    class AddContextFix : LocalQuickFix {
        override fun getName() = "Add domain-specific context"
        override fun getFamilyName() = "Prompt Improvements"
        override fun applyFix(project: Project, descriptor: ProblemDescriptor) {
            WriteCommandAction.runWriteCommandAction(project) {
                val document = descriptor.psiElement.containingFile.viewProvider.document
                val text = document.text
                val context = """
                    |Domain Context:
                    |-
                    |[Add relevant domain information]
                    |-
                    |
                """.trimMargin()
                document.insertString(0, context)
            }
        }
    }

    class AddTaskRequirementsFix : LocalQuickFix {
        override fun getName() = "Clarify task requirements"
        override fun getFamilyName() = "Prompt Improvements"
        override fun applyFix(project: Project, descriptor: ProblemDescriptor) {
            WriteCommandAction.runWriteCommandAction(project) {
                val document = descriptor.psiElement.containingFile.viewProvider.document
                val text = document.text
                val requirements = """
                    |Task Requirements:
                    |1. [Specific requirement]
                    |2. [Specific requirement]
                    |3. [Specific requirement]
                    |
                """.trimMargin()
                document.insertString(document.textLength, "\n\n$requirements")
            }
        }
    }

    class ApplyPatternFix(private val patternId: String) : LocalQuickFix {
        override fun getName() = "Apply prompt pattern"
        override fun getFamilyName() = "Prompt Improvements"
        override fun applyFix(project: Project, descriptor: ProblemDescriptor) {
            WriteCommandAction.runWriteCommandAction(project) {
                val document = descriptor.psiElement.containingFile.viewProvider.document
                val patternLibrary = PromptPatternLibrary.getInstance(project)
                val pattern = patternLibrary.findPatterns(document.text)
                    .find { it.id == patternId } ?: return@runWriteCommandAction
                
                document.replaceString(0, document.textLength, pattern.template)
            }
        }
    }

    class SwitchModelFix(private val model: String) : LocalQuickFix {
        override fun getName() = "Switch to $model"
        override fun getFamilyName() = "Prompt Improvements"
        override fun applyFix(project: Project, descriptor: ProblemDescriptor) {
            WriteCommandAction.runWriteCommandAction(project) {
                val document = descriptor.psiElement.containingFile.viewProvider.document
                val settings = PromptEfficiencySettings.getInstance(project)
                settings.setDefaultModel(model)
            }
        }
    }
} 