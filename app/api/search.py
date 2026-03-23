from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.model.schema import MovieSearchResponse
from app.repository.movie_repository import MovieRepository
from app.service.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/movies", response_model=MovieSearchResponse)
async def search_movies(
    q: str | None = Query(default=None, description="영화 제목 검색어"),
    genre: str | None = Query(default=None, description="장르 필터"),
    page: int = Query(default=1, ge=1, description="페이지 번호"),
    size: int = Query(default=20, ge=1, le=100, description="페이지 크기"),
    db: AsyncSession = Depends(get_db),
) -> MovieSearchResponse:
    print(f"[search] request received q={q!r}, genre={genre!r}, page={page}, size={size}")
    repository = MovieRepository(db)
    service = SearchService(repository)
    return await service.search_movies(q=q, genre=genre, page=page, size=size)
