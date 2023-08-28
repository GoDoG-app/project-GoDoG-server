from flask import Flask, jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config
from resources.posting import PostingListResource, PostingResource
from resources.user import UserRegisterResource, UserLoginResource, UserLogoutResource, jwt_blocklist

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

api.add_resource( PostingListResource , "/posting") # 게시물 작성
api.add_resource( PostingResource , '/posting/<int:posting_id>') # 게시물 수정,삭제


if __name__ == '__main__':
    app.run()