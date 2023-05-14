import uvicorn

from core.config import config

if __name__ == "__main__":
    uvicorn.run(
        host="0.0.0.0",
        app="core.server:app",
        reload=True if config.ENVIRONMENT != "production" else False,
        workers=1,
    )
