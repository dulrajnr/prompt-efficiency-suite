package com.prompt.efficiency.settings

import com.intellij.openapi.components.PersistentStateComponent
import com.intellij.openapi.components.State
import com.intellij.openapi.components.Storage
import com.intellij.util.xmlb.XmlSerializerUtil

@State(
    name = "PromptEfficiencySettings",
    storages = [Storage("prompt-efficiency.xml")]
)
class PromptEfficiencySettings : PersistentStateComponent<PromptEfficiencySettings> {
    var serverUrl: String = "https://api.prompt.com"
    var apiKey: String = ""
    var defaultModel: String = "gpt-4"
    var currency: String = "USD"
    var timeout: Int = 30
    var maxTokens: Int = 4096
    var autoAnalyze: Boolean = false
    var showSuggestions: Boolean = true
    var enableTemplates: Boolean = true

    override fun getState(): PromptEfficiencySettings = this

    override fun loadState(state: PromptEfficiencySettings) {
        XmlSerializerUtil.copyBean(state, this)
    }

    companion object {
        fun getInstance(): PromptEfficiencySettings {
            return com.intellij.openapi.components.ServiceManager.getService(PromptEfficiencySettings::class.java)
        }
    }
}
