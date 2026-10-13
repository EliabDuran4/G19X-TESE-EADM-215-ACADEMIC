from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Sistema de Observabilidad Documental"
    upload_dir: str = "uploads"

    keycloak_url: str = "http://localhost:8080"
    keycloak_realm: str = "observabilidad-documental"
    keycloak_client_id: str = "sistema-documental-app"
    keycloak_client_secret: str = ""

    database_url_documental: str = ""

    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_service_name: str = "backend-documental"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-5-5"
    ai_provider: str = "claude"
    ai_fallback_provider: str = ""
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:3b"
    ollama_timeout: float = 180.0

    class Config:
        env_file = ".env"


settings = Settings()