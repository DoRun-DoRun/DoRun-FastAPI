# Start

uvicorn main:app --reload

## DB 자동 생성

alembic revision --autogenerate

## migrations에 생성된 리비전 파일로 DB 변경

alembic upgrade head

## 서버 재설정

sudo systemctl restart myapi.service

## 가상환경 진입

cd /Users/pahkey/myapi/bin
source activate
cd /Users/hin6150/Desktop/Project/DoRun-DoRun
