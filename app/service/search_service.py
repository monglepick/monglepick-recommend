from app.model.schema import MovieListItem, MovieSearchResponse
from app.repository.movie_repository import MovieRepository


class SearchService:
    def __init__(self, repository: MovieRepository) -> None:
        self.repository = repository

    async def search_movies(
        self,
        q: str | None,
        genre: str | None,
        page: int,
        size: int,
    ) -> MovieSearchResponse:
        movies, total = await self.repository.search_movies(
            q=q,
            genre=genre,
            page=page,
            size=size,
        )
        print(
            f"[search_service] fetched {len(movies)} movies "
            f"(total={total}, page={page}, size={size})"
        )

        items = [MovieListItem.model_validate(movie) for movie in movies]

        return MovieSearchResponse(
            items=items,
            page=page,
            size=size,
            total=total,
            has_next=(page * size) < total,
        )
