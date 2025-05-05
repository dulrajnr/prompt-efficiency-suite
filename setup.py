from setuptools import setup, find_packages

setup(
    name="prompt_efficiency_suite",
    version="1.0.0",
    description="A comprehensive toolkit for optimizing and managing prompts",
    author="Prompt Efficiency Suite Team",
    author_email="support@promptefficiencysuite.com",
    packages=find_packages(),
    install_requires=[
        "spacy>=3.7.0",
        "tiktoken>=0.3.0",
        "numpy>=1.21.0",
        "Pillow>=10.0.0",
        "scikit-learn>=0.24.2",
        "pytest>=6.2.5",
        "black>=21.7b0",
        "isort>=5.9.3",
        "mypy>=0.910",
        "click>=8.0.0",
        "pyyaml>=6.0.0",
        "markdown>=3.5.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
) 