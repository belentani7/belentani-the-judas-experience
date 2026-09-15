from __future__ import annotations

import hashlib
import bcrypt
import json
from pathlib import Path
from threading import Lock
from typing import Any

from app.config import get_settings
from app.models import CANONICAL_TENANT, SEED_USER, WORKS, RELEASES
from app.models.entities import Release, Tenant, User, Work, uid


class Store:
    """JSON-backed tenancy stub. Replace with Postgres when the SaaS grows 1000x."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = Lock()
        self.tenants: dict[str, Tenant] = {}
        self.users: dict[str, User] = {}
        self.works: dict[str, Work] = {}
        self.releases: dict[str, Release] = {}
        self.gem_state: dict[str, bool] = {}
        self._load_or_seed()

    def _dump(self) -> dict[str, Any]:
        return {
            "tenants": [t.to_dict() for t in self.tenants.values()],
            "users": [
                {
                    **u.to_public(),
                    "password_hash": u.password_hash,
                }
                for u in self.users.values()
            ],
            "works": [w.to_dict() for w in self.works.values()],
            "releases": [r.to_dict() for r in self.releases.values()],
            "gem_state": self.gem_state,
        }

    def persist(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._dump(), indent=2), encoding="utf-8")

    def _load_or_seed(self) -> None:
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.tenants = {t["id"]: Tenant(**t) for t in raw.get("tenants", [])}
            self.users = {}
            for u in raw.get("users", []):
                self.users[u["id"]] = User(
                    id=u["id"],
                    tenant_id=u["tenant_id"],
                    email=u["email"],
                    password_hash=u["password_hash"],
                    display_name=u["display_name"],
                    role=u.get("role", "artist"),
                )
            self.works = {w["id"]: Work(**w) for w in raw.get("works", [])}
            self.releases = {r["id"]: Release(**r) for r in raw.get("releases", [])}
            self.gem_state = dict(raw.get("gem_state", {}))
            return
        self.tenants[CANONICAL_TENANT.id] = CANONICAL_TENANT
        self.users[SEED_USER.id] = SEED_USER
        for w in WORKS:
            self.works[w.id] = w
        for r in RELEASES:
            self.releases[r.id] = r
        self.persist()

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def authenticate(self, email: str, password: str) -> User | None:
        for user in self.users.values():
            if user.email.lower() == email.lower():
                try:
                    if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                        return user
                except (ValueError, AttributeError):
                    # Handle invalid password hashes
                    continue
        return None

    def register(self, email: str, password: str, display_name: str) -> User:
        tenant = Tenant(id=uid("ten"), slug=email.split("@")[0], name=f"{display_name} Studio")
        user = User(
            id=uid("usr"),
            tenant_id=tenant.id,
            email=email,
            password_hash=self.hash_password(password),
            display_name=display_name,
            role="tenant_admin",
        )
        with self._lock:
            self.tenants[tenant.id] = tenant
            self.users[user.id] = user
            self.persist()
        return user

    def works_for(self, tenant_id: str) -> list[Work]:
        return [w for w in self.works.values() if w.tenant_id == tenant_id]

    def releases_for(self, tenant_id: str) -> list[Release]:
        return [r for r in self.releases.values() if r.tenant_id == tenant_id]

    def add_work(self, tenant_id: str, title: str, synopsis: str, kind: str = "work") -> Work:
        work = Work(
            id=uid("wrk"),
            tenant_id=tenant_id,
            title=title,
            kind=kind,
            status="draft",
            synopsis=synopsis,
            frequency="432Hz",
            platform="studio",
            href="/studio",
        )
        with self._lock:
            self.works[work.id] = work
            self.persist()
        return work


_store: Store | None = None


def get_store() -> Store:
    global _store
    if _store is None:
        _store = Store(get_settings().data_dir / "omega.json")
    return _store
