from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import ValidationError
import mongoengine.errors as error
from model.model import UserModel
from schema import UserSchema,updateUserSchema,ObjectIdField
from flask import request
from flask_jwt_extended import jwt_required,get_jwt

from bson import ObjectId
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token
blp=Blueprint("User","user")
@blp.route("/user")
class CreateUser(MethodView):
        
        def post(self):
            try:
                user_data=request.json
                user_data["password"]=pbkdf2_sha256.hash(user_data["password"])
                data=UserSchema.load(self=UserSchema(),data=user_data)
                user=UserModel(update_count=0,**data).save()
                return UserSchema.dump(self=UserSchema(),obj=user)
            
            except ValidationError as e:
                return {"status":404,"message":"error while validating userdata in mongodb"}
            except error.NotUniqueError as e:
                return {"status":404,"message":"user already exists"}
            except error.FieldDoesNotExist as e:
                 return {"status":404,"message":"required fields are empty"}
        def get(self):
             users=UserModel.objects.all()
             return UserSchema.dump(self=UserSchema(many=True),obj=users)
        
@blp.route("/user/login")
class Loginuser(MethodView):
    def post(self):
        user_data=request.json
        user=UserModel.objects.get(username=user_data["username"])
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token=create_access_token(identity=str(user.id))
            return {"access token":access_token}

# @blp.route("/user/logout")
# def logout_view():
#     return logout()
# class logout(MethodView):
#     @jwt_required
#     def post(self):
#         jti=get_jwt()["jti"]
#         print(jti)
#         ExpiredJwtSchema.load(self=ExpiredJwtSchema(),data=jti)
#         expired=Jwtmodel(jti).save()
#         return {"message":"blocklisted"}

@blp.route("/user/<string:user_id>")
class getUser(MethodView):
     def get(self,user_id):
          try: 
            user=UserModel.objects.get(id=user_id)
            return UserSchema.dump(self=UserSchema(),obj=user)
          except error.DoesNotExist as e:
               return{"status":404,"message":"User does not exist"}
     @jwt_required
     def delete(self,user_id):
          try:
            UserModel.objects.get(id=user_id).delete()
            return{"status":201,"message":"User deleted successfully"}
          except error.DoesNotExist as e:
              return{"status":404,"message":"User does not exist"}
          except ValidationError as e:
             return {"status":404,"message":"error while validating userdata in mongodb"}
     @jwt_required
     def put(self,user_id):
            try:
                user_data=request.json
                data=updateUserSchema.load(self=updateUserSchema(),data=user_data)
                updatecount=UserModel.objects.get(id=user_id).update_count
                print(updatecount)
                if updatecount>=2:
                    return{"status":404,"message":"you have updated profile too many times"}
                else:
                    updcount=UserModel.objects.get(id=user_id).update_count
                    updcount+=1
                    UserModel.objects.get(id=user_id).update(update_count=updcount,**data)
                    user=UserModel.objects.get(id=user_id)
                    return updateUserSchema.dump(self=updateUserSchema(),obj=user)
                    
            except ValidationError as e:
                return {"status":404,"message":"error while validating userdata in mongodb"}
            except error.NotUniqueError as e:
                return {"status":404,"message":"user already exists"}
            except error.FieldDoesNotExist as e:
                 return {"status":404,"message":"required fields are empty"}
            
              
              
     



          

