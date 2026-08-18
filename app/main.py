from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.router import router
from app.config import settings
from app.database import Base,engine
from models.vector_model import RepositoryChunk

with engine.begin() as connection:
    connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

Base.metadata.create_all(bind=engine)

app =FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="""
AI Code Review & Security Agent

Features:
- Clone GitHub repositories
- Run Bandit
- Run Semgrep
- AI Code Review
- AI Repository Assistant (RAG)
"""
)

app.include_router(router)

@app.get("/")
async def root():
    return{
        "application":settings.APP_NAME,
        "version":settings.APP_VERSION,
        "status":"Running"
    }

@app.get("/health")
async def health_check():
    return{
        "status":"healthy"
    }

# @app.get("/config")
# async def configuration():
#     """
#     Useful while developing.
#     Remove in production.
#     """
#     return {
#         "repository_directory": str(settings.REPOSITORY_DIR),
#         "reports_directory": str(settings.REPORT_DIR),
#         "max_files": settings.MAX_FILES,
#         "max_loc": settings.MAX_LOC,
#         "max_repository_size_mb": settings.MAX_REPOSITORY_SIZE_MB,
#         "model": settings.MODEL_NAME
#     }

@app.exception_handler(Exception)
async def global_exception_handler(request,exc):
    return JSONResponse(
        status_code=500,
        content={
            "status":"error",
            "message":str(exc)
        }
    )

    
