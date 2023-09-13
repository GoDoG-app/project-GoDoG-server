from datetime import timedelta
import json
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import jsonify, request
from mysql.connector import Error
from flask_restful import Resource

from mysql_connection import get_connection

class walkingListResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        try : 
            connection= get_connection()
            if data['time'] is not None and data['distance'] is not None:
                query= '''
                    INSERT INTO walkingList
                    (userId, distance, time)
                    values
                    (%s, %s, %s)'''
            record = (user_id, data['distance'], data['time'])
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

            
        except Exception as e:
            print(e)
            return{'result':'fail','error':str(e)}, 400
        
        return {'result':'success'}

class getWalkingListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''SELECT userId, petsId, distance, time, createdAt
                    FROM walkingList
                    WHERE userId = %s;'''
            record = (user_id,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Exception as e:
            print(e)
            return {'result': 'fail', 'error': str(e)}, 400

        # timedelta 객체를 직렬화할 필요 없이, 더 간단하게 데이터를 가공합니다.
        for row in result_list:
            row['createdAt'] = row['createdAt'].isoformat()

            
        return jsonify({'result': 'success', 'count': len(result_list), 'items': result_list})