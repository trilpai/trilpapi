from fastapi import FastAPI
from src.core.logging import setup_logging
from src.core.constants import PROJECT_ROOT
from src.routes import router as app_router

# Initialize logging
setup_logging()

# Create the FastAPI app instance
app = FastAPI(
    title="Trilp API",
    description=(
        "A high-performance and scalable API built with FastAPI for managing "
        "offices, users, roles, privileges, and more."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Include the central router from routes.py
app.include_router(app_router)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint for testing the API.

    Returns:
        dict: A welcome message to confirm that the API is running.

    Example:
        {
            "message": "Welcome to Trilp API!"
        }
    """
    return {"message": f"Welcome to {app.title}!"}

if __name__ == "__main__":
    import uvicorn
    # Optionally read environment variables for host and port, or use defaults
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
    )
