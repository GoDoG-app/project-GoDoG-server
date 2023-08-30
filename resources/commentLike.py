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



# 댓글 좋아요,취소
class CommentLikeResource(Resource):

    @jwt_required()
    def post(self, posting_id,comment_id):

        self.db = firestore.client() 

        try:
            user_id = get_jwt_identity()

            like_ref = self.db.collection('comment_likes').document(comment_id).collection('likes').document(str(user_id))
            like_data = like_ref.get()
 
            if like_data.exists:  # 이미 좋아요를 누른 상태인 경우, 좋아요를 취소
                like_ref.delete()
                return {'message': 'Comment unliked successfully'}
            else:  # 좋아요를 누르지 않은 상태인 경우, 좋아요를 추가
                like_data = {   
                    'posting_id':str(posting_id),
                    'comment_id':str(comment_id),
                    'timestamp': firestore.SERVER_TIMESTAMP
                    }
                like_ref.set(like_data)
                return {'message': 'Comment liked successfully'}


        except Exception as e:
            print(e)
            return{'result':'fail','error':str(e)}, 400

















