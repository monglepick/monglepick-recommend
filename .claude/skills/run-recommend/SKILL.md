---
name: run-recommend
description: Recommend 서비스를 로컬에서 실행하거나 헬스체크합니다.
argument-hint: "[run|health|deps]"
disable-model-invocation: true
allowed-tools: "Bash, Read"
---

# Recommend 서비스 실행 스킬

## 실행 모드

### 개발 서버 실행 (`run` 또는 인자 없음)
```bash
cd /Users/yoonhyungjoo/Documents/monglepick/monglepick-recommend && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload 2>&1
```
- MySQL + Redis가 실행 중이어야 합니다
- 핫 리로드: 코드 변경 시 자동 재시작

### 헬스체크 (`health`)
```bash
curl -sf http://localhost:8001/health | python3 -m json.tool 2>/dev/null || echo "서비스 미실행"
```

### 의존성 설치 (`deps`)
```bash
cd /Users/yoonhyungjoo/Documents/monglepick/monglepick-recommend && pip install -r requirements.txt 2>&1
```

## 사전 조건

| 서비스 | 필수 | 확인 명령 |
|--------|------|----------|
| MySQL | ✅ | `docker exec staging-mysql mysqladmin ping -u monglepick -pmonglepick` |
| Redis | ✅ | `docker exec staging-redis redis-cli ping` |
| .env | ✅ | `ls .env` (없으면 `cp .env.example .env`) |

## 환경변수 참조

| 변수 | 기본값 | 설명 |
|------|--------|------|
| DB_HOST | localhost | MySQL 호스트 |
| DB_PORT | 3306 | MySQL 포트 |
| DB_NAME | monglepick | DB명 |
| REDIS_HOST | localhost | Redis 호스트 |
| REDIS_DB | 1 | Redis DB (agent=0과 분리) |
| JWT_SECRET | - | Spring Boot와 동일 시크릿 |
| SERVER_PORT | 8001 | 서비스 포트 |

## API 문서

서비스 실행 후 Swagger UI:
- `http://localhost:8001/docs` (Swagger)
- `http://localhost:8001/redoc` (ReDoc)
