# python
FROM python:3.11.4

# /app 디렉토리 생성
RUN mkdir -p /app

# /app 디렉토리 WORKDIR 로 설정
WORKDIR /app

# 모든 파일 복사
COPY ./ ./

# 패키지 설치
RUN pip install --upgrade pip && pip install -r requirements.txt

# 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]