package com.prompt.efficiency.templates

import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.util.xmlb.XmlSerializerUtil
import org.json.JSONObject
import java.util.*

@State(
    name = "PromptTemplates",
    storages = [Storage("prompt-templates.xml")]
)
class PromptTemplate : PersistentStateComponent<PromptTemplate> {
    var templates: MutableMap<String, Template> = mutableMapOf()
    var categories: MutableSet<String> = mutableSetOf()
    var sharedTemplates: MutableMap<String, SharedTemplate> = mutableMapOf()

    data class Template(
        var name: String = "",
        var description: String = "",
        var content: String = "",
        var category: String = "",
        var variables: MutableList<String> = mutableListOf(),
        var createdAt: Date = Date(),
        var updatedAt: Date = Date(),
        var versions: MutableList<Version> = mutableListOf(),
        var tags: MutableSet<String> = mutableSetOf(),
        var isPublic: Boolean = false,
        var author: String = "",
        var lastUsed: Date? = null
    )

    data class Version(
        var number: Int = 1,
        var content: String = "",
        var description: String = "",
        var createdAt: Date = Date(),
        var createdBy: String = "",
        var changes: String = ""
    )

    data class SharedTemplate(
        var id: String = UUID.randomUUID().toString(),
        var template: Template = Template(),
        var sharedBy: String = "",
        var sharedAt: Date = Date(),
        var permissions: MutableSet<String> = mutableSetOf(),
        var isPublic: Boolean = false,
        var downloadCount: Int = 0,
        var rating: Double = 0.0,
        var reviews: MutableList<Review> = mutableListOf()
    )

    data class Review(
        var id: String = UUID.randomUUID().toString(),
        var rating: Int = 0,
        var comment: String = "",
        var reviewer: String = "",
        var createdAt: Date = Date()
    )

    override fun getState(): PromptTemplate {
        return this
    }

    override fun loadState(state: PromptTemplate) {
        XmlSerializerUtil.copyBean(state, this)
    }

    fun addTemplate(template: Template) {
        template.versions.add(Version(content = template.content))
        templates[template.name] = template
        categories.add(template.category)
        template.updatedAt = Date()
    }

    fun removeTemplate(name: String) {
        templates.remove(name)
        updateCategories()
    }

    fun updateTemplate(name: String, template: Template) {
        val existingTemplate = templates[name]
        if (existingTemplate != null) {
            // Create new version if content changed
            if (existingTemplate.content != template.content) {
                val newVersion = Version(
                    number = existingTemplate.versions.size + 1,
                    content = template.content,
                    description = "Updated content",
                    createdAt = Date(),
                    createdBy = template.author
                )
                template.versions.add(newVersion)
            }
            template.createdAt = existingTemplate.createdAt
        }
        templates[name] = template
        categories.add(template.category)
        template.updatedAt = Date()
    }

    fun getTemplate(name: String): Template? {
        val template = templates[name]
        template?.lastUsed = Date()
        return template
    }

    fun getTemplatesByCategory(category: String): List<Template> {
        return templates.values.filter { it.category == category }
    }

    fun getTemplatesByVariable(variable: String): List<Template> {
        return templates.values.filter { it.variables.contains(variable) }
    }

    fun getTemplatesByTag(tag: String): List<Template> {
        return templates.values.filter { it.tags.contains(tag) }
    }

    fun getTemplatesByAuthor(author: String): List<Template> {
        return templates.values.filter { it.author == author }
    }

    fun getRecentTemplates(limit: Int = 10): List<Template> {
        return templates.values
            .filter { it.lastUsed != null }
            .sortedByDescending { it.lastUsed }
            .take(limit)
    }

    fun getPopularTemplates(limit: Int = 10): List<Template> {
        return sharedTemplates.values
            .sortedByDescending { it.downloadCount }
            .take(limit)
            .map { it.template }
    }

    fun shareTemplate(name: String, isPublic: Boolean = false, permissions: Set<String> = emptySet()) {
        val template = templates[name] ?: return
        val sharedTemplate = SharedTemplate(
            template = template,
            sharedBy = template.author,
            permissions = permissions.toMutableSet(),
            isPublic = isPublic
        )
        sharedTemplates[sharedTemplate.id] = sharedTemplate
    }

    fun downloadSharedTemplate(id: String): Template? {
        val sharedTemplate = sharedTemplates[id] ?: return null
        sharedTemplate.downloadCount++
        return sharedTemplate.template
    }

    fun addReview(templateId: String, review: Review) {
        val sharedTemplate = sharedTemplates[templateId] ?: return
        sharedTemplate.reviews.add(review)
        // Update average rating
        sharedTemplate.rating = sharedTemplate.reviews.map { it.rating }.average()
    }

    fun fillTemplate(name: String, variables: Map<String, String>): String {
        val template = templates[name] ?: throw IllegalArgumentException("Template not found: $name")
        var content = template.content

        // Replace variables in the template
        variables.forEach { (key, value) ->
            content = content.replace("\${$key}", value)
        }

        // Check for any remaining variables
        val remainingVariables = Regex("\\$\\{([^}]+)\\}").findAll(content)
            .map { it.groupValues[1] }
            .toList()

        if (remainingVariables.isNotEmpty()) {
            throw IllegalArgumentException("Missing variables: ${remainingVariables.joinToString()}")
        }

        template.lastUsed = Date()
        return content
    }

    fun exportTemplates(): String {
        val json = JSONObject()
        templates.forEach { (name, template) ->
            json.put(name, JSONObject().apply {
                put("name", template.name)
                put("description", template.description)
                put("content", template.content)
                put("category", template.category)
                put("variables", template.variables)
                put("createdAt", template.createdAt.time)
                put("updatedAt", template.updatedAt.time)
                put("versions", template.versions.map { version ->
                    JSONObject().apply {
                        put("number", version.number)
                        put("content", version.content)
                        put("description", version.description)
                        put("createdAt", version.createdAt.time)
                        put("createdBy", version.createdBy)
                        put("changes", version.changes)
                    }
                })
                put("tags", template.tags)
                put("isPublic", template.isPublic)
                put("author", template.author)
                put("lastUsed", template.lastUsed?.time)
            })
        }
        return json.toString(2)
    }

    fun importTemplates(json: String) {
        val jsonObj = JSONObject(json)
        jsonObj.keys().forEach { key ->
            val templateObj = jsonObj.getJSONObject(key)
            val template = Template(
                name = templateObj.getString("name"),
                description = templateObj.getString("description"),
                content = templateObj.getString("content"),
                category = templateObj.getString("category"),
                variables = templateObj.getJSONArray("variables")
                    .map { it.toString() }
                    .toMutableList(),
                createdAt = Date(templateObj.getLong("createdAt")),
                updatedAt = Date(templateObj.getLong("updatedAt")),
                versions = templateObj.getJSONArray("versions").map { versionObj ->
                    val version = versionObj as JSONObject
                    Version(
                        number = version.getInt("number"),
                        content = version.getString("content"),
                        description = version.getString("description"),
                        createdAt = Date(version.getLong("createdAt")),
                        createdBy = version.getString("createdBy"),
                        changes = version.getString("changes")
                    )
                }.toMutableList(),
                tags = templateObj.getJSONArray("tags")
                    .map { it.toString() }
                    .toMutableSet(),
                isPublic = templateObj.getBoolean("isPublic"),
                author = templateObj.getString("author"),
                lastUsed = if (templateObj.has("lastUsed")) Date(templateObj.getLong("lastUsed")) else null
            )
            addTemplate(template)
        }
    }

    private fun updateCategories() {
        categories = templates.values.map { it.category }.toMutableSet()
    }

    companion object {
        fun getInstance(): PromptTemplate {
package com.prompt.efficiency.templates

import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.util.xmlb.XmlSerializerUtil
import org.json.JSONObject
import java.util.*

@State(
    name = "PromptTemplates",
    storages = [Storage("prompt-templates.xml")]
)
class PromptTemplate : PersistentStateComponent<PromptTemplate> {
    var templates: MutableMap<String, Template> = mutableMapOf()
    var categories: MutableSet<String> = mutableSetOf()

    data class Template(
        var name: String = "",
        var description: String = "",
        var content: String = "",
        var category: String = "",
        var variables: MutableList<String> = mutableListOf(),
        var createdAt: Date = Date(),
        var updatedAt: Date = Date()
    )

    override fun getState(): PromptTemplate {
        return this
    }

    override fun loadState(state: PromptTemplate) {
        XmlSerializerUtil.copyBean(state, this)
    }

    fun addTemplate(template: Template) {
        templates[template.name] = template
        categories.add(template.category)
        template.updatedAt = Date()
    }

    fun removeTemplate(name: String) {
        templates.remove(name)
        updateCategories()
    }

    fun updateTemplate(name: String, template: Template) {
        templates[name] = template
        categories.add(template.category)
        template.updatedAt = Date()
    }

    fun getTemplate(name: String): Template? {
        return templates[name]
    }

    fun getTemplatesByCategory(category: String): List<Template> {
        return templates.values.filter { it.category == category }
    }

    fun getTemplatesByVariable(variable: String): List<Template> {
        return templates.values.filter { it.variables.contains(variable) }
    }

    fun fillTemplate(name: String, variables: Map<String, String>): String {
        val template = templates[name] ?: throw IllegalArgumentException("Template not found: $name")
        var content = template.content

        // Replace variables in the template
        variables.forEach { (key, value) ->
            content = content.replace("\${$key}", value)
        }

        // Check for any remaining variables
        val remainingVariables = Regex("\\$\\{([^}]+)\\}").findAll(content)
            .map { it.groupValues[1] }
            .toList()

        if (remainingVariables.isNotEmpty()) {
            throw IllegalArgumentException("Missing variables: ${remainingVariables.joinToString()}")
        }

        return content
    }

    fun exportTemplates(): String {
        val json = JSONObject()
        templates.forEach { (name, template) ->
            json.put(name, JSONObject().apply {
                put("name", template.name)
                put("description", template.description)
                put("content", template.content)
                put("category", template.category)
                put("variables", template.variables)
                put("createdAt", template.createdAt.time)
                put("updatedAt", template.updatedAt.time)
            })
        }
        return json.toString(2)
    }

    fun importTemplates(json: String) {
        val jsonObj = JSONObject(json)
        jsonObj.keys().forEach { key ->
            val templateObj = jsonObj.getJSONObject(key)
            val template = Template(
                name = templateObj.getString("name"),
                description = templateObj.getString("description"),
                content = templateObj.getString("content"),
                category = templateObj.getString("category"),
                variables = templateObj.getJSONArray("variables")
                    .map { it.toString() }
                    .toMutableList(),
                createdAt = Date(templateObj.getLong("createdAt")),
                updatedAt = Date(templateObj.getLong("updatedAt"))
            )
            addTemplate(template)
        }
    }

    private fun updateCategories() {
        categories = templates.values.map { it.category }.toMutableSet()
    }

    companion object {
        fun getInstance(): PromptTemplate {
            return com.intellij.openapi.components.ServiceManager.getService(PromptTemplate::class.java)
        }
    }
} 