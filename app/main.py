from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import ROOT, get_settings
from app.routers import api, auth, pages, studio
from app.services.store import get_store

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, session_cookie=settings.session_cookie)

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
app.include_router(studio.router)
app.include_router(api.router)


@app.get("/favicon.ico")
async def favicon():
    from fastapi.responses import RedirectResponse

    return RedirectResponse("/static/img/mark.svg")
