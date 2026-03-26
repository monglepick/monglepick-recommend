"""
프로젝트 루트 실행용 엔트리포인트.

`uvicorn main:app --reload --port 8001`처럼 루트 모듈을 가리켜 실행해도
실제 추천 서비스 앱을 불러오도록 app.main:app 을 재노출합니다.
"""

import uvicorn

from app.main import app


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
