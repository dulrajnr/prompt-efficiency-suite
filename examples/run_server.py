#!/usr/bin/env python3
"""
Script to run the Prompt Efficiency Suite API server.
"""

import uvicorn
from prompt_efficiency_suite.main import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 