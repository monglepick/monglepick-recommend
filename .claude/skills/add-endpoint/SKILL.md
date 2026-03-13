---
name: add-endpoint
description: Recommend 서비스에 새로운 API 엔드포인트를 추가합니다. 3-Layer 아키텍처(API → Service → Repository)에 맞게 구현합니다.
argument-hint: "[엔드포인트명]"
allowed-tools: "Read, Edit, Write, Grep, Glob, Bash"
---

# API 엔드포인트 추가 스킬

`$ARGUMENTS` 이름의 새 API 엔드포인트를 3-Layer 패턴으로 추가합니다.

## 현재 엔드포인트 구조

```
/api/v1/search/
├── GET  /movies          ← 영화 검색
├── GET  /autocomplete    ← 자동완성
├── GET  /trending        ← 인기 검색어
├── GET  /recent          ← 최근 검색어 (인증)
├── DELETE /recent        ← 전체 삭제 (인증)
└── DELETE /recent/{kw}   ← 개별 삭제 (인증)

/api/v1/onboarding/
├── GET  /genres           ← 장르 목록 + 대표 포스터
├── POST /genres           ← 장르 선호 저장 (인증)
├── GET  /worldcup         ← 이상형 월드컵 대진표
├── POST /worldcup         ← 월드컵 결과 저장 (인증)
├── GET  /worldcup/result  ← 월드컵 결과 분석 (인증)
├── GET  /moods            ← 무드 목록
├── POST /moods            ← 무드 선호 저장 (인증)
└── GET  /status           ← 온보딩 완료 상태 (인증)
```

## Step 1: Repository (데이터 접근)

**파일**: `app/repository/{이름}_repository.py`

```python
"""
{이름} 리포지토리.

[데이터 접근 계층 설명]
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from app.model.entity import 관련엔티티


class {이름}Repository:
    """
    {이름} 데이터 접근 리포지토리.

    Args:
        session: SQLAlchemy 비동기 세션
    """

    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, id: int) -> 관련엔티티 | None:
        """ID로 조회"""
        result = await self._session.execute(
            select(관련엔티티).where(관련엔티티.id == id)
        )
        return result.scalar_one_or_none()

    async def save(self, entity: 관련엔티티) -> 관련엔티티:
        """저장"""
        self._session.add(entity)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity
```

## Step 2: Entity & Schema (필요 시)

**파일**: `app/model/entity.py`에 추가

```python
class NewEntity(Base):
    """새 엔티티"""
    __tablename__ = "new_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 필드 정의
    created_at = Column(DateTime, server_default=func.now())
```

**파일**: `app/model/schema.py`에 추가

```python
class NewRequest(BaseModel):
    """요청 스키마"""
    field: str = Field(..., description="필드 설명", min_length=1)

class NewResponse(BaseModel):
    """응답 스키마"""
    id: int
    field: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

## Step 3: Service (비즈니스 로직)

**파일**: `app/service/{이름}_service.py`

```python
"""
{이름} 서비스.

[비즈니스 로직 설명]
"""

import aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.repository.{이름}_repository import {이름}Repository


class {이름}Service:
    """
    {이름} 비즈니스 로직 서비스.

    Args:
        session: SQLAlchemy 비동기 세션
        redis_client: Redis 비동기 클라이언트
    """

    def __init__(self, session: AsyncSession, redis_client: aioredis.Redis):
        self._session = session
        self._redis = redis_client
        self._settings = get_settings()
        self._repo = {이름}Repository(session)

    async def execute(self, param: str) -> dict:
        """비즈니스 로직 실행"""
        # 구현
        pass
```

## Step 4: API 엔드포인트

**파일**: `app/api/{이름}.py` 또는 기존 파일에 추가

```python
"""
{이름} API 엔드포인트.

[API 설명]
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_redis, get_current_user, get_current_user_optional
from app.model.schema import NewRequest, NewResponse
from app.service.{이름}_service import {이름}Service

router = APIRouter(prefix="/api/v1/{경로}", tags=["{태그}"])


@router.get("", response_model=list[NewResponse])
async def get_list(
    page: int = Query(1, ge=1, description="페이지 번호"),
    size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    session: AsyncSession = Depends(get_db),
    redis = Depends(get_redis),
    user_id: int | None = Depends(get_current_user_optional),
):
    """
    목록을 조회한다.

    인증 없이 조회 가능하며, 로그인 시 개인화된 결과를 반환한다.
    """
    service = {이름}Service(session, redis)
    return await service.get_list(page=page, size=size, user_id=user_id)
```

## Step 5: 라우터 등록

**파일**: `app/api/router.py`

```python
from app.api.{이름} import router as {이름}_router
api_router.include_router({이름}_router)
```

## Step 6: 테스트 작성

**파일**: `tests/test_{이름}.py`

```python
"""
{이름} API 테스트.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_list_성공(client: AsyncClient):
    """목록 조회 성공"""
    response = await client.get("/api/v1/{경로}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_list_인증_필요(client: AsyncClient, auth_headers: dict):
    """인증 필요 엔드포인트"""
    response = await client.get("/api/v1/{경로}/protected", headers=auth_headers)
    assert response.status_code == 200
```

## Step 7: 실행 확인

```bash
cd /Users/yoonhyungjoo/Documents/monglepick/monglepick-recommend && pytest tests/ -v --tb=short 2>&1
```

## 핵심 규칙

1. **100% async** — 모든 함수는 `async def`
2. **Depends() 의존성 주입** — DB, Redis, 인증은 FastAPI Depends
3. **Pydantic 검증** — Request/Response 스키마 필수
4. **에러 처리** — Redis 다운 시 MySQL fallback
5. **타입 힌트** — Python 3.12+ 스타일 (`int | None`)
6. **JWT 호환** — Spring Boot 발급 JWT와 동일 시크릿
