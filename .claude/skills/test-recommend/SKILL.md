---
name: test-recommend
description: Recommend 서비스의 pytest 테스트를 실행하고 결과를 분석합니다. 검색 API 11개 + 온보딩 API 9개 = 20개 테스트를 수행합니다.
argument-hint: "[all|search|onboarding|키워드]"
disable-model-invocation: true
allowed-tools: "Bash, Read, Grep"
---

# Recommend 서비스 테스트 스킬

## 환경

- **프로젝트 경로**: `/Users/yoonhyungjoo/Documents/monglepick/monglepick-recommend`
- **프레임워크**: pytest + pytest-asyncio
- **실행 조건**: MySQL, Redis 불필요 (SQLite in-memory + FakeRedis로 mock)
- **테스트 수**: 20개 (검색 11 + 온보딩 9)

## 사전 준비

테스트 의존성 설치 (최초 1회):
```bash
cd /Users/yoonhyungjoo/Documents/monglepick/monglepick-recommend && pip install pytest pytest-asyncio aiosqlite httpx fakeredis 2>&1
```

## 실행 모드

### 전체 테스트 (`all` 또는 인자 없음)
```bash
cd /Users/yoonhyungjoo/Documents/monglepick/monglepick-recommend && pytest tests/ -v --tb=short -q 2>&1
```

### 검색 테스트만 (`search`)
```bash
cd /Users/yoonhyungjoo/Documents/monglepick/monglepick-recommend && pytest tests/test_search.py -v --tb=short 2>&1
```

### 온보딩 테스트만 (`onboarding`)
```bash
cd /Users/yoonhyungjoo/Documents/monglepick/monglepick-recommend && pytest tests/test_onboarding.py -v --tb=short 2>&1
```

### 특정 키워드 (`-k` 필터)
```bash
cd /Users/yoonhyungjoo/Documents/monglepick/monglepick-recommend && pytest tests/ -v --tb=long -k "$ARGUMENTS" 2>&1
```

## 테스트 Fixture 참조

| Fixture | 용도 |
|---------|------|
| `async_session` | SQLite in-memory AsyncSession (자동 테이블 생성/삭제) |
| `fake_redis` | FakeRedis 인스턴스 (SortedSet, Hash, String) |
| `client` | FastAPI AsyncClient (의존성 오버라이드) |
| `auth_headers` | JWT 테스트 토큰 (user_id=1, email=test@monglepick.com) |

## 결과 분석

1. PASSED/FAILED 개수 요약
2. FAILED 시 에러 메시지에서 원인 분석
3. 관련 소스 코드를 읽고 수정 방안 제시
