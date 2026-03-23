from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import BigInteger, DateTime, Float, Integer, String, Text, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Movie(Base):
    __tablename__ = "movies"

    movie_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    title_en: Mapped[str | None] = mapped_column(String(500), nullable=True)
    poster_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    backdrop_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    release_year: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    runtime: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True, index=True)
    vote_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    popularity_score: Mapped[float | None] = mapped_column(Float, nullable=True, index=True)
    genres: Mapped[list[Any] | None] = mapped_column(JSON, nullable=True)
    director: Mapped[str | None] = mapped_column(String(200), nullable=True)
    cast: Mapped[list[Any] | None] = mapped_column(JSON, nullable=True)
    certification: Mapped[str | None] = mapped_column(String(50), nullable=True)
    trailer_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)
    tagline: Mapped[str | None] = mapped_column(String(500), nullable=True)
    imdb_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    original_language: Mapped[str | None] = mapped_column(String(10), nullable=True)
    collection_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    kobis_movie_cd: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sales_acc: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    audience_count: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    screen_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kobis_watch_grade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    kobis_open_dt: Mapped[str | None] = mapped_column(String(10), nullable=True)
    kmdb_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    awards: Mapped[str | None] = mapped_column(Text, nullable=True)
    filming_location: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        server_default=func.now(),
        onupdate=func.now(),
    )
