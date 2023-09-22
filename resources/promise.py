from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
from config import Config
from mysql_connection import get_connection


# 약속 수정,삭제
class PromiseResource(Resource):

   # 약속 수정
    @jwt_required()
    def put(self, promise_id):

        user_id = get_jwt_identity()

        data = request.get_json()

        try:
            connection = get_connection()

            # 약속 레코드를 가져옴
            promise_query = "SELECT userId FROM promise WHERE id = %s;"
            cursor = connection.cursor()
            cursor.execute(promise_query, (promise_id,))
            promise_record = cursor.fetchone()

            if promise_record is None:
                return {'result': 'fail', 'error': '약속이 존재하지 않습니다.'}, 404

            promise_creator_id = promise_record[0]

            cursor.close()

            # 장소, 날짜, 시간은 필수
            if 'meetingPlace' not in data or 'meetingDay' not in data or 'meetingTime' not in data:
                return {'result': 'fail', 'error': '필수항목 확인'}, 400

            # 로그인한 유저와 약속 소유자 비교
            if user_id != promise_creator_id:
                return {'result': 'fail', 'error': '권한 없음'}, 403  # 403 Forbidden

            meetingPlace = data['meetingPlace']
            meetingDay = data['meetingDay']
            meetingTime = data['meetingTime']

            query = '''update promise
                    set meetingPlace = %s, meetingDay = %s, meetingTime = %s
                    where id = %s and userId = %s;'''
            record = (meetingPlace, meetingDay, meetingTime, promise_id, user_id)

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

            return {'result': 'success'}

        except Exception as e:
            print(e)
            return {'result': 'fail', 'error': str(e)}, 400


    # 약속 삭제
    @jwt_required()
    def delete(self, promise_id):

        user_id = get_jwt_identity()

        try:
            connection = get_connection()

            # 약속 레코드를 가져옴
            promise_query = "SELECT userId FROM promise WHERE id = %s;"
            cursor = connection.cursor()
            cursor.execute(promise_query, (promise_id,))
            promise_record = cursor.fetchone()

            if promise_record is None:
                return {'result': 'fail', 'error': '약속이 존재하지 않습니다.'}, 404

            promise_creator_id = promise_record[0]

            cursor.close()

            # 로그인한 유저와 약속 소유자 비교
            if user_id != promise_creator_id:
                return {'result': 'fail', 'error': '권한 없음'}, 403  # 403 Forbidden

            # 약속 삭제
            delete_query = "DELETE FROM promise WHERE id = %s AND userId = %s;"
            cursor = connection.cursor()
            cursor.execute(delete_query, (promise_id, user_id))

            connection.commit()

            cursor.close()
            connection.close()

            return {'result': 'success'}

        except Exception as e:
            print(e)
            return {'result': 'fail', 'error': str(e)}, 400


# 내 전체 약속 목록
class PromiseListResource(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        try:
            
            connection = get_connection()
            query = '''select p.id,
                                p.userId,
                                u1.nickname as userNickanme,
                                p.friendId,
                                u2.nickname as friendNickname,
                                p.meetingPlace,
                                p.meetingDay,
                                p.meetingTime
                        from promise p
                        join user u1
                            on p.userId = u1.id
                        join user u2
                            on p.friendId = u2.id
                        where p.userId = %s or p.friendId = %s
                        order by p.meetingDay,p.meetingTime;'''
            record = (user_id,user_id,)

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



# 약속 생성할때 테이블에 2개가 저장되도록(쿼리문 2개)
# ex) 6번과 7번이 약속을 잡을 때 6번이 약속을 생성하면
#         테이블에 userId =6 , friendId = 7
#                 userId =7 , friendId = 6
# 그러면 내 약속 목록 조회할려면 where = 내 아이디 로 할 수 있음
# 수정 할 때에도 쿼리문 2개로 수정
# 삭제 할 때에도 쿼리문 2개로 삭제



# 약속 생성
class PromiseCreateResource(Resource):

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

        #  query1 = '''insert into user
        #         (email, password, nickname, gender, birth, loginType)
        #         values
        #         (%s,%s,%s,%s,%s,%s);'''
        # record1 = (data['email'], hashed_password, data['nickname'], data['gender'], data['birth'], data['loginType'])


        # cursor = connection.cursor()
        # cursor.execute(query1,record1)
        
        # user_id = cursor.lastrowid

        # query2= '''insert into region
        # (userId,address,lat,lng)
        # values
        # (%s,%s,%s,%s);'''
        # record2 = (user_id,data['address'],data['lat'],data['lng'])

        # cursor = connection.cursor()
        # cursor.execute(query2,record2)


        # connection.commit() # 데이터베이스에 적용하라.
        # #### DB에 데이터를 insert 한 후에,
        # #### 그 인서트된 행의 아이디를 가져오는 코드!!

        # cursor.close()
        # connection.close()
        

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