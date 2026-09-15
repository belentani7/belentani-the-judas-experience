from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import ROOT, get_settings
from app.routers import api, auth, base43, pages, studio
from app.services.store import get_store

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*.vercel.app"])
app.add_middleware(GZipMiddleware)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, session_cookie=settings.session_cookie)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'"
    
    return response

# Force HTTPS in production
if not settings.debug:
    app.add_middleware(HTTPSRedirectMiddleware)

static_dir = ROOT / "app" / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.middleware("http")
async def attach_user(request: Request, call_next):
    store = get_store()
    user_id = request.session.get("user_id") if hasattr(request, "session") else None
    request.state.user = store.users.get(user_id) if user_id else None
    return await call_next(request)


app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(base43.router)
app.include_router(studio.router)
app.include_router(api.router)


@app.get("/favicon.ico")
async def favicon():
    from fastapi.responses import RedirectResponse

    return RedirectResponse("/static/img/mark.svg")
