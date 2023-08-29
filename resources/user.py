import json
from flask_restful import Resource
from flask import jsonify, redirect, request
import mysql.connector
from mysql.connector import Error
import requests
from config import Config
from mysql_connection import get_connection
from email_validator import validate_email, EmailNotValidError
from utils import check_password, hash_password
from flask_jwt_extended import create_access_token, get_jwt, jwt_required


# 로그아웃

## 로그아웃된 토큰을 저장할 set 을 만든a다.
jwt_blocklist = set()

class UserLogoutResource(Resource) :

    @jwt_required()
    def delete(self):

        jti = get_jwt()['jti']
        print(jti)
        jwt_blocklist.add(jti)

        return {'result' : 'success'}

### 회원가입

class UserRegisterResource(Resource) :
    
    def post(self) :
        
        # {
        #     "email": "abc@naver.com",
        #     "password": "1234"
        # }
        
        # 1. 클라이언트가 보낸 데이터를 받아준다.

        data = request.get_json()

        # 2. 이메일 주소형식이 올바른지 확인한다.

        try :
            validate_email(data['email'])
        except EmailNotValidError as e :
            print(e)
            return {'result' : 'fail','error' : str(e)}, 400

        # 3. 비밀번호 길이가 유효한지 체크한다.
        #    만약, 비번이 6자리이상, 12자리 이하라고 한다면,

        if len(data['password']) < 6 or len(data['password']) > 12 :
            return {'result' : 'fail', 'error' : '비번 길이 에러'}, 400 # 보통 에러 코드는 숫자로 쓴다

        # 4. 비밀번호 암호화 한다.!!!!!중요!!!!!!!
        hashed_password = hash_password( data['password'] )

        print(str(hashed_password))

        # 5. DB에 이미 회원정보(이메일, 닉네임)가 있는지 확인한다.

        try:
            connection = get_connection()
            query = '''select *
                    from user
                    where email = %s;'''
            record = (data['email'],)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list =  cursor.fetchall()

            print(result_list)

            if len( result_list ) ==1 :
                return {'result' : 'fail', 'error' : '이미 회원가입 한 사람'}, 400
            

        except Error as e :
            print(e)
            return {'result' : 'fail', 'error' : str(e)}, 500
            
        try:
            connection= get_connection()
            query= '''select * from user
                        where nickname = %s;'''
            record= (data['nickname'],)
            
            cursor= connection.cursor(dictionary=True)
            cursor.execute(query, record)
            
            result_list= cursor.fetchall()
            print(result_list)
            
            if len(result_list)==1:
                return {'result':'fail', 'error':'이미 존재하는 닉네임'}, 400
            
        except Error as e :
            print(e)
            return {'result' : 'fail', 'error' : str(e)}, 500
            
            
        # 통과했으면 DB에 저장한다.

        query1 = '''insert into user
                (email, password, nickname, gender, birth)
                values
                (%s,%s,%s,%s,%s);'''
        record1 = (data['email'], hashed_password, data['nickname'], data['gender'], data['birth'])


        cursor = connection.cursor()
        cursor.execute(query1,record1)
        
        user_id = cursor.lastrowid

        query2= '''insert into region
        (userId,address,lat,lng)
        values
        (%s,%s,%s,%s);'''
        record2 = (user_id,data['address'],data['lat'],data['lng'])

        cursor = connection.cursor()
        cursor.execute(query2,record2)


        connection.commit() # 데이터베이스에 적용하라.
        #### DB에 데이터를 insert 한 후에,
        #### 그 인서트된 행의 아이디를 가져오는 코드!!

        cursor.close()
        connection.close()
        

        # create_access_token(user_id, expires_delta=datetime.timedelta(days=10))
        access_token = create_access_token(user_id)

        
        return {'result' : 'success', 'access_token': access_token} # 200은 생략

### 로그인 관련 개발

class UserLoginResource(Resource) :
    def post(self) :

        # 1. 클라이언트로부터 데이터 받아온다.
        data = request.get_json()

        # 2. 이메일 주소로, DB에 select 한다.
        try :
            connection = get_connection()
            query = '''select *
                    from user
                    where email = %s;'''
            record = (data['email'],)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()


        except Error as e :
            return {'result': 'fail', 'error' : str(e)}, 500
        print("받아온 데이터 체크 시작")
        print(result_list)
        print("받아온 데이터 체크 끝")

        if len(result_list) == 0 :
            return {'result' : 'fail', 'error' : '회원가입한 사람 아님'}, 400
        
        # 3. 비밀번호가 일치하는지 확인한다.
        #    암호화된 비밀번호가 일치하는지 확인해야 함.

        check = check_password(data['password'], result_list[0]['password'] )

        if check == False :
            return {'result' : 'fail', 'error': '비번 틀렸음'}, 400


        # 4. 클라이언트에게 데이터를 보내준다.
        access_token = create_access_token(result_list[0]['id'])
        user_name = result_list[0]['nickname']

        return {'result' : 'success', 'access_token':access_token}
    
# class UserKakaoLoginResource(Resource):
#     def post(self):
#         try:
#             data = request.get_json()

#             if data is not None:
#                 kakao_token = data.get('kakaoToken')  # 클라이언트에서 'kakaoToken'으로 전송

#                 # 받아온 토큰을 사용하거나 처리할 작업을 수행
#                 # 이 부분에서 토큰을 확인하고 필요한 작업을 수행합니다.

#                 # 예: 받아온 토큰을 그대로 응답
#                 response_data = {'message': 'Kakao Token received successfully', 'kakaoToken': kakao_token}  # 서버에서 'kakaoToken'으로 응답

#                 return response_data, 200
#             else:
#                 return {'message': 'Error', 'error': 'No data received'}, 400  # 클라이언트로부터 데이터가 없을 때 에러 응답

#         except Exception as e:
#             return {'message': 'Error', 'error': str(e)}, 500

class UserKakaoLoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()

            if data is not None:
                kakao_token = data.get('kakaoToken')  # 클라이언트에서 'kakaoToken'으로 전송

                # Kakao API 호출
                kakao_api_url = "https://kapi.kakao.com/v2/user/me"
                headers = {"Authorization": f"Bearer {kakao_token}"}
                response = requests.get(kakao_api_url, headers=headers)

                if response.status_code == 200:
                    # Kakao API 호출 성공
                    kakao_response_data = response.json()
                    # 이제 kakao_response_data를 처리하거나 반환할 데이터에 추가할 수 있습니다.
                    
                    # 예: 받아온 토큰과 Kakao API 응답을 함께 응답
                    response_data = {
                        'message': 'Kakao Token received successfully',
                        'kakaoToken': kakao_token,
                        'kakaoUserData': kakao_response_data
                    }
                    return response_data, 200
                else:
                    # Kakao API 호출 실패
                    return {'message': 'Error', 'error': 'Failed to fetch Kakao user data'}, 500
            else:
                return {'message': 'Error', 'error': 'No data received'}, 400  # 클라이언트로부터 데이터가 없을 때 에러 응답

        except Exception as e:
            return {'message': 'Error', 'error': str(e)}, 500