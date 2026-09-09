from datetime import datetime, timezone

from app.config import get_settings


def hud_payload() -> dict:
    s = get_settings()
    now = datetime.now(timezone.utc)
    return {
        "lat": s.latitude,
        "lon": s.longitude,
        "freq": f"{s.frequency_hz:.2f}Hz",
        "time": now.strftime("%H:%M:%S"),
        "node": s.node_id,
        "status": "CRITICAL",
        "os": "JUDAS_OS v12.0 // OMEGA_CLEAN // SYSTEM_READY",
        "cpu": "34.1%",
    }
