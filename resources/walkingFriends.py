from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
from mysql_connection import get_connection



# 산책중인 친구
class WalkingFriendsResource(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        try:
            connection = get_connection()

            query = '''select u.nickname,u.proImgUrl
                    from follow f
                    join walkingFriends wf
                        on f.followeeId = wf.userId
                    join user u
                        on wf.userId = u.id
                    where f.followerId = %s;'''
            record = (user_id,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            print(result_list)

            cursor.close()
            connection.close()

        except Exception as e:
            print(e)
            return {'result':'fail','error':str(e)}, 400
        
        return {'result' : 'success',
                'count' : len(result_list),
                'items' : result_list}














