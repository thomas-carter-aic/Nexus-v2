"""
Simplified FastAPI Application for testing.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="AI-Native PaaS Platform",
        description="AI-Native Cloud-Native Platform-as-a-Service",
        version="1.0.0"
    )
    
    @app.get("/", response_model=Dict[str, Any])
    async def root():
        """Welcome endpoint"""
        return {
            "message": "Welcome to AI-Native PaaS Platform",
            "version": "1.0.0",
            "status": "running"
        }
    
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint"""
        return HealthResponse(
            status="healthy",
            message="API is running"
        )
    
    return app


# For testing
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
