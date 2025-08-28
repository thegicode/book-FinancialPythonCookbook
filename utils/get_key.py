import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 가져오기
FRED_API_KEY = os.getenv("FRED_KEY")

