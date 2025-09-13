#!/usr/bin/env python3
"""
Simple script to run the ShotPin FastAPI application
"""

import uvicorn
import sys
import os

def main():
    """Run the FastAPI application"""
    try:
        # Change to the directory containing main.py
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        print("🚀 Starting ShotPin API Server...")
        print("📚 API Documentation will be available at: http://localhost:8000/docs")
        print("🔍 Health check available at: http://localhost:8000/")
        print("=" * 50)
        
        # Run the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
