from pydantic import BaseSettings

class Settings(BaseSettings) :
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://default:secret@192.168.0.115/faculdade'
    JWT_SECRET: str = ''
    class Config:
        case_sensitive = True
        
settings: Settings = Settings()