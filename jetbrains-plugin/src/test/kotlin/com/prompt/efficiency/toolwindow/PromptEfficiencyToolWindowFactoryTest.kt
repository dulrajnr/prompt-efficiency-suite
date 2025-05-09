package com.prompt.efficiency.toolwindow

import com.intellij.openapi.project.Project
import com.intellij.openapi.wm.ToolWindow
import com.intellij.openapi.wm.ToolWindowManager
import com.intellij.testFramework.fixtures.BasePlatformTestCase
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.mockito.Mockito.*
import javax.swing.JComponent

class PromptEfficiencyToolWindowFactoryTest : BasePlatformTestCase() {
    private lateinit var factory: PromptEfficiencyToolWindowFactory
    private lateinit var project: Project
    private lateinit var toolWindow: ToolWindow

    @BeforeEach
    override fun setUp() {
        super.setUp()
        project = mock(Project::class.java)
        toolWindow = mock(ToolWindow::class.java)
        factory = PromptEfficiencyToolWindowFactory()
    }

    @Test
    fun `test create tool window content`() {
        val contentManager = mock(ToolWindowManager::class.java)
        `when`(toolWindow.contentManager).thenReturn(contentManager)

        factory.createToolWindowContent(project, toolWindow)

        verify(contentManager).addContent(any())
    }

    @Test
    fun `test tool window panel creation`() {
        val contentManager = mock(ToolWindowManager::class.java)
        `when`(toolWindow.contentManager).thenReturn(contentManager)

        factory.createToolWindowContent(project, toolWindow)

        verify(contentManager).addContent(argThat { content ->
            content.component is PromptEfficiencyToolWindowPanel
        })
    }

    @Test
    fun `test tool window panel initialization`() {
        val contentManager = mock(ToolWindowManager::class.java)
        `when`(toolWindow.contentManager).thenReturn(contentManager)

        factory.createToolWindowContent(project, toolWindow)

        verify(contentManager).addContent(argThat { content ->
            val panel = content.component as PromptEfficiencyToolWindowPanel
            panel.componentCount > 0
        })
    }
} 