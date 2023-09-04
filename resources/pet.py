
from aifc import Error
from datetime import datetime
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from config import Config

from mysql_connection import get_connection

import boto3



# 특정 유저 펫 정보
class UserPetInfoResource(Resource):

    def get(self,user_id):

        try :
            connection = get_connection()
            query = '''select *
                    from pets
                    where userId = %s;'''
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

        i = 0
        for row in result_list:
            
            result_list[i]['createdAt'] = row['createdAt'].isoformat()
            result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
            i = i + 1
        
        return {'result' : 'success',
                'items' : result_list}


# 펫 등록
class PetRegisterResource(Resource):

    @jwt_required()
    def post(self):

        user_id = get_jwt_identity()

        if 'petName' not in request.form or 'petAge' not in request.form or 'petGender' not in request.form:
            return {'result' : 'fail', 'error' : '필수항목 확인'},400
        
        petName = request.form['petName']
        petAge = request.form['petAge']
        petGender = request.form['petGender']
        petOneliner = request.form['petOneliner']

        if 'photo' in request.files :

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
                petProUrl = Config.S3_BASE_URL + new_filename
            else:
                petProUrl = None

            try:
                connection = get_connection()
                query = '''insert into pets
                        (userId,petName,petAge,petGender,petProUrl,oneliner)
                        values
                        (%s,%s,%s,%s,%s,%s);'''
                record = (user_id,petName,petAge,petGender,petProUrl,petOneliner)

                cursor = connection.cursor()
                cursor.execute(query, record)

                connection.commit()

                cursor.close()
                connection.close()

                return {'result':'success'}

            except Exception as e:
                print(e)
                return {'result':'fail','error':str(e)}, 400
            
        else:
            try:

                connection = get_connection()
                query = '''insert into pets
                        (userId,petName,petAge,petGender,oneliner)
                        values
                        (%s,%s,%s,%s);'''
                record = (user_id,petName,petAge,petGender,petOneliner)

                cursor = connection.cursor()
                cursor.execute(query, record)

                connection.commit()

                cursor.close()
                connection.close()

                return {'result':'success'}

            except Exception as e:
                print(e)
                return {'result':'fail','error':str(e)}, 400
            
# 펫 정보변경,삭제
class PetResource(Resource):

    # 펫 정보변경
    @jwt_required()
    def put(self):

        user_id = get_jwt_identity()

        if 'petName' not in request.form or 'petAge' not in request.form or 'petGender' not in request.form:
            return {'result' : 'fail', 'error' : '필수항목 확인'},400
        
        petName = request.form['petName']
        petAge = request.form['petAge']
        petGender = request.form['petGender']
        petOneliner = request.form['petOneliner']


        if 'photo' in request.files :

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
                petProUrl = Config.S3_BASE_URL + new_filename
            else:
                petProUrl = None

            try:
                connection = get_connection()
                query = '''update pets
                        set petName = %s, petAge = %s, petGender = %s, petProUrl = %s, oneliner = %s
                        where userId = %s;'''
                record = (petName,petAge,petGender,petProUrl,petOneliner,user_id)
                cursor = connection.cursor()
                cursor.execute(query,record)
                connection.commit()

                cursor.close()
                connection.close()

                return {'result':'success'}

            except Exception as e:
                print(e)
                return {'result':'fail','error':str(e)}, 400
            
        else:
            try:
                connection = get_connection()
                query = '''update pets
                        set petName = %s, petAge = %s, petGender = %s, oneliner = %s
                        where userId = %s;'''
                record = (petName,petAge,petGender,petOneliner,user_id)
                cursor = connection.cursor()
                cursor.execute(query,record)
                connection.commit()

                cursor.close()
                connection.close()

                return {'result':'success'}

            except Exception as e:
                print(e)
                return{'result':'fail','error':str(e)}, 400
            

    # 펫 삭제
    @jwt_required()
    def delete(self):
        
        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''delete from pets
                        where userId = %s;'''
            record = (user_id,)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()

        except Exception as e:
            print(e)
            return{'result':'fail','error':str(e)}, 400

        return {'result':'success'}

# 내 펫 정보
class MyPetInfoResource(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        try:
            connection = get_connection()
            query = '''select *
                        from pets
                        where userId = %s;'''
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

        i = 0
        for row in result_list:
            
            result_list[i]['createdAt'] = row['createdAt'].isoformat()
            result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
            i = i + 1
        
        return {'result' : 'success',
                'items' : result_list}