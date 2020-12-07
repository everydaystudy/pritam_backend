# 1. python 실행 환경
FROM python:3.7

# 2. 소스 복사
COPY . /app

# 3. python 모듈 설치 (실행 디렉토리 설정)
WORKDIR /app
RUN pip install -r requirements.txt

# 4. Flask 서버 실행
CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=8000"]
