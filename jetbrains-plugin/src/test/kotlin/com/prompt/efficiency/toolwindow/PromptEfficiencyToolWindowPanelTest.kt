package com.prompt.efficiency.toolwindow

import com.intellij.openapi.editor.Editor
import com.intellij.openapi.editor.SelectionModel
import com.intellij.openapi.fileEditor.FileEditorManager
import com.intellij.openapi.project.Project
import com.intellij.testFramework.LightPlatformTestCase
import com.prompt.efficiency.api.PromptEfficiencyApiClient
import com.prompt.efficiency.settings.PromptEfficiencySettings
import okhttp3.*
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.mockito.Mockito.*
import org.mockito.kotlin.mock
import java.io.IOException
import javax.swing.JButton
import javax.swing.JList
import javax.swing.JTable
import javax.swing.table.DefaultTableModel
import org.junit.jupiter.api.Assertions.*

class PromptEfficiencyToolWindowPanelTest : LightPlatformTestCase() {
    private lateinit var project: Project
    private lateinit var editor: Editor
    private lateinit var selectionModel: SelectionModel
    private lateinit var settings: PromptEfficiencySettings
    private lateinit var client: OkHttpClient
    private lateinit var panel: PromptEfficiencyToolWindowPanel
    private lateinit var call: Call
    private lateinit var response: Response
    private lateinit var responseBody: ResponseBody
    private lateinit var mockProject: Project
    private lateinit var mockEditor: Editor
    private lateinit var mockSelectionModel: SelectionModel
    private lateinit var mockFileEditorManager: FileEditorManager
    private lateinit var mockApiClient: PromptEfficiencyApiClient
    private lateinit var mockSettings: PromptEfficiencySettings

    @BeforeEach
    fun setup() {
        super.setUp()
        mockProject = mock(Project::class.java)
        mockEditor = mock(Editor::class.java)
        mockSelectionModel = mock(SelectionModel::class.java)
        mockFileEditorManager = mock(FileEditorManager::class.java)
        mockApiClient = mock(PromptEfficiencyApiClient::class.java)
        mockSettings = mock(PromptEfficiencySettings::class.java)

        `when`(mockEditor.selectionModel).thenReturn(mockSelectionModel)
        `when`(mockProject.getService(FileEditorManager::class.java)).thenReturn(mockFileEditorManager)
        `when`(mockFileEditorManager.selectedTextEditor).thenReturn(mockEditor)

        project = mock()
        editor = mock()
        selectionModel = mock()
        settings = mock()
        client = mock()
        call = mock()
        response = mock()
        responseBody = mock()

        `when`(project.getService(Editor::class.java)).thenReturn(editor)
        `when`(editor.selectionModel).thenReturn(selectionModel)
        `when`(settings.serverUrl).thenReturn("http://localhost:8000")
        `when`(settings.apiKey).thenReturn("test-key")
        `when`(settings.defaultModel).thenReturn("gpt-4")
        `when`(settings.defaultCurrency).thenReturn("USD")

        panel = PromptEfficiencyToolWindowPanel(project)
    }

    @Test
    fun `test analyze selected text success`() {
        // Given
        val selectedText = "Test prompt"
        val responseJson = """{"clarity": 0.8, "structure": 0.7, "complexity": 0.6}"""
        
        `when`(selectionModel.selectedText).thenReturn(selectedText)
        `when`(response.isSuccessful).thenReturn(true)
        `when`(response.body()).thenReturn(responseBody)
        `when`(responseBody.string()).thenReturn(responseJson)
        `when`(client.newCall(any())).thenReturn(call)
        `when`(call.enqueue(any())).thenAnswer { invocation ->
            val callback = invocation.getArgument<Callback>(0)
            callback.onResponse(call, response)
        }

        // When
        panel.analyzeSelectedText(project)

        // Then
        verify(client).newCall(any())
        verify(call).enqueue(any())
    }

    @Test
    fun `test analyze selected text failure`() {
        // Given
        val selectedText = "Test prompt"
        val errorMessage = "Connection failed"
        
        `when`(selectionModel.selectedText).thenReturn(selectedText)
        `when`(client.newCall(any())).thenReturn(call)
        `when`(call.enqueue(any())).thenAnswer { invocation ->
            val callback = invocation.getArgument<Callback>(0)
            callback.onFailure(call, IOException(errorMessage))
        }

        // When
        panel.analyzeSelectedText(project)

        // Then
        verify(client).newCall(any())
        verify(call).enqueue(any())
    }

    @Test
    fun `test optimize selected text success`() {
        // Given
        val selectedText = "Test prompt"
        val responseJson = """{"optimized_prompt": "Optimized test prompt"}"""
        
        `when`(selectionModel.selectedText).thenReturn(selectedText)
        `when`(response.isSuccessful).thenReturn(true)
        `when`(response.body()).thenReturn(responseBody)
        `when`(responseBody.string()).thenReturn(responseJson)
        `when`(client.newCall(any())).thenReturn(call)
        `when`(call.enqueue(any())).thenAnswer { invocation ->
            val callback = invocation.getArgument<Callback>(0)
            callback.onResponse(call, response)
        }

        // When
        panel.optimizeSelectedText(project)

        // Then
        verify(client).newCall(any())
        verify(call).enqueue(any())
        verify(editor.document).setText("Optimized test prompt")
    }

    @Test
    fun `test estimate cost success`() {
        // Given
        val selectedText = "Test prompt"
        val responseJson = """{"total_cost": 0.5, "currency": "USD"}"""
        
        `when`(selectionModel.selectedText).thenReturn(selectedText)
        `when`(response.isSuccessful).thenReturn(true)
        `when`(response.body()).thenReturn(responseBody)
        `when`(responseBody.string()).thenReturn(responseJson)
        `when`(client.newCall(any())).thenReturn(call)
        `when`(call.enqueue(any())).thenAnswer { invocation ->
            val callback = invocation.getArgument<Callback>(0)
            callback.onResponse(call, response)
        }

        // When
        panel.estimateCost(project)

        // Then
        verify(client).newCall(any())
        verify(call).enqueue(any())
    }

    @Test
    fun `test scan repository success`() {
        // Given
        val responseJson = """{"files_scanned": 2, "prompts_found": 2}"""
        
        `when`(project.basePath).thenReturn("/test/path")
        `when`(response.isSuccessful).thenReturn(true)
        `when`(response.body()).thenReturn(responseBody)
        `when`(responseBody.string()).thenReturn(responseJson)
        `when`(client.newCall(any())).thenReturn(call)
        `when`(call.enqueue(any())).thenAnswer { invocation ->
            val callback = invocation.getArgument<Callback>(0)
            callback.onResponse(call, response)
        }

        // When
        panel.scanRepository(project)

        // Then
        verify(client).newCall(any())
        verify(call).enqueue(any())
    }

    @Test
    fun `test translate prompt success`() {
        // Given
        val selectedText = "Test prompt"
        val responseJson = """{"translated_prompt": "Translated test prompt"}"""
        
        `when`(selectionModel.selectedText).thenReturn(selectedText)
        `when`(response.isSuccessful).thenReturn(true)
        `when`(response.body()).thenReturn(responseBody)
        `when`(responseBody.string()).thenReturn(responseJson)
        `when`(client.newCall(any())).thenReturn(call)
        `when`(call.enqueue(any())).thenAnswer { invocation ->
            val callback = invocation.getArgument<Callback>(0)
            callback.onResponse(call, response)
        }

        // When
        panel.translatePrompt(project)

        // Then
        verify(client).newCall(any())
        verify(call).enqueue(any())
        verify(editor.document).setText("Translated test prompt")
    }

    @Test
    fun `test update table`() {
        // Given
        val json = org.json.JSONObject().apply {
            put("key1", "value1")
            put("key2", "value2")
        }

        // When
        panel.updateTable(json)

        // Then
        val table = panel.getTable()
        val model = table.model as DefaultTableModel
        assertEquals(2, model.rowCount)
        assertEquals("key1", model.getValueAt(0, 0))
        assertEquals("value1", model.getValueAt(0, 1))
        assertEquals("key2", model.getValueAt(1, 0))
        assertEquals("value2", model.getValueAt(1, 1))
    }

    fun testInitialState() {
        // Verify initial UI state
        assertNotNull(panel.getComponent(0)) // Toolbar
        assertNotNull(panel.getComponent(1)) // Main panel
        assertNotNull(panel.getComponent(2)) // Status panel

        // Verify buttons
        val toolbar = panel.getComponent(0) as JToolBar
        assertEquals(5, toolbar.componentCount)
        assertTrue(toolbar.getComponent(0) is JButton)
        assertTrue(toolbar.getComponent(1) is JButton)
        assertTrue(toolbar.getComponent(2) is JButton)
        assertTrue(toolbar.getComponent(3) is JButton)
        assertTrue(toolbar.getComponent(4) is JButton)
    }

    fun testAnalyzeSelectedText() {
        // Setup
        val testPrompt = "Test prompt"
        `when`(mockSelectionModel.selectedText).thenReturn(testPrompt)
        `when`(mockSettings.currency).thenReturn("USD")

        // Execute
        panel.analyzeSelectedText()

        // Verify
        verify(mockApiClient).analyzePrompt(testPrompt)
        val table = findComponent<JTable>(panel)
        val model = table.model as DefaultTableModel
        assertTrue(model.rowCount > 0)
    }

    fun testOptimizeSelectedText() {
        // Setup
        val testPrompt = "Test prompt"
        `when`(mockSelectionModel.selectedText).thenReturn(testPrompt)
        `when`(mockSettings.currency).thenReturn("USD")

        // Execute
        panel.optimizeSelectedText()

        // Verify
        verify(mockApiClient).optimizePrompt(testPrompt)
        val table = findComponent<JTable>(panel)
        val model = table.model as DefaultTableModel
        assertTrue(model.rowCount > 0)
    }

    fun testEstimateCost() {
        // Setup
        val testPrompt = "Test prompt"
        `when`(mockSelectionModel.selectedText).thenReturn(testPrompt)
        `when`(mockSettings.defaultModel).thenReturn("gpt-4")

        // Execute
        panel.estimateCost()

        // Verify
        verify(mockApiClient).estimateCost(testPrompt, "gpt-4")
        val table = findComponent<JTable>(panel)
        val model = table.model as DefaultTableModel
        assertTrue(model.rowCount > 0)
    }

    fun testScanRepository() {
        // Setup
        val testPath = "/test/path"
        `when`(mockProject.basePath).thenReturn(testPath)
        `when`(mockSettings.currency).thenReturn("USD")

        // Execute
        panel.scanRepository()

        // Verify
        verify(mockApiClient).scanRepository(testPath)
        val table = findComponent<JTable>(panel)
        val model = table.model as DefaultTableModel
        assertTrue(model.rowCount > 0)
    }

    fun testTranslatePrompt() {
        // Setup
        val testPrompt = "Test prompt"
        val targetLanguage = "es"
        `when`(mockSelectionModel.selectedText).thenReturn(testPrompt)

        // Execute
        panel.translatePrompt()

        // Verify
        verify(mockApiClient).translatePrompt(testPrompt, targetLanguage)
        val table = findComponent<JTable>(panel)
        val model = table.model as DefaultTableModel
        assertTrue(model.rowCount > 0)
    }

    fun testErrorHandling() {
        // Setup
        val testPrompt = "Test prompt"
        `when`(mockSelectionModel.selectedText).thenReturn(testPrompt)
        `when`(mockApiClient.analyzePrompt(testPrompt)).thenThrow(RuntimeException("Test error"))

        // Execute
        panel.analyzeSelectedText()

        // Verify error handling
        val statusLabel = findComponent<JLabel>(panel)
        assertTrue(statusLabel.text.contains("Test error"))
    }

    fun testUpdateSuggestions() {
        // Setup
        val suggestions = listOf("Suggestion 1", "Suggestion 2")

        // Execute
        panel.updateSuggestions(suggestions)

        // Verify
        val list = findComponent<JList<String>>(panel)
        assertEquals(2, list.model.size)
        assertEquals("Suggestion 1", list.model.getElementAt(0))
        assertEquals("Suggestion 2", list.model.getElementAt(1))
    }

    private inline fun <reified T : Component> findComponent(parent: Container): T {
        for (component in parent.components) {
            if (component is T) {
                return component
            }
            if (component is Container) {
                try {
                    return findComponent(component)
                } catch (e: NoSuchElementException) {
                    // Continue searching
                }
            }
        }
        throw NoSuchElementException("Component of type ${T::class.java} not found")
    }
} 