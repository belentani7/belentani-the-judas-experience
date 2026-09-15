from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import ROOT, get_settings
from app.models import CHAPTERS, GEMS, PILLARS
from app.services.store import get_store
from app.services.telemetry import hud_payload

templates = Jinja2Templates(directory=str(ROOT / "app" / "templates"))
router = APIRouter()


def ctx(request: Request, **extra) -> dict:
    user = getattr(request.state, "user", None)
    return {
        "request": request,
        "settings": get_settings(),
        "hud": hud_payload(),
        "user": user,
        **extra,
    }


@router.get("/", response_class=HTMLResponse)
async def portal(request: Request):
    store = get_store()
    user = getattr(request.state, "user", None)
    tenant_id = user.tenant_id if user else "ten_belentani"
    return templates.TemplateResponse(
        "portal.html",
        ctx(
            request,
            works=store.works_for(tenant_id) or list(store.works.values()),
            pillars=PILLARS,
            gems=GEMS,
        ),
    )


@router.get("/judas", response_class=HTMLResponse)
async def judas(request: Request):
    return templates.TemplateResponse(
        "judas.html",
        ctx(request, chapters=CHAPTERS, gems=GEMS, pillars=PILLARS),
    )


@router.get("/studio", response_class=HTMLResponse)
async def studio(request: Request):
    store = get_store()
    user = getattr(request.state, "user", None)
    tenant_id = user.tenant_id if user else "ten_belentani"
    return templates.TemplateResponse(
        "studio.html",
        ctx(
            request,
            works=store.works_for(tenant_id) or list(store.works.values()),
            releases=store.releases_for(tenant_id) or list(store.releases.values()),
        ),
    )


@router.get("/base43", response_class=HTMLResponse)
async def base43_interface(request: Request):
    return templates.TemplateResponse("base43.html", ctx(request))
