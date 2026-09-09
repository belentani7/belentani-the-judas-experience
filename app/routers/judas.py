from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.config import FREQ_HZ, LAT, LON, NODE, OS_VERSION
from app.database import get_db
from app.deps import optional_user
from app.models.experience import ExperienceChapter
from app.models.user import User
from app.services.hud import ARCHETYPES

router = APIRouter()


@router.get("/judas", response_class=HTMLResponse)
async def judas(
    request: Request,
    db: Session = Depends(get_db),
    user: User | None = Depends(optional_user),
):
    chapters = db.query(ExperienceChapter).order_by(ExperienceChapter.order_index).all()
    return request.app.state.templates.TemplateResponse(
        "judas.html",
        {
            "request": request,
            "user": user,
            "chapters": chapters,
            "archetypes": ARCHETYPES,
            "hud": {
                "lat": LAT,
                "lon": LON,
                "freq": FREQ_HZ,
                "node": NODE,
                "os": OS_VERSION,
            },
        },
    )
