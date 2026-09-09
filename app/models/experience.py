from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ExperienceChapter(Base):
    __tablename__ = "experience_chapters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phase: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(200))
    kicker: Mapped[str] = mapped_column(String(120))
    body: Mapped[str] = mapped_column(Text)
    glyph: Mapped[str] = mapped_column(String(8), default="◉")
    order_index: Mapped[int] = mapped_column(Integer, default=0)
