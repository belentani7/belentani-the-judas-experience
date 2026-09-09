from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BELENTANI_", extra="ignore")

    app_name: str = "Belentani The Judas Experience"
    studio_name: str = "DUCK STUDIOS"
    node_id: str = "JUDAS-CORE-07"
    frequency_hz: float = 432.0
    latitude: float = 41.3851
    longitude: float = 2.1734
    secret_key: str = "change-me-in-production-omega-core"
    session_cookie: str = "judas_session"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 4320
    data_dir: Path = ROOT / "data"

    # Visual system — extracted from belentani.es Judas Era language
    void: str = "#050203"
    blood: str = "#8a0d18"
    neon: str = "#ff1a3c"
    crystal: str = "rgba(255, 255, 255, 0.08)"
    gold_key: str = "#c9a84c"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    return settings
