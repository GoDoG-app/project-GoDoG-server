from flask import Flask, jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.follow import FollowListResource, FollowResource
from resources.pet import MyPetListResource, PetRegisterResource, PetResource
from resources.postLike import PostingLikeResource
from resources.posting import MyPostListResource, PostingAllListResource, PostingCategoryListResource, PostingListResource, PostingResource, UserPostListResource
from resources.user import UserKakaoLoginResource, UserRegisterResource, UserLoginResource, UserLogoutResource, jwt_blocklist

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

api = Api(app)

api.add_resource( UserRegisterResource , '/user/register') 
api.add_resource( UserLoginResource , '/user/login' )
api.add_resource( UserLogoutResource , '/user/logout')
api.add_resource( UserKakaoLoginResource, '/user/KakaoToken') # 카카오 토큰 발급

api.add_resource( PetRegisterResource, '/pet/register') # 펫 등록
api.add_resource( PetResource , "/pet/<int:pets_id>" ) # 펫 정보변경,삭제
api.add_resource( MyPetListResource , "/pet/mylist") # 내가 등록한 펫

api.add_resource( PostingListResource , "/posting") # 게시물 작성
api.add_resource( PostingResource , '/posting/<int:posting_id>') # 게시물 수정,삭제
api.add_resource( PostingAllListResource , "/posting/list") # 전체 게시물 가져오기
api.add_resource( PostingCategoryListResource, "/posting/category/<int:category_id>") # 카테고리별 게시물 가져오기
api.add_resource( MyPostListResource , "/posting/mylist") # 내 게시물 가져오기
api.add_resource( UserPostListResource , "/posting/<int:another_user_id>/list") # 특정유저 게시물 가져오기

api.add_resource( PostingLikeResource ,"/post/<int:posting_id>/like") # 게시물 좋아요,취소

api.add_resource( FollowListResource , "/followlist") # 내 친구목록 가져오기
api.add_resource( FollowResource , '/follow/<int:followee_id>') # 친구맺기,끊기



if __name__ == '__main__':
    app.run()