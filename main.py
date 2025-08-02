from src import app

# This is the entry point for your FastAPI application
# The actual app is defined in src/__init__.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
