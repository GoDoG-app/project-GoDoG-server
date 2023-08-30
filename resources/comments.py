from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request


from firebase_admin import firestore


# 댓글 수정,삭제
class CommentsUDResource(Resource):

    # 수정
    @jwt_required()
    def put(self, posting_id, comment_id):

        self.db = firestore.client()
        
        try:
            user_id = get_jwt_identity()
            data = request.get_json()

            # 예외처리
            if 'content' not in data or not data['content'].strip():
                return{'result':'fail','error':'내용을 입력하세요'}, 400

            # 댓글 데이터 업데이트
            comment_data = {
                'user_id': user_id,
                'content': data.get('content'),
                'timestamp': firestore.SERVER_TIMESTAMP
            }

            # 댓글 업데이트 전에 작성자 확인
            comment_ref = self.db.collection('post_comments').document(str(posting_id)).collection('comments').document(comment_id)
            comment = comment_ref.get()
            if comment.exists: # 댓글 문서가 있으면 아래코드 실행
                comment_author_id = comment.get('user_id')
                if comment_author_id == user_id:
                    comment_ref.update(comment_data) # 댓글 업데이트
                    return {'result':'success'}
                else:
                    return {'error': '댓글을 수정할 권한이 없습니다.'}, 403
            else:
                return {'error': '댓글을 찾을 수 없습니다.'}, 404

        except Exception as e:
            return {'result':'fail','error': str(e)}, 400
        
        

# 댓글 작성
class CommentsResource(Resource):

    @jwt_required()
    def post(self, posting_id):

        self.db = firestore.client()
    

        try:
            user_id = get_jwt_identity()
            data = request.get_json()

            # 예외처리
            if 'content' not in data or not data['content'].strip():
                return{'result':'fail','error':'내용을 입력하세요'}, 400

            # 댓글 데이터 작성
            comment_data = {
                'user_id': user_id,
                'content': data['content'],
                'timestamp': firestore.SERVER_TIMESTAMP
            }

            # 댓글 저장
            comment_ref = self.db.collection('post_comments').document(str(posting_id)).collection('comments').add(comment_data)
            
            # comment_ref에서 문서 참조 가져오기
            comment_doc_ref = comment_ref[1]
            comment_id = comment_doc_ref.id

            return {'result':'success',
                    'comment_id': comment_id}

        except Exception as e:
            print(e)
            return {'result': 'fail', 'error': str(e)}, 400
