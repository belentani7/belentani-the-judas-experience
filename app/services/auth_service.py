from __future__ import annotations

from sqlalchemy.orm import Session
from starlette.requests import Request

from app.models.user import User
from app.services import hash_password, verify_password


def register_user(db: Session, *, tenant_id: int, email: str, display_name: str, password: str) -> User:
    user = User(
        tenant_id=tenant_id,
        email=email.lower().strip(),
        display_name=display_name.strip(),
        password_hash=hash_password(password),
        role="artist",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email.lower().strip()).one_or_none()
    if user and verify_password(password, user.password_hash):
        return user
    return None


def current_user(request: Request, db: Session) -> User | None:
    uid = request.session.get("uid")
    if not uid:
        return None
    return db.query(User).filter(User.id == uid).one_or_none()
