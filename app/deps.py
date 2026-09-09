from __future__ import annotations

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth_service import current_user


def db_session(db: Session = Depends(get_db)) -> Session:
    return db


def optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    return current_user(request, db)


def require_user(request: Request, db: Session = Depends(get_db)) -> User:
    user = current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="AUTH_REQUIRED")
    return user
