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

class PostingAllListResource(Resource) :
    
    @jwt_required()
    def get(self):
        
        user_id = get_jwt_identity()

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try:
            connection = get_connection()
            query = '''SELECT
                        p.userId as post_userid,
                        p.id AS post_id,
                        u.nickname AS user_nickname,
                        u.proImgUrl AS user_profile_image,
                        r.address AS user_region,
                        p.postContent,
                        p.postImgUrl,
                        if ( pl.id is null , 0, 1) as isLike,
                        pc.categoryName as category,
                        (SELECT COUNT(*) FROM postLikes pl WHERE pl.postId = p.id) AS post_likes_count,
                        p.createdAt,
                        p.updatedAt,
                        u.id
                    FROM
                        posting p
                    JOIN
                        user u ON p.userId = u.id
                    left JOIN
                        region r ON u.id = r.userId
                    left join postLikes pl
                        on pl.userId = %s and p.id = pl.postId
                    join postCategory pc
                        on p.postCategoryId = pc.id
                    order by p.createdAt desc
                    limit '''+offset+''','''+limit+''';'''
            record = (user_id,)

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()

            print(result_list)

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result':'fail','error':str(e)},500

        i = 0
        for row in result_list:
            result_list[i]['createdAt'] = row['createdAt'].isoformat()
            result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
            i = i + 1
        
        return {'result' : 'success',
                'count' : len(result_list),
                'items' : result_list}
    
# 카테고리별 게시물 가져오기
class PostingCategoryListResource(Resource):

    @jwt_required()
    def get(self, category_id):

        user_id = get_jwt_identity()
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try:
            
            connection = get_connection()
            query = '''SELECT
                        p.userId as post_userid,
                        p.id AS post_id,
                        u.nickname AS user_nickname,
                        u.proImgUrl AS user_profile_image,
                        r.address AS user_region,
                        p.postContent,
                        p.postImgUrl,
                        if ( pl.id is null , 0, 1) as isLike,
                        pc.categoryName as category,
                        (SELECT COUNT(*) FROM postLikes pl WHERE pl.postId = p.id) AS post_likes_count,
                        p.createdAt,
                        p.updatedAt,
                        u.id
                    FROM
                        posting p
                    JOIN
                        user u ON p.userId = u.id
                    left JOIN
                        region r ON u.id = r.userId
                    left join postLikes pl
                        on pl.userId = %s and p.id = pl.postId
                    join postCategory pc
                        on p.postCategoryId = pc.id
                    where pc.id = %s
                    order by p.createdAt desc
                    limit '''+offset+''','''+limit+''';'''
            record = (user_id,category_id)
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
                'count' : len(result_list),
                'items' : result_list}
    

# 특정 유저의 게시물 가져오기
class UserPostListResource(Resource):

    @jwt_required()
    def get(self,another_user_id):

        user_id = get_jwt_identity()
        
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try:
            connection = get_connection()
            query = '''SELECT
                        p.userId as post_userid,
                        p.id AS post_id,
                        u.nickname AS user_nickname,
                        u.proImgUrl AS user_profile_image,
                        r.address AS user_region,
                        p.postContent,
                        p.postImgUrl,
                        if ( pl.id is null , 0, 1) as isLike,
                        pc.categoryName as category,
                        (SELECT COUNT(*) FROM postLikes pl WHERE pl.postId = p.id) AS post_likes_count,
                        p.createdAt,
                        p.updatedAt,
                        u.id
                    FROM
                        posting p
                    JOIN
                        user u ON p.userId = u.id
                    left JOIN
                        region r ON u.id = r.userId
                    left join postLikes pl
                        on pl.userId = %s and p.id = pl.postId
                    join postCategory pc
                        on p.postCategoryId = pc.id
                    where u.id = %s
                    order by p.createdAt desc
                    limit '''+offset+''','''+limit+''';'''
            record = (user_id,another_user_id,)
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
                'count' : len(result_list),
                'items' : result_list}


# 내 게시물 가져오기
class MyPostListResource(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try:
            connection = get_connection()
            query = '''SELECT
                        p.userId as post_userid,
                        p.id AS post_id,
                        u.nickname AS user_nickname,
                        u.proImgUrl AS user_profile_image,
                        r.address AS user_region,
                        p.postContent,
                        p.postImgUrl,
                        if ( pl.id is null , 0, 1) as isLike,
                        pc.categoryName as category,
                        (SELECT COUNT(*) FROM postLikes pl WHERE pl.postId = p.id) AS post_likes_count,
                        p.createdAt,
                        p.updatedAt,
                        u.id
                    FROM
                        posting p
                    JOIN
                        user u ON p.userId = u.id
                    left JOIN
                        region r ON u.id = r.userId
                    left join postLikes pl
                        on pl.userId = %s and p.id = pl.postId
                    join postCategory pc
                        on p.postCategoryId = pc.id
                    where u.id = %s
                    order by p.createdAt desc
                    limit '''+offset+''','''+limit+''';'''
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
            result_list[i]['createdAt'] = row['createdAt'].isoformat()
            result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
            i = i + 1
        
        return {'result' : 'success',
                'count' : len(result_list),
                'items' : result_list}