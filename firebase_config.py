# firebase_config.py

import firebase_admin
from firebase_admin import credentials, firestore

# 서비스 계정 키 경로
cred = credentials.Certificate("firebase-key.json")

# Firebase 앱 초기화
firebase_admin.initialize_app(cred)

# Firestore 클라이언트 가져오기
db = firestore.client()
