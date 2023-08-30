from datetime import datetime

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request, jsonify
import mysql.connector
from mysql.connector import Error
import requests
from config import Config

from mysql_connection import get_connection

from firebase_admin import firestore




# 채팅방 목록 가져오기
class ChatRoomListResource(Resource):

    @jwt_required()
    def get(self):

        self.db = firestore.client()

        try :

            user_id = get_jwt_identity()

            # 해당 유저가 속한 채팅방 리스트 조회
            chat_rooms = []
            chat_ref = self.db.collection('chat_rooms')
            query = chat_ref.where('users', 'array_contains', user_id)
            for doc in query.stream():
                chat_rooms.append({
                    'room_id': doc.id,
                    'users': doc.get('users')
                })

            return {'result': 'success', 'chat_rooms': chat_rooms}

        except Exception as e:
            print(e)
            return {'result': 'fail', 'error': str(e)}, 400


# 채팅 보내기
class SendMessageResource(Resource):

    @jwt_required()
    def post(self):

        self.db = firestore.client()

        try:
            data = request.get_json()
            room_id = data['room_id']
            sender_id = get_jwt_identity()
            message = data['message']

            if 'message' not in data or not data['message'].strip():
                return {'result': 'fail', 'error': '내용을 입력하세요'}, 400

            # 채팅 메시지 저장
            chat_ref = self.db.collection('chat_rooms').document(room_id).collection('messages')
            chat_ref.add({
                'sender_id': sender_id,
                'message': message,
                'timestamp': firestore.SERVER_TIMESTAMP
            })

            return {'result': 'success', 'message': 'Message sent successfully'}

        except Exception as e:
            print(e)
            return {'result': 'fail', 'error': str(e)}, 400




# 채팅방 생성
class CreateChatRoomResource(Resource):

    @jwt_required()
    def post(self):

        self.db = firestore.client()

        try:
            data = request.get_json()
            sender_id = get_jwt_identity()
            receiver_id = data['user_id']
            # room_id = str(uuid.uuid4) # 유저 ID로 채팅방 ID 생성

            # # 이미 존재하는 방인지 확인하고, 없으면 생성
            # chat_ref = self.db.collection('chat_rooms').document(room_id)
            # if not chat_ref.get().exists:
            #     chat_ref.set({})  # 채팅방 생성

            # 파이어베이스에서 생성되는 고유 ID로 채팅방 생성
            chat_ref = self.db.collection('chat_rooms').document()
            chat_ref.set({})
            room_id = chat_ref.id

            # 채팅방에 유저 ID 추가
            chat_ref.update({
                'users': [sender_id, receiver_id]
            })

            return{'result':'success','room_id':room_id}


        except Exception as e:
            print(e)
            return {'result':'fail','error':str(e)}, 400



