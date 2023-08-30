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


            # 이미 존재하는 방인지 확인
            existing_room = self.find_existing_room(sender_id, receiver_id)

            if existing_room:
                return {'result': 'success', 'room_id': existing_room}

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
        
    def find_existing_room(self, sender_id, receiver_id):
        chat_rooms_ref = self.db.collection('chat_rooms')

        # Sender의 채팅방 목록 쿼리
        query_sender = chat_rooms_ref.where('users', 'array_contains', sender_id)
        chat_rooms_sender = query_sender.stream()

        # Receiver의 채팅방 목록 쿼리
        query_receiver = chat_rooms_ref.where('users', 'array_contains', receiver_id)
        chat_rooms_receiver = query_receiver.stream()

        # 이미 존재하는 방을 찾기 위해 두 개의 쿼리 결과를 비교
        for chat_room in chat_rooms_sender:
            room_id = chat_room.id
            # Sender의 채팅방이 Receiver의 채팅방 목록에도 있는지 확인
            if room_id in [room.id for room in chat_rooms_receiver]:
                return room_id  # 이미 존재하는 방의 ID 반환

        return None  # 이미 존재하는 방이 없으면 None 반환



