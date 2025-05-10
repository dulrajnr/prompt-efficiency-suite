package com.prompt.efficiency.templates

import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.Assertions.*
import java.util.*

class PromptTemplateTest {
    private lateinit var templateManager: PromptTemplate

    @BeforeEach
    fun setup() {
        templateManager = PromptTemplate()
    }

    @Test
    fun `test add and get template`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            tags = mutableSetOf("greeting"),
            author = "Test User",
            isPublic = true
        )

        templateManager.addTemplate(template)
        val retrieved = templateManager.getTemplate("Test Template")

        assertNotNull(retrieved)
        assertEquals(template.name, retrieved?.name)
        assertEquals(template.description, retrieved?.description)
        assertEquals(template.content, retrieved?.content)
        assertEquals(template.category, retrieved?.category)
        assertEquals(template.variables, retrieved?.variables)
        assertEquals(template.tags, retrieved?.tags)
        assertEquals(template.author, retrieved?.author)
        assertEquals(template.isPublic, retrieved?.isPublic)
        assertTrue(retrieved?.versions?.isNotEmpty() == true)
    }

    @Test
    fun `test remove template`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name")
        )

        templateManager.addTemplate(template)
        templateManager.removeTemplate("Test Template")
        val retrieved = templateManager.getTemplate("Test Template")

        assertNull(retrieved)
    }

    @Test
    fun `test update template`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name")
        )

        templateManager.addTemplate(template)

        val updatedTemplate = PromptTemplate.Template(
            name = "Test Template",
            description = "An updated test template",
            content = "Hello \${name}, how are you?",
            category = "Test",
            variables = mutableListOf("name"),
            createdAt = template.createdAt
        )

        templateManager.updateTemplate("Test Template", updatedTemplate)
        val retrieved = templateManager.getTemplate("Test Template")

        assertNotNull(retrieved)
        assertEquals(updatedTemplate.description, retrieved?.description)
        assertEquals(updatedTemplate.content, retrieved?.content)
        assertNotEquals(template.updatedAt, retrieved?.updatedAt)
    }

    @Test
    fun `test get templates by category`() {
        val template1 = PromptTemplate.Template(
            name = "Template 1",
            description = "First template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name")
        )

        val template2 = PromptTemplate.Template(
            name = "Template 2",
            description = "Second template",
            content = "Goodbye \${name}!",
            category = "Test",
            variables = mutableListOf("name")
        )

        val template3 = PromptTemplate.Template(
            name = "Template 3",
            description = "Third template",
            content = "Welcome \${name}!",
            category = "Other",
            variables = mutableListOf("name")
        )

        templateManager.addTemplate(template1)
        templateManager.addTemplate(template2)
        templateManager.addTemplate(template3)

        val testTemplates = templateManager.getTemplatesByCategory("Test")
        assertEquals(2, testTemplates.size)
        assertTrue(testTemplates.all { it.category == "Test" })
    }

    @Test
    fun `test get templates by variable`() {
        val template1 = PromptTemplate.Template(
            name = "Template 1",
            description = "First template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name")
        )

        val template2 = PromptTemplate.Template(
            name = "Template 2",
            description = "Second template",
            content = "Goodbye \${name}!",
            category = "Test",
            variables = mutableListOf("name")
        )

        val template3 = PromptTemplate.Template(
            name = "Template 3",
            description = "Third template",
            content = "Welcome \${user}!",
            category = "Other",
            variables = mutableListOf("user")
        )

        templateManager.addTemplate(template1)
        templateManager.addTemplate(template2)
        templateManager.addTemplate(template3)

        val nameTemplates = templateManager.getTemplatesByVariable("name")
        assertEquals(2, nameTemplates.size)
        assertTrue(nameTemplates.all { it.variables.contains("name") })
    }

    @Test
    fun `test fill template`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}, welcome to \${place}!",
            category = "Test",
            variables = mutableListOf("name", "place")
        )

        templateManager.addTemplate(template)

        val variables = mapOf(
            "name" to "John",
            "place" to "New York"
        )

        val filled = templateManager.fillTemplate("Test Template", variables)
        assertEquals("Hello John, welcome to New York!", filled)
    }

    @Test
    fun `test fill template with missing variables`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}, welcome to \${place}!",
            category = "Test",
            variables = mutableListOf("name", "place")
        )

        templateManager.addTemplate(template)

        val variables = mapOf(
            "name" to "John"
        )

        assertThrows(IllegalArgumentException::class.java) {
            templateManager.fillTemplate("Test Template", variables)
        }
    }

    @Test
    fun `test export and import templates`() {
        val template1 = PromptTemplate.Template(
            name = "Template 1",
            description = "First template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name")
        )

        val template2 = PromptTemplate.Template(
            name = "Template 2",
            description = "Second template",
            content = "Goodbye \${name}!",
            category = "Test",
            variables = mutableListOf("name")
        )

        templateManager.addTemplate(template1)
        templateManager.addTemplate(template2)

        val json = templateManager.exportTemplates()
        val newManager = PromptTemplate()
        newManager.importTemplates(json)

        val imported1 = newManager.getTemplate("Template 1")
        val imported2 = newManager.getTemplate("Template 2")

        assertNotNull(imported1)
        assertNotNull(imported2)
        assertEquals(template1.content, imported1?.content)
        assertEquals(template2.content, imported2?.content)
    }

    @Test
    fun `test template versioning`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            author = "Test User"
        )

        templateManager.addTemplate(template)
        val initialVersion = template.versions.first()

        // Update template content
        val updatedTemplate = template.copy(
            content = "Hello \${name}, how are you?",
            updatedAt = Date()
        )
        templateManager.updateTemplate(template.name, updatedTemplate)

        val retrieved = templateManager.getTemplate("Test Template")
        assertNotNull(retrieved)
        assertEquals(2, retrieved?.versions?.size)
        assertNotEquals(initialVersion.content, retrieved?.versions?.last()?.content)
    }

    @Test
    fun `test template sharing`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            author = "Test User",
            isPublic = true
        )

        templateManager.addTemplate(template)
        templateManager.shareTemplate(template.name)

        val sharedTemplate = templateManager.sharedTemplates.values.first()
        assertEquals(template.name, sharedTemplate.template.name)
        assertEquals(template.author, sharedTemplate.sharedBy)
        assertTrue(sharedTemplate.isPublic)
    }

    @Test
    fun `test template downloading`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            author = "Test User"
        )

        templateManager.addTemplate(template)
        templateManager.shareTemplate(template.name)
        val sharedTemplate = templateManager.sharedTemplates.values.first()

        val downloadedTemplate = templateManager.downloadSharedTemplate(sharedTemplate.id)
        assertNotNull(downloadedTemplate)
        assertEquals(template.name, downloadedTemplate?.name)
        assertEquals(1, sharedTemplate.downloadCount)
    }

    @Test
    fun `test template reviews`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            author = "Test User"
        )

        templateManager.addTemplate(template)
        templateManager.shareTemplate(template.name)
        val sharedTemplate = templateManager.sharedTemplates.values.first()

        val review = PromptTemplate.Review(
            rating = 5,
            comment = "Great template!",
            reviewer = "Reviewer"
        )
        templateManager.addReview(sharedTemplate.id, review)

        val updatedSharedTemplate = templateManager.sharedTemplates[sharedTemplate.id]
        assertNotNull(updatedSharedTemplate)
        assertEquals(1, updatedSharedTemplate?.reviews?.size)
        assertEquals(5.0, updatedSharedTemplate?.rating)
    }

    @Test
    fun `test template filtering`() {
        val template1 = PromptTemplate.Template(
            name = "Template 1",
            description = "First template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            tags = mutableSetOf("greeting"),
            author = "User 1"
        )

        val template2 = PromptTemplate.Template(
            name = "Template 2",
            description = "Second template",
            content = "Goodbye \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            tags = mutableSetOf("farewell"),
            author = "User 2"
        )

        templateManager.addTemplate(template1)
        templateManager.addTemplate(template2)

        val testTemplates = templateManager.getTemplatesByCategory("Test")
        assertEquals(2, testTemplates.size)

        val greetingTemplates = templateManager.getTemplatesByTag("greeting")
        assertEquals(1, greetingTemplates.size)
        assertEquals("Template 1", greetingTemplates.first().name)

        val user1Templates = templateManager.getTemplatesByAuthor("User 1")
        assertEquals(1, user1Templates.size)
        assertEquals("Template 1", user1Templates.first().name)
    }

    @Test
    fun `test recent and popular templates`() {
        val template1 = PromptTemplate.Template(
            name = "Template 1",
            description = "First template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            author = "User 1"
        )

        val template2 = PromptTemplate.Template(
            name = "Template 2",
            description = "Second template",
            content = "Goodbye \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            author = "User 2"
        )

        templateManager.addTemplate(template1)
        templateManager.addTemplate(template2)

        // Make template1 more recent
        templateManager.getTemplate("Template 1")
        templateManager.getTemplate("Template 1")

        val recentTemplates = templateManager.getRecentTemplates(1)
        assertEquals(1, recentTemplates.size)
        assertEquals("Template 1", recentTemplates.first().name)

        // Share templates and download template2 more
        templateManager.shareTemplate("Template 1")
        templateManager.shareTemplate("Template 2")
        val sharedTemplate2 = templateManager.sharedTemplates.values.find { it.template.name == "Template 2" }
        repeat(5) { templateManager.downloadSharedTemplate(sharedTemplate2?.id ?: "") }

        val popularTemplates = templateManager.getPopularTemplates(1)
        assertEquals(1, popularTemplates.size)
        assertEquals("Template 2", popularTemplates.first().name)
    }

    @Test
    fun `test template export and import with versions`() {
        val template = PromptTemplate.Template(
            name = "Test Template",
            description = "A test template",
            content = "Hello \${name}!",
            category = "Test",
            variables = mutableListOf("name"),
            tags = mutableSetOf("greeting"),
            author = "Test User",
            isPublic = true
        )

        templateManager.addTemplate(template)

        // Update template to create a new version
        val updatedTemplate = template.copy(
            content = "Hello \${name}, how are you?",
            updatedAt = Date()
        )
        templateManager.updateTemplate(template.name, updatedTemplate)

        val json = templateManager.exportTemplates()
        val newManager = PromptTemplate()
        newManager.importTemplates(json)

        val importedTemplate = newManager.getTemplate("Test Template")
        assertNotNull(importedTemplate)
        assertEquals(2, importedTemplate?.versions?.size)
        assertEquals(updatedTemplate.content, importedTemplate?.content)
        assertEquals(template.tags, importedTemplate?.tags)
        assertEquals(template.author, importedTemplate?.author)
        assertEquals(template.isPublic, importedTemplate?.isPublic)
    }
}
