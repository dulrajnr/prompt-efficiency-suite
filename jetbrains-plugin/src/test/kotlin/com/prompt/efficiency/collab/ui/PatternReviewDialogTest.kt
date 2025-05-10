package com.prompt.efficiency.collab.ui

import com.intellij.testFramework.LightPlatformTestCase
import com.prompt.efficiency.collab.TeamPatternManager
import java.util.*
import javax.swing.JTextArea
import javax.swing.JComboBox

class PatternReviewDialogTest : LightPlatformTestCase() {
    private lateinit var dialog: PatternReviewDialog
    private lateinit var pattern: TeamPatternManager.TeamPattern

    override fun setUp() {
        super.setUp()
        pattern = TeamPatternManager.TeamPattern(
            id = UUID.randomUUID().toString(),
            name = "Test Pattern",
            description = "Test Description",
            template = "Test Template",
            category = "Test Category",
            model = "gpt-4",
            tags = setOf("test", "example"),
            author = "Test User",
            status = TeamPatternManager.PatternStatus.DRAFT,
            version = 1,
            usageCount = 10,
            successRate = 0.85,
            reviews = mutableListOf()
        )
        dialog = PatternReviewDialog(project, pattern)
    }

    fun testInitialState() {
        // Check initial field values
        assertEquals(TeamPatternManager.ReviewStatus.PENDING, (findComboBox("Status:") as JComboBox<TeamPatternManager.ReviewStatus>).selectedItem)
        assertEquals("", findTextArea("Comments:").text)

        // Check pattern info display
        val templateArea = dialog.contentPane.findComponent {
            it is JTextArea && it.text == pattern.template && !it.isEditable
        } as JTextArea
        assertEquals(pattern.template, templateArea.text)
    }

    fun testValidation() {
        // Test empty comments
        assertNotNull(dialog.doValidate())

        // Add comments
        findTextArea("Comments:").text = "Test review comments"

        // Test validation passes
        assertNull(dialog.doValidate())
    }

    fun testGetReview() {
        // Fill fields
        (findComboBox("Status:") as JComboBox<TeamPatternManager.ReviewStatus>).selectedItem = TeamPatternManager.ReviewStatus.APPROVED
        findTextArea("Comments:").text = "Test review comments"

        // Get review
        val review = dialog.getReview()

        // Check review values
        assertEquals(pattern.id, review.patternId)
        assertEquals("Current User", review.reviewerId) // TODO: Update when actual user is implemented
        assertEquals(TeamPatternManager.ReviewStatus.APPROVED, review.status)
        assertEquals("Test review comments", review.comments)
        assertNotNull(review.createdAt)
    }

    private fun findTextArea(label: String): JTextArea {
        return dialog.contentPane.findComponent {
            it is JTextArea && it.parent?.parent?.findComponent { it is JLabel && it.text == label } != null
        } as JTextArea
    }

    private fun findComboBox(label: String): JComboBox<*> {
        return dialog.contentPane.findComponent {
            it is JComboBox<*> && it.parent?.findComponent { it is JLabel && it.text == label } != null
        } as JComboBox<*>
    }
}
