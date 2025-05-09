plugins {
    id("java")
    id("org.jetbrains.kotlin.jvm") version "1.8.21"
    id("org.jetbrains.intellij") version "1.13.3"
    id("org.jetbrains.dokka") version "1.8.20"
    id("jacoco")
}

group = "com.prompt.efficiency"
version = "1.0.0"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.jfree:jfreechart:1.5.4")
    implementation("com.google.code.gson:gson:2.10.1")
    implementation("org.json:json:20231013")
    implementation("com.squareup.okhttp3:okhttp:4.11.0")
    implementation("com.opencsv:opencsv:5.7.1")
    
    // Testing
    testImplementation("org.junit.jupiter:junit-jupiter:5.9.2")
    testImplementation("org.mockito:mockito-core:5.3.1")
    testImplementation("org.mockito.kotlin:mockito-kotlin:5.1.0")
    testImplementation("com.intellij.remoterobot:remote-robot:0.11.16")
    testImplementation("org.jetbrains.kotlin:kotlin-test")
}

intellij {
    version.set("2023.1")
    type.set("IC")
    plugins.set(listOf("java", "Kotlin"))
    updateSinceUntilBuild.set(false)
}

tasks {
    withType<JavaCompile> {
        sourceCompatibility = "17"
        targetCompatibility = "17"
    }
    
    withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
        kotlinOptions.jvmTarget = "17"
    }

    patchPluginXml {
        sinceBuild.set("231")
        untilBuild.set("241.*")
    }

    signPlugin {
        certificateChain.set(System.getenv("CERTIFICATE_CHAIN"))
        privateKey.set(System.getenv("PRIVATE_KEY"))
        password.set(System.getenv("PRIVATE_KEY_PASSWORD"))
    }

    publishPlugin {
        token.set(System.getenv("PUBLISH_TOKEN"))
    }

    test {
        useJUnitPlatform()
        finalizedBy(jacocoTestReport)
    }

    jacocoTestReport {
        reports {
            xml.required.set(true)
            html.required.set(true)
        }
    }

    dokkaHtml {
        outputDirectory.set(file("${project.buildDir}/dokka"))
        dokkaSourceSets {
            named("main") {
                moduleName.set("Prompt Efficiency Plugin")
                includes.from("Module.md")
            }
        }
    }

    buildSearchableOptions {
        enabled = false
    }

    runIde {
        autoReloadPlugins.set(true)
        systemProperty("idea.log.debug.categories", "#com.prompt.efficiency")
    }

    runPluginVerifier {
        ideVersions.set(listOf("2023.1", "2023.2", "2023.3"))
    }
} 