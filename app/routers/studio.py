from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from app.services.store import get_store

router = APIRouter(prefix="/studio")


@router.post("/works", response_class=HTMLResponse)
async def create_work(
    request: Request,
    title: str = Form(...),
    synopsis: str = Form(""),
    kind: str = Form("work"),
):
    user = getattr(request.state, "user", None)
    tenant_id = user.tenant_id if user else "ten_belentani"
    get_store().add_work(tenant_id, title, synopsis, kind)
    return RedirectResponse("/studio", status_code=HTTP_303_SEE_OTHER)
