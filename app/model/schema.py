from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MovieListItem(BaseModel):
    movie_id: str
    title: str
    title_en: str | None = None
    poster_path: str | None = None
    release_year: int | None = None
    rating: float | None = None
    genres: list[Any] | None = None
    director: str | None = None
    overview: str | None = None

    model_config = ConfigDict(from_attributes=True)


class MovieSearchResponse(BaseModel):
    items: list[MovieListItem] = Field(default_factory=list)
    page: int
    size: int
    total: int
    has_next: bool
