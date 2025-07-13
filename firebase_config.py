import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# 환경변수에서 JSON 문자열 가져오기
firebase_key_json = os.environ.get("FIREBASE_KEY_JSON")

# JSON 문자열을 파싱해서 dict로 변환
firebase_key_dict = json.loads(firebase_key_json)

# dict를 credentials로 변환
cred = credentials.Certificate(firebase_key_dict)

# Firebase 초기화
firebase_admin.initialize_app(cred)

# Firestore 클라이언트
db = firestore.client()
