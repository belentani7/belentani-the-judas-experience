from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.config import FREQ_HZ, LAT, LON, NODE, OS_VERSION
from app.database import get_db
from app.deps import optional_user
from app.models.user import User
from app.models.work import Work
from app.services.hud import ARCHETYPES, HUD_BOOT, PILLARS

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def portal(
    request: Request,
    db: Session = Depends(get_db),
    user: User | None = Depends(optional_user),
):
    works = db.query(Work).order_by(Work.id).all()
    return request.app.state.templates.TemplateResponse(
        "portal.html",
        {
            "request": request,
            "user": user,
            "works": works,
            "archetypes": ARCHETYPES,
            "pillars": PILLARS,
            "boot": HUD_BOOT,
            "hud": {
                "lat": LAT,
                "lon": LON,
                "freq": FREQ_HZ,
                "node": NODE,
                "os": OS_VERSION,
            },
        },
    )
