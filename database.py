# import boto3
# from botocore.exceptions import NoCredentialsError
# from fastapi import File, UploadFile
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from starlette.config import Config

# config = Config('.env')
# SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# # S3 설정
# ACCESS_KEY = config('S3_ACCESS_KEY')
# SECRET_KEY = config('S3_SECRET_KEY')
# BUCKET_NAME = 'do-run'

# s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
#                   aws_secret_access_key=SECRET_KEY)


# async def upload_file(file_name: str, file: UploadFile = File(...)):
#     try:
#         s3.upload_fileobj(file.file, BUCKET_NAME, file_name)
#         file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
#         return file_url
#     except NoCredentialsError:
#         return "Credentials not available"


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app/db.py
from pathlib import Path
import shutil
from fastapi import UploadFile, File
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

# ────────────────────────────────
# 1) 환경 변수
# ────────────────────────────────
config = Config('.env')

#   postgresql+psycopg2://<USER>:<PASSWORD>@<HOST>:<PORT>/<DBNAME>
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')


# 로컬 저장 경로 (예: ./uploads)
UPLOAD_DIR: Path = Path(
    config('UPLOAD_DIR', default='uploads')
).resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ────────────────────────────────
# 2) SQLAlchemy 세팅 (PostgreSQL)
# ────────────────────────────────
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 연결 검사
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base = declarative_base()

# ────────────────────────────────
# 3) 파일 업로드 헬퍼
# ────────────────────────────────
async def upload_file(
    file_name: str,
    file: UploadFile = File(...),
) -> str:
    """
    업로드된 파일을 UPLOAD_DIR에 저장하고
    파일의 로컬 경로(URL 아님)를 반환합니다.
    """
    destination = UPLOAD_DIR / file_name
    with destination.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    # FastAPI 경로를 생성하거나 그대로 경로 문자열 반환
    return str(destination)  # 예: '/abs/path/uploads/myimage.png'

# ────────────────────────────────
# 4) DB 세션 종속성
# ────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()