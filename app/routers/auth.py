from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER

from app.config import ROOT, get_settings
from app.services.store import get_store
from app.services.telemetry import hud_payload

templates = Jinja2Templates(directory=str(ROOT / "app" / "templates"))
router = APIRouter(prefix="/auth")


def ctx(request: Request, **extra) -> dict:
    return {
        "request": request,
        "settings": get_settings(),
        "hud": hud_payload(),
        "user": getattr(request.state, "user", None),
        **extra,
    }


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", ctx(request, error=None))


@router.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_store().authenticate(email, password)
    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            ctx(request, error="Signal rejected. Check the key."),
            status_code=401,
        )
    request.session["user_id"] = user.id
    return RedirectResponse("/studio", status_code=HTTP_303_SEE_OTHER)


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", ctx(request, error=None))


@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    display_name: str = Form(...),
):
    user = get_store().register(email, password, display_name)
    request.session["user_id"] = user.id
    return RedirectResponse("/studio", status_code=HTTP_303_SEE_OTHER)


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
