from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error
from config import Config

from mysql_connection import get_connection

# 내 친구목록 가져오기
class FollowListResource(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()
        try:
            
            connection = get_connection()
            query = '''select f.id,f.followerId,f.followeeId, u.nickname,u.proImgUrl,u.oneliner
                        from follow f
                        join user u
                        on u.id = f.followeeId
                        where f.followerId = %s
                        order by u.nickname;'''
            record = (user_id,)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            print(result_list)

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result':'fail','error':str(e)},500

        # 알림때 필요할수도 있음
        # i = 0
        # for row in result_list:
        #     result_list[i]['createdAt'] = row['createdAt'].isoformat()
        #     i = i + 1
        
        return {'result' : 'success',
                'count' : len(result_list),
                'items' : result_list}


# 친구 맺기,끊기
class FollowResource(Resource):
    
    # 친구 맺기
    @jwt_required()
    def post(self, followee_id):

        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''insert into follow
                        (followerId, followeeId)
                        values
                        (%s,%s);'''
            record = (user_id, followee_id)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()
            cursor.close()
            connection.close()
        
        except Error as e:
            print(e)
            return {'result' : 'fail', 'error':str(e)},500

        return {'result' : 'success'}

    # 친구 끊기    
    @jwt_required()
    def delete(self, followee_id):

        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''delete from follow
                        where followerId =%s and followeeId = %s;'''
            record = (user_id, followee_id)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()
            cursor.close()
            connection.close()
        
        except Error as e:
            print(e)
            return {'result' : 'fail', 'error':str(e)},500

        return {'result' : 'success'}