from datetime import datetime
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
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required


import boto3



# 특정 유저 정보
class UserInfoResource(Resource):

    def get(self,user_id):

        try:
            connection = get_connection()
            query = '''select u.id,
                            u.email as userEmail,
                            u.nickname as userNickname,
                            u.gender as userGender,
                            u.birth as userBirth,
                            u.proImgUrl as userImgUrl,
                            u.oneliner as userOneliner,
                            u.loginType as userLoginType,
                            u.kakaoId as userKakaoId,
                            r.address as userAddress
                    from user u
                    join region r
                        on u.id = r.userId
                    where u.id = %s;'''
            record = (user_id,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result = cursor.fetchall()

            print(result)

            cursor.close()
            connection.close()


        except Exception as e:
            print(e)
            return{'result':'fail','error':str(e)}, 400
        
        i = 0
        for row in result:
            result[i]['userBirth'] = row['userBirth'].isoformat()
            i = i + 1
        
        return {'result' : 'success',
                'info':result}



# 내 정보, 수정
class MyProfileResource(Resource):

    # 내 정보
    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''select u.id,
                            u.email as userEmail,
                            u.nickname as userNickname,
                            u.gender as userGender,
                            u.birth as userBirth,
                            u.proImgUrl as userImgUrl,
                            u.oneliner as userOneliner,
                            u.loginType as userLoginType,
                            u.kakaoId as userKakaoId,
                            r.address as userAddress
                    from user u
                    join region r
                        on u.id = r.userId
                    where u.id = %s;'''
            record = (user_id,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result = cursor.fetchall()

            print(result)

            cursor.close()
            connection.close()


        except Exception as e:
            print(e)
            return{'result':'fail','error':str(e)}, 400
        
        i = 0
        for row in result:
            result[i]['userBirth'] = row['userBirth'].isoformat()
            i = i + 1
        
        return {'result' : 'success',
                'info':result}
    
    # 내 정보 수정
    @jwt_required()
    def put(self):

        user_id = get_jwt_identity()
        

        if 'nickname' not in request.form:
            return {'result' : 'fail', 'error' : '닉네임을 입력하세요.'},400
        
        nickname = request.form['nickname']

        if 'address' not in request.form:
            return {'resilt' : 'fail', 'error' : '주소를 입력하세요.'}, 400

        address = request.form['address']
        lat = request.form['lat']
        lng = request.form['lng']

        oneliner = request.form['oneliner']

        if 'photo' in request.files : # 사진이 있을 경우

            file = request.files['photo']
            

            if file :
            # 2. 사진부터 S3에 저장한다.
                current_time = datetime.now()

                # 문자열로 가공
                # if file:
                new_filename = current_time.isoformat().replace(':','_').replace('.','_') + '_' + str(user_id) + '.jpg'

                try:
                    s3 = boto3.client('s3',
                                    aws_access_key_id = Config.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key = Config.AWS_SECRET_ACCESS_KEY)
                    
                    s3.upload_fileobj(file,
                                    Config.S3_BUCKET,
                                    new_filename,
                                    ExtraArgs = {'ACL':'public-read',
                                                'ContentType':'image/jpeg'})
                except Exception as e:
                    print(e)
                    return {'result':'fail','error':str(e)}, 400
                userProUrl = Config.S3_BASE_URL + new_filename
            else:
                userProUrl = None

            try:
                connection = get_connection()
                query1 = '''update user
                            set nickname = %s,proImgUrl = %s,oneliner = %s
                            where id = %s;'''
                record1 = (nickname,userProUrl,oneliner,user_id)
                cursor = connection.cursor()
                cursor.execute(query1,record1)

                query2 = '''update region
                            set address = %s,lat = %s,lng = %s
                            where userId = %s;'''
                record2 = (address,lat,lng,user_id)
                cursor = connection.cursor()
                cursor.execute(query2,record2)

                connection.commit()

                cursor.close()
                connection.close()

                return {'result':'success'}

            except Exception as e:
                print(e)
                return {'result':'fail','error':str(e)}, 400
        
        # 사진이 없을 경우
        else: 
            try:
                connection = get_connection()
                query1 = '''update user
                            set nickname = %s,oneliner = %s
                            where id = %s;'''
                record1 = (nickname,oneliner,user_id)
                cursor = connection.cursor()
                cursor.execute(query1,record1)

                query2 = '''update region
                            set address = %s,lat = %s,lng = %s
                            where userId = %s;'''
                record2 = (address,lat,lng,user_id)
                cursor = connection.cursor()
                cursor.execute(query2,record2)

                connection.commit()

                cursor.close()
                connection.close()

                return {'result':'success'}
            
            except Exception as e:
                print(e)
                return{'result':'fail','error':str(e)}, 400





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
                (email, password, nickname, gender, birth, loginType)
                values
                (%s,%s,%s,%s,%s,%s);'''
        record1 = (data['email'], hashed_password, data['nickname'], data['gender'], data['birth'], data['loginType'])


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
    
class UserKakaoLoginResource(Resource):
    def post(self):
        
        data = request.get_json()
        
        check_list = ['kakaoId', 'email', 'nickname', 'loginType']
        for check in check_list:
            if check not in data:
                return {
                    'result' : 'fail',
                    'error' : '필수 항목을 확인하세요.'
                }, 400
        
        try:
            connection = get_connection()
            
            query = '''
                select *
                from user
                where loginType = 1
                    and kakaoId = %s
                    and email = %s
                    and nickname = %s;
            '''
            record = (data['kakaoId'], data['email'], data['nickname'])
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result = cursor.fetchone()
            
            if result == None:
                print(result)
                
                query = '''
                    insert into user
                    (email, nickname, loginType, kakaoId)
                    values
                    (%s, %s, 1, %s);
                '''
                record = (data['email'], data['nickname'], data['kakaoId'])
                cursor = connection.cursor()
                cursor.execute(query, record)
                
                result = {
                    'id' : cursor.lastrowid
                }         
                
                connection.commit()
                
            
            cursor.close()
            connection.close()
            
            print(result['id'])
        except Error as e:
            return {
                'result' : 'fail',
                'error' : str(e)
            }, 500
        
                    
        access_token = create_access_token(result['id'])
        
        return {
            'result' : 'success',
            'access_token' : access_token
        }