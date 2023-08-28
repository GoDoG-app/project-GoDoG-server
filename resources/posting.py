from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error
import requests
from config import Config

from mysql_connection import get_connection

import boto3

# 게시물 작성
class PostingListResource(Resource):

    @jwt_required()
    def post(self) :

        # 1. 클라이언트로부터 데이터를 받아온다.
        user_id = get_jwt_identity()

        # 카테고리,사진,내용은 필수
        if 'photo' not in request.files or 'content' not in request.form or 'category' not in request.form :
            return {'result' : 'fail', 'error' : '필수항목 확인'},400
        
        # 사진 받아온다.
        file = request.files['photo']
        # 내용 받아온다.
        content = request.form['content']
        # 카테고리 선택
        category = request.form['category']

        # 2. 사진부터 S3에 저장한다.
        current_time = datetime.now()

        # 문자열로 가공
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
        
        # 3. DB에 사진의 url 과 content 내용을 저장한다.
        try:
            connection = get_connection()
            query = '''insert into posting
                    (userId,postCategoryId,postContent,postImgUrl)
                    values
                    (%s,%s,%s,%s);'''
            record = ( user_id, category, content, Config.S3_BASE_URL+new_filename)
  

            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()

            return {'result':'success'}

        except Exception as e:
            print(e)
            return{'result':'fail','error':str(e)}, 400
        
# 게시물 수정,삭제
class PostingResource(Resource):

    # 게시물 수정
    @jwt_required()
    def put(self, posting_id):

        user_id = get_jwt_identity()

        print(request.files)

        # 카테고리,사진,내용은 필수
        if 'photo' not in request.files or 'content' not in request.form or 'category' not in request.form :
            return {'result' : 'fail', 'error' : '필수항목 확인'},400

        file = request.files['photo']
        content = request.form['content']
        category = request.form['category']


        # 2. 수정된 사진부터 S3에 저장한다.
        current_time = datetime.now()

        # 문자열로 가공
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
            return {'result': 'fail', 'error' : str(e)}
        
        # DB의 테이블을 업데이트 한다.
        # 새로운 파일 URL 과 내용을 업데이트 한다.

        try :
            connection = get_connection()
            query = '''update posting
                        set postContent = %s, postImgUrl = %s, postCategoryId = %s
                        where userId = %s and id = %s;'''
            record = (content,Config.S3_BASE_URL+new_filename, category, user_id, posting_id)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result' : 'fail', 'error' : str(e)},500
        
        # 데이터 가공한후 클라이언트에 응답
        return {'result':'success'}


    # 게시물 삭제
    @jwt_required()
    def delete(self, posting_id):
        
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            query = '''delete from posting
                        where userId = %s and id=%s'''
            record = (user_id,posting_id)
            cursor = connection.cursor()
            cursor.execute(query,record)
            connection.commit()

            cursor.close()
            connection.close()


        except Error as e:
            print(e)
            return {'result' : 'fail', 'error':str(e)},500
        
        return {'result':'success'}