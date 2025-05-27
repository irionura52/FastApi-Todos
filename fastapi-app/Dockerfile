# Python 3.9 베이스 이미지 사용
FROM python:3.9

# 비루트 사용자 생성 (보안을 위해)
RUN useradd -m myuser

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치 (루트 권한으로 설치)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

RUN chown myuser:myuser /app/todo.json && chmod 664 /app/todo.json

# 비루트 사용자로 실행
USER myuser

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
