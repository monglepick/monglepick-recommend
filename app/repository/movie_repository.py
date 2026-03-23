from __future__ import annotations

import json

from sqlalchemy import Select, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.entity import Movie


class MovieRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def _build_search_query(
        self,
        q: str | None,
        genre: str | None,
    ) -> Select[tuple[Movie]]:
        stmt = select(Movie)

        if q and q.strip():
            keyword = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    Movie.title.ilike(keyword),
                    Movie.title_en.ilike(keyword),
                )
            )

        if genre and genre.strip():
            genre_value = genre.strip()
            genre_json = json.dumps(genre_value, ensure_ascii=False)

            # movies.genres is assumed to be a JSON array like ["드라마", "스릴러"].
            # If the real JSON structure differs, this condition should be refined.
            stmt = stmt.where(
                or_(
                    func.JSON_CONTAINS(Movie.genres, genre_json) == 1,
                    func.JSON_SEARCH(Movie.genres, "one", genre_value).is_not(None),
                )
            )

        return stmt.order_by(
            func.coalesce(Movie.popularity_score, -1).desc(),
            func.coalesce(Movie.rating, -1).desc(),
        )

    async def search_movies(
        self,
        q: str | None,
        genre: str | None,
        page: int,
        size: int,
    ) -> tuple[list[Movie], int]:
        stmt = self._build_search_query(q=q, genre=genre)
        count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())

        total = await self.db.scalar(count_stmt)
        offset = (page - 1) * size

        result = await self.db.execute(stmt.offset(offset).limit(size))
        movies = result.scalars().all()

        return movies, total or 0
