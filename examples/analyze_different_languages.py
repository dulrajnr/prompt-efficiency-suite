#!/usr/bin/env python3
"""
Example script demonstrating analysis of prompts with different languages.
"""

import asyncio
from prompt_efficiency_suite.analyzer import PromptAnalyzer
from prompt_efficiency_suite.model_translator import ModelType

async def analyze_prompt(analyzer, prompt, language_type):
    """Analyze a prompt and print the results."""
    print(f"\nAnalyzing {language_type} Language Prompt:")
    print("=" * 50)
    print(f"Prompt:\n{prompt}")
    
    result = analyzer.analyze_prompt(
        prompt=prompt,
        model=ModelType.GPT4
    )
    
    print("\nAnalysis Results:")
    print(f"Clarity Score: {result.metrics.clarity_score:.2f}")
    print(f"Structure Score: {result.metrics.structure_score:.2f}")
    print(f"Complexity Score: {result.metrics.complexity_score:.2f}")
    print(f"Token Estimate: {result.metrics.token_estimate}")
    print(f"Quality Score: {result.metrics.quality_score:.2f}")
    
    print("\nTop Improvement Suggestions:")
    for suggestion in result.metrics.improvement_suggestions[:3]:
        print(f"- {suggestion}")
    
    print("\nKey Patterns:")
    for pattern_type, patterns in result.pattern_analysis.items():
        if patterns:
            print(f"\n{pattern_type}:")
            for pattern in patterns[:2]:
                print(f"  - {pattern}")

async def main():
    # Initialize the analyzer
    analyzer = PromptAnalyzer()
    
    # Example prompts with different languages
    prompts = {
        "English": """
        System: You are a helpful assistant.
        Context: This is the background information.
        Instruction: Help me with this task.
        Example: Here's an example.
        """,
        
        "Spanish": """
        Sistema: Eres un asistente útil.
        Contexto: Esta es la información de fondo.
        Instrucción: Ayúdame con esta tarea.
        Ejemplo: Aquí hay un ejemplo.
        """,
        
        "French": """
        Système: Vous êtes un assistant utile.
        Contexte: Voici les informations de base.
        Instruction: Aidez-moi avec cette tâche.
        Exemple: Voici un exemple.
        """,
        
        "German": """
        System: Sie sind ein hilfreicher Assistent.
        Kontext: Dies sind die Hintergrundinformationen.
        Anweisung: Helfen Sie mir bei dieser Aufgabe.
        Beispiel: Hier ist ein Beispiel.
        """,
        
        "Italian": """
        Sistema: Sei un assistente utile.
        Contesto: Questa è l'informazione di base.
        Istruzione: Aiutami con questo compito.
        Esempio: Ecco un esempio.
        """,
        
        "Portuguese": """
        Sistema: Você é um assistente útil.
        Contexto: Esta é a informação de fundo.
        Instrução: Ajude-me com esta tarefa.
        Exemplo: Aqui está um exemplo.
        """
    }
    
    # Analyze each prompt
    for language_type, prompt in prompts.items():
        await analyze_prompt(analyzer, prompt, language_type)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 