from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
from config import Config
from mysql_connection import get_connection

# 약속 api
class PromiseResource(Resource):

    # 약송 생성
    @jwt_required()
    def post(self,friend_id):

        user_id = get_jwt_identity()
                
        data = request.get_json() 

        try:
            
            connection = get_connection()

            # 카테고리,사진,내용은 필수
            # if 'photo' not in request.files or 'content' not in request.form or 'category' not in request.form :
            #     return {'result' : 'fail', 'error' : '필수항목 확인'},400
            
            # 장소,날짜,시간은 필수
            if 'meetingPlace' not in data or 'meetingDay' not in data or 'meetingTime' not in data:
                return {'result' : 'fail', 'error': '필수항목 확인'}, 400
            
            meetingPlace = data['meetingPlace']
            meetingDay = data['meetingDay']
            meetingTime = data['meetingTime']

            query = '''insert into promise
                    (userId, friendId, meetingPlace, meetingDay,meetingTime)
                    values
                    (%s, %s, %s, %s, %s);'''
            record = (user_id,friend_id,meetingPlace,meetingDay,meetingTime)

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

            return {'result':'success'}

        except Exception as e:
            print(e)
            return {'result':'fail','error':str(e)}, 400


    # 약속 목록
    @jwt_required()
    def get(self,friend_id):

        user_id = get_jwt_identity()

        try:

            connection = get_connection()

            query = '''select userId,friendId,meetingPlace,meetingDay,meetingTime
                    from promise        
                    where userid = %s and friendId = %s;'''
            record = (user_id,friend_id)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            print(result_list)

            cursor.close()
            connection.close()


        except Exception as e:
            print(e)
            return {'result':'fail','error':str(e)}, 400
        
        i = 0
        for row in result_list:
            result_list[i]['meetingDay'] = row['meetingDay'].isoformat()
            result_list[i]['meetingTime'] = str(row['meetingTime'])
            i = i + 1
        
        return {'result' : 'success',
                'count' : len(result_list),
                'items' : result_list}