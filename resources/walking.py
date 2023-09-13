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