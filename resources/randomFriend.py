from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
from mysql.connector import Error

from mysql_connection import get_connection

import math
import random

          
class RandomFriendResource(Resource):
    @jwt_required()
    def generate_random_coordinates(self, radius_km) :
        user_id = get_jwt_identity()
        print(user_id)
        # 24번 유저의 현재 위치를 사용하여 랜덤한 위도와 경도 생성
        connection = get_connection()
        query = '''SELECT u.id, r.lat, r.lng
                    FROM user u
                    JOIN region r
                        ON u.id = r.userId
                    WHERE u.id = %s;'''
        record = (user_id, )
        cursor = connection.cursor()
        cursor.execute(query, record)
        user_coordinates = cursor.fetchall()
        user_latitude = user_coordinates[0][1]
        user_longitude = user_coordinates[0][2]

        random_angle = 2 * math.pi * random.random()
        random_radius = radius_km * math.sqrt(random.random())
        print(random_angle)

        new_latitude = user_latitude + (random_radius / 111.32)
        new_longitude = user_longitude + (random_radius / (111.32 * math.cos(math.radians(user_latitude))))

        print(new_latitude, new_longitude)

        return new_latitude, new_longitude
            

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try:
            connection = get_connection()

            random_latitude, random_longitude = self.generate_random_coordinates(2.0)
            print(random_latitude, random_longitude)

            query = '''SELECT * FROM (
                        SELECT u.id, r.lat, r.lng, u.proImgUrl, u.nickname,
                            (6371 * acos(cos(radians(r.lat)) * cos(radians(%s))
                             * cos(radians(%s) - radians(r.lng)) +
                            sin(radians(r.lat)) * sin(radians(%s)))) AS distance
                        FROM user u
                        left JOIN region r
                        ON u.id = r.userId
                        WHERE u.id != %s
                        ORDER BY distance
                        ) AS subquery
                        WHERE distance < 5
                        LIMIT '''+offset+''', '''+limit+''';'''

            record = (random_latitude, random_longitude, random_latitude, user_id )
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            print(result_list)

            cursor.close()
            connection.close()

            result = {"result": "success", "conunt":len(result_list),"items":result_list }
            return result, 200

        except Exception as e:
            print(e)
            return {'result': 'fail', 'error': str(e)}, 500
