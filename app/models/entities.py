from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


Role = Literal["visitor", "artist", "tenant_admin"]


@dataclass
class Tenant:
    id: str
    slug: str
    name: str
    plan: str = "omega"
    created_at: str = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class User:
    id: str
    tenant_id: str
    email: str
    password_hash: str
    display_name: str
    role: Role = "artist"
    created_at: str = field(default_factory=utcnow)

    def to_public(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "email": self.email,
            "display_name": self.display_name,
            "role": self.role,
        }


@dataclass
class Work:
    id: str
    tenant_id: str
    title: str
    kind: str
    status: str
    synopsis: str
    frequency: str
    platform: str
    href: str
    created_at: str = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Release:
    id: str
    tenant_id: str
    title: str
    year: int
    catalog: str
    tracks: list[str]
    created_at: str = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ExperienceChapter:
    id: str
    index: int
    code: str
    title: str
    body: str
    prompt: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Gem:
    id: str
    code: str
    name: str
    archetype: str
    glyph: str
    active: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
