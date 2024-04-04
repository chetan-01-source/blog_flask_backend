from flask import Flask,jsonify
from flask_mongoengine import MongoEngine
from resources.user import blp as UserBlueprint
from resources.blogs import blp as BlogBlueprint
from flask_smorest import Api
from flask_jwt_extended import JWTManager
app=Flask(__name__)
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config[
    "OPENAPI_SWAGGER_UI_URL"
] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
db = MongoEngine()
app.config['MONGODB_SETTINGS'] = {
    'db': 'user',
    'host': 'mongodb://localhost/user'
}
db.init_app(app)
api=Api(app)
app.config["SECRET_KEY"]="chetan"
jwt=JWTManager(app)

# @jwt.token_in_blocklist_loader
# def check_if_token_in_blocklist(jwt_header, jwt_data):
#      jti= jwt_data["jti"]

#      expirejwt= Jwtmodel.objects.get(expired_jti=jti)
#      if(expirejwt):
#          return True
#      else:
#          return False


# @jwt.revoked_token_loader
# def revoked_token_callback(jwt_header, jwt_payload):
#     return (
#         jsonify(
#             {"description": "The token has been revoked.", "error": "token_revoked"}
#         ),
#         401,
#     )
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

api.register_blueprint(BlogBlueprint)
api.register_blueprint(UserBlueprint)