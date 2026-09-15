from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER
from pydantic import BaseModel, EmailStr, constr
from starlette.middleware.sessions import SessionMiddleware

from app.config import ROOT, get_settings
from app.services.store import get_store
from app.services.telemetry import hud_payload

templates = Jinja2Templates(directory=str(ROOT / "app" / "templates"))
router = APIRouter(prefix="/auth")

# Input validation models
class RegisterRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)
    display_name: constr(min_length=2, max_length=50)

class LoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=1, max_length=128)


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
    if not email or not password:
        return templates.TemplateResponse(
            "auth/login.html",
            ctx(request, error="Email and password are required"),
            status_code=400,
        )
    
    user = get_store().authenticate(email, password)
    if not user:
        # Rate limiting mitigation - generic error message
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
    # Input validation
    if not email or not password or not display_name:
        raise HTTPException(status_code=400, detail="All fields are required")
    
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    if len(display_name) < 2:
        raise HTTPException(status_code=400, detail="Display name must be at least 2 characters")
    
    # Check if email already exists
    store = get_store()
    existing_user = next((u for u in store.users.values() if u.email.lower() == email.lower()), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = store.register(email, password, display_name)
    request.session["user_id"] = user.id
    return RedirectResponse("/studio", status_code=HTTP_303_SEE_OTHER)


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
