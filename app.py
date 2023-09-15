from flask import Flask, jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.follow import FollowListResource, FollowResource
from resources.pet import MyPetInfoResource, PetRegisterResource, PetResource, UserPetInfoResource
from resources.postLike import PostingLikeResource
from resources.posting import MyPostListResource, PostingAllListResource, PostingCategoryListResource, PostingListResource, PostingResource, UserPostListResource
from resources.promise import PromiseResource
from resources.randomFriend import RandomFriendResource
from resources.tmap import TMapRouteResource
from resources.user import UserInfoResource, UserKakaoLoginResource, MyProfileResource, UserRegisterResource, UserLoginResource, UserLogoutResource, UserSearchResource, jwt_blocklist
from resources.walking import walkingListResource, getWalkingListResource

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
api.add_resource( UserKakaoLoginResource , '/user/kakaologin')

api.add_resource( MyProfileResource ,"/user/profile") # 내 정보, 수정

api.add_resource( PetRegisterResource, '/pet/register') # 펫 등록
api.add_resource( PetResource , "/pet/edit" ) # 펫 정보변경,삭제
api.add_resource( MyPetInfoResource , "/pet/info") # 내가 등록한 펫

api.add_resource( UserInfoResource ,"/user/<int:user_id>") # 특정 유저 정보
api.add_resource( UserPetInfoResource ,"/userpet/<int:user_id>") # 특정 유저 펫 정보


api.add_resource( PostingListResource , "/posting") # 게시물 작성
api.add_resource( PostingResource , '/posting/<int:posting_id>') # 게시물 수정,삭제
api.add_resource( PostingAllListResource , "/posting/list") # 전체 게시물 가져오기
api.add_resource( PostingCategoryListResource, "/posting/category/<int:category_id>") # 카테고리별 게시물 가져오기
api.add_resource( MyPostListResource , "/posting/mylist") # 내 게시물 가져오기
api.add_resource( UserPostListResource , "/posting/<int:another_user_id>/list") # 특정유저 게시물 가져오기

api.add_resource( PostingLikeResource ,"/post/<int:posting_id>/like") # 게시물 좋아요,취소

api.add_resource( FollowListResource , "/followlist") # 내 친구목록 가져오기
api.add_resource( FollowResource , '/follow/<int:followee_id>') # 친구맺기,끊기

api.add_resource( RandomFriendResource, "/randomfriend/list") # 랜덤친구 추천

api.add_resource( TMapRouteResource, "/route") # tmap 보행자경로 api

api.add_resource( UserSearchResource , "/search") # 유저 검색

api.add_resource( walkingListResource , "/walkinglist") # 산책기록

api.add_resource( getWalkingListResource, "/walkinglist/my") # 내 산책기록 api

api.add_resource( PromiseResource ,"/promise/<int:friend_id>") # 약속 api

if __name__ == '__main__':
    app.run()