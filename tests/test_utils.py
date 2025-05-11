import pytest

from prompt_efficiency_suite.utils import (
    calculate_avg_word_length,
    calculate_quality_score,
    count_sentences,
    count_tokens,
    count_words,
)


def test_count_tokens() -> None:
    """Test counting tokens in a string."""
    text = "This is a test string"
    assert count_tokens(text) > 0
    assert count_tokens("") == 0
    assert count_tokens("Hello, world!") > count_tokens("Hello")


def test_count_words() -> None:
    """Test counting words in a string."""
    assert count_words("This is a test") == 4
    assert count_words("") == 0
    assert count_words("Hello, world!") == 2
    assert count_words("Multiple    spaces") == 2


def test_count_sentences() -> None:
    """Test counting sentences in a string."""
    assert count_sentences("This is a test. This is another test.") == 2
    assert count_sentences("") == 0
    assert count_sentences("Hello! How are you? I'm fine.") == 3
    assert count_sentences("No period here") == 1


def test_calculate_avg_word_length() -> None:
    """Test calculating average word length."""
    assert calculate_avg_word_length("This is a test") == 3.0
    assert calculate_avg_word_length("") == 0.0
    assert calculate_avg_word_length("Hello, world!") == 5.0
    assert calculate_avg_word_length("a b c") == 1.0


def test_calculate_quality_score() -> None:
    """Test calculating quality score."""
    metrics = {
        "token_count": 100,
        "word_count": 50,
        "sentence_count": 5,
        "avg_word_length": 4.5,
    }
    score = calculate_quality_score(metrics)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
