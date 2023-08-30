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


# 대댓글 수정,삭제
class CocommentsUDResource(Resource):

    @jwt_required()
    def put(self, posting_id, comment_id, cocomment_id):

        self.db = firestore.client()

        try:

            user_id = get_jwt_identity()
            data = request.get_json()

            if 'content' not in data or not data['content'].strip():
                return {'result': 'fail', 'error': '내용을 입력하세요'}, 400
            
            cocomment_ref = self.db.collection('post_comments').document(str(posting_id)).collection('comments').document(comment_id).collection('cocomment').document(cocomment_id)
            cocomment = cocomment_ref.get()
            
            if cocomment.exists:
                cocomment_author_id = cocomment.get('user_id')
                if cocomment_author_id == user_id:
                    cocomment_ref.update({'content': data['content']})
                    return {'result': 'success'}
                else:
                    return {'error': '대댓글을 수정할 권한이 없습니다.'}, 403
            else:
                return {'error': '대댓글을 찾을 수 없습니다.'}, 404


        except Exception as e:
            print(e)
            return{'result':'fail','error':str(e)}, 400
        
    # 대댓글 삭제
    @jwt_required()
    def delete(self, posting_id,comment_id, cocomment_id):

        self.db = firestore.client()

        try :
            user_id = get_jwt_identity()

            cocomment_ref = self.db.collection('post_comments').document(str(posting_id)).collection('comments').document(comment_id).collection('cocomment').document(cocomment_id)
            cocomment = cocomment_ref.get()

            if cocomment.exists:
                cocomment_author_id = cocomment.get('user_id')
                if cocomment_author_id == user_id:
                    cocomment_ref.delete()
                    return {'result': 'success'}
                else:
                    return {'error': '대댓글을 삭제할 권한이 없습니다.'}, 403
            else:
                return {'error': '대댓글을 찾을 수 없습니다.'}, 404


        except Exception as e:
            print(e)
            return{'result':'fail','error':str(e)}, 400



# 대댓글 작성
class CocomentsResource(Resource):

    @jwt_required()
    def post(self, posting_id, comment_id):

        self.db = firestore.client()

        try:

            user_id = get_jwt_identity()
            data = request.get_json()

            if 'content' not in data or not data['content'].strip():
                return {'result': 'fail', 'error': '내용을 입력하세요'}, 400
            
            # 대댓글 데이터 작성
            cocomment_data = {
                'user_id': user_id,
                'content': data['content'],
                'timestamp': firestore.SERVER_TIMESTAMP
            }

            # 대댓글 저장
            cocomment_ref = self.db.collection('post_comments').document(str(posting_id)).collection('comments').document(comment_id).collection('cocomment').add(cocomment_data)
            
            cocomment_doc_ref = cocomment_ref[1]
            cocomment_id = cocomment_doc_ref.id

            return {'result': 'success', 'cocomment_id': cocomment_id}

        except Exception as e:
            print(e)
            return {'result':'fail','error':str(e)}, 400







