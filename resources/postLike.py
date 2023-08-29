from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
from mysql.connector import Error

from mysql_connection import get_connection

class PostingLikeResource(Resource):
    # 좋아요
    # JWT 토큰이 필요한 인증 데코레이터
    @jwt_required()    
    def post(self, posting_id):
        # 현재 로그인한 사용자의 ID를 가져옵니다.
        user_id = get_jwt_identity()
        
        # url : 로컬호스트/post/<int:post_id>/like
        
        try:
            # 데이터 베이스 연결
            connection = get_connection()
            query = """insert into postLikes
                        (postId, userId)
                    values
                        (%s, %s);"""
                        
            record = (posting_id, user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            
            connection.commit()
            
            cursor.close()
            connection.close()
        
        except Error as e :
            return {'result' : 'fail', 'error': str(e)}, 400
        return {'result' : 'success'}
    
    # 좋아요 취소
    @jwt_required()
    def delete(self, posting_id):
        
        user_id= get_jwt_identity()
        
        try :
            connection= get_connection()
            query= '''delete from postLikes
                    where postId= %s and userId = %s;'''
            record= (posting_id, user_id)
            cursor= connection.cursor()
            cursor.execute(query, record)
            
            connection.commit()
            
            cursor.close()
            connection.close()
            
        except Error as e:
            print(e)
            return {"result": "fail", "error": str(e)}
        
        return {"result" : "success"}