from pathlib import Path
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME:str="AI Code security agent"
    APP_VERSION:str="1.0.0"
    DEBUG:bool=True

    GROQ_API_KEY:str

    BASE_DIR:Path=Path(__file__).resolve().parent.parent

    REPOSITORY_DIR:Path= BASE_DIR/'repositories'
    REPORT_DIR:Path=BASE_DIR/'reports'
    LOG_DIR:Path=BASE_DIR/'logs'

    DATABASE_URL: str

    MAX_FILES: int = 10
    MAX_LOC: int = 5000
    MAX_REPOSITORY_SIZE_MB: int = 20

    MODEL_NAME: str = "openai/gpt-oss-20b"
    TEMPERATURE: float = 0.2



    CHROMA_DB_DIR:Path=BASE_DIR/'vector_db'

    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    RAG_TOP_K: int = 5

    model_config=SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
        extra='ignore'
    )
    
settings=Settings()

settings.REPOSITORY_DIR.mkdir(exist_ok=True)
settings.REPORT_DIR.mkdir(exist_ok=True)
settings.LOG_DIR.mkdir(exist_ok=True)



