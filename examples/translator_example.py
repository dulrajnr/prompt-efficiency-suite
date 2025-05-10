from prompt_efficiency_suite.translator.model_types import ModelType
from prompt_efficiency_suite.translator.translator import PromptComponents, PromptTranslator


def print_translation_result(result):
    """Print the results of a translation."""
    print("\n=== Translation Result ===")
    print("\nTranslated Prompt:")
    print(result.translated_prompt)

    print("\nValidation:")
    if result.validation_result.is_valid:
        print("✓ Prompt is valid")
    else:
        print("✗ Prompt is invalid")
        for error in result.validation_result.errors:
            print(f"  - Error: {error}")

    for warning in result.validation_result.warnings:
        print(f"  - Warning: {warning}")

    if result.optimization_result:
        print("\nOptimization:")
        for improvement in result.optimization_result.improvements:
            print(f"  - {improvement}")
        print(f"  - Token savings: {result.optimization_result.estimated_token_savings}")

    print(f"\nEstimated cost: ${result.estimated_cost:.4f}")


def main():
    # Create translator instance
    translator = PromptTranslator()

    # Example 1: Translate a string prompt with validation and optimization
    gpt_prompt = """
    System: You are a helpful AI assistant that can write code.

    Instruction: Please write a Python function that calculates the Fibonacci sequence.

    Example:
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)

    Context: This is for a beginner Python programming tutorial.
    """

    # Translate from GPT-4 to Claude
    result = translator.translate(gpt_prompt, ModelType.GPT4, ModelType.CLAUDE, optimize=True)
    print("=== GPT-4 to Claude Translation ===")
    print_translation_result(result)

    # Example 2: Translate using PromptComponents with validation
    components = PromptComponents(
        system_message="You are a creative writing assistant.",
        instruction="Write a short story about a robot learning to paint.",
        examples=[
            "The robot's brush strokes were precise but lacked emotion.",
            "With each painting, the robot's understanding of art grew.",
            "The robot's first abstract piece surprised everyone.",
            "The robot's color choices became more intuitive over time.",
        ],
        context="This is for an art and technology workshop.",
        constraints="Please ensure that the story is under 500 words.",
        output_format="Return the story in markdown format.",
    )

    # Translate from Claude to GPT-3.5
    result = translator.translate(components, ModelType.CLAUDE, ModelType.GPT35, optimize=True)
    print("\n=== Claude to GPT-3.5 Translation ===")
    print_translation_result(result)

    # Example 3: Invalid prompt (missing instruction)
    invalid_components = PromptComponents(system_message="You are a helpful assistant.", context="This is a test.")

    # Try to translate invalid prompt
    result = translator.translate(invalid_components, ModelType.GPT4, ModelType.CLAUDE, optimize=True)
    print("\n=== Invalid Prompt Translation ===")
    print_translation_result(result)


if __name__ == "__main__":
    main()
