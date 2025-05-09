#!/usr/bin/env python3
"""
Script to test the Prompt Efficiency Suite API endpoints.
"""

import asyncio
import httpx
import json

async def test_analyze_endpoint():
    """Test the /analyze endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/analyze",
            json={
                "prompt": """
                System: You are a helpful assistant.
                Context: This is some background information.
                Instruction: Please help me with this task step by step.
                """,
                "model": "gpt-4",
                "metadata": {
                    "key": "value",
                    "number": 42
                }
            }
        )
        
        print("\nAnalyze Endpoint Response:")
        print("=" * 50)
        print(json.dumps(response.json(), indent=2))

async def test_quick_analyze_endpoint():
    """Test the /analyze/quick endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v1/analyze/quick",
            params={
                "prompt": """
                System: You are a helpful assistant.
                Context: This is some background information.
                Instruction: Please help me with this task step by step.
                """
            }
        )
        
        print("\nQuick Analyze Endpoint Response:")
        print("=" * 50)
        print(json.dumps(response.json(), indent=2))

async def test_patterns_endpoint():
    """Test the /analyze/patterns endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v1/analyze/patterns",
            params={
                "prompt": """
                This is really very important.
                Please clearly explain this complex task.
                """
            }
        )
        
        print("\nPatterns Endpoint Response:")
        print("=" * 50)
        print(json.dumps(response.json(), indent=2))

async def test_structure_endpoint():
    """Test the /analyze/structure endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v1/analyze/structure",
            params={
                "prompt": """
                System: You are a helpful assistant.
                Context: Some background.
                Instruction: Do something.
                Example: Here's how.
                """
            }
        )
        
        print("\nStructure Endpoint Response:")
        print("=" * 50)
        print(json.dumps(response.json(), indent=2))

async def main():
    """Run all API tests."""
    print("Testing Prompt Efficiency Suite API...")
    
    try:
        await test_analyze_endpoint()
        await test_quick_analyze_endpoint()
        await test_patterns_endpoint()
        await test_structure_endpoint()
        
        print("\nAll tests completed successfully!")
        
    except httpx.ConnectError:
        print("\nError: Could not connect to the API server.")
        print("Make sure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 