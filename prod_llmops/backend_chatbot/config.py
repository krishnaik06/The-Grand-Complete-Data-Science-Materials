from pydantic import BaseSettings

class Settings(BaseSettings):
    qdrant_host: str = "10.0.222.59"  #change it according to cluster ip address kubernetes
    qdrant_api_key: str
    openai_api_key: str

    class Config:
        env_file = ".env"



settings = Settings()


