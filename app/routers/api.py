from fastapi import APIRouter, Request

from app.models import CHAPTERS, GEMS
from app.services.store import get_store
from app.services.telemetry import hud_payload

router = APIRouter(prefix="/api")


@router.get("/health")
async def health():
    return {"ok": True, "os": "JUDAS_OS", "freq": 432}


@router.get("/hud")
async def hud():
    return hud_payload()


@router.get("/chapters")
async def chapters():
    return [c.to_dict() for c in CHAPTERS]


@router.get("/gems")
async def gems():
    store = get_store()
    gems = []
    for gem in GEMS:
        data = gem.to_dict()
        data["active"] = store.gem_state.get(gem.id, False)
        gems.append(data)
    return gems


@router.post("/gems/{gem_id}/toggle")
async def toggle_gem(gem_id: str):
    store = get_store()
    store.gem_state[gem_id] = not store.gem_state.get(gem_id, False)
    store.persist()
    return {"id": gem_id, "active": store.gem_state[gem_id]}


@router.get("/works")
async def works(request: Request):
    store = get_store()
    user = getattr(request.state, "user", None)
    tenant_id = user.tenant_id if user else "ten_belentani"
    items = store.works_for(tenant_id) or list(store.works.values())
    return [w.to_dict() for w in items]
