#!/usr/bin/env python3
"""
Example script demonstrating the model translator functionality.
"""

from prompt_efficiency_suite.model_translator import ModelTranslator, ModelType


def main():
    # Initialize the model translator
    translator = ModelTranslator()

    # Example prompts for different models
    prompts = {
        ModelType.GPT4: """
        System: You are a helpful assistant.
        Context: This is some background information.
        Instruction: Please help me with this task step by step.
        """,
        ModelType.GPT35: """
        You are a helpful assistant. Given the following background information,
        please help me with this task step by step.
        """,
        ModelType.CLAUDE: """
        Human: I need help with a task. Here's some background information.
        Please provide step-by-step assistance.

        Assistant: I'll help you with that task. Let me break it down into steps.
        """,
        ModelType.LLAMA: """
        <s>[INST] You are a helpful assistant. Given the following background information,
        please help me with this task step by step. [/INST]
        """,
    }

    # Test translations between models
    print("Model Translation Examples:")
    print("=" * 50)

    for source_model, source_prompt in prompts.items():
        print(f"\nSource Model: {source_model.value}")
        print(f"Source Prompt:\n{source_prompt}")

        for target_model in ModelType:
            if target_model != source_model:
                translated_prompt = translator.translate_prompt(
                    prompt=source_prompt,
                    source_model=source_model,
                    target_model=target_model,
                )

                print(f"\nTranslated to {target_model.value}:")
                print(translated_prompt)
                print("-" * 30)


if __name__ == "__main__":
    main()
