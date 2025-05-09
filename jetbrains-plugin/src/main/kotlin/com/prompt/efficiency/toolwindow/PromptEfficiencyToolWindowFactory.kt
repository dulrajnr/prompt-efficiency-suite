package com.prompt.efficiency.toolwindow

import com.intellij.openapi.project.Project
import com.intellij.openapi.wm.ToolWindow
import com.intellij.openapi.wm.ToolWindowFactory
import com.intellij.ui.content.ContentFactory

class PromptEfficiencyToolWindowFactory : ToolWindowFactory {
    override fun createToolWindowContent(project: Project, toolWindow: ToolWindow) {
        val contentFactory = ContentFactory.getInstance()
        val content = contentFactory.createContent(
            PromptEfficiencyToolWindowPanel(project),
            "Prompt Efficiency",
            false
        )
        toolWindow.contentManager.addContent(content)
    }
} 