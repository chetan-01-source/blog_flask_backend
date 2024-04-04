from datetime import datetime
from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import ValidationError
import mongoengine.errors as error
from model.model import BlogModel,UserModel
from schema import BlogSchema,UpdateBlogSchema
from flask import request
from bson import ObjectId


blp=Blueprint("Blogs","blogs")


@blp.route("/blog/<string:user_id>")

class Blogoperation(MethodView):
    def post(self,user_id):
     try:              
        Blog_data=request.json
        user=UserModel.objects.get(id=user_id)
       
        data=BlogSchema.load(self=BlogSchema(),data=Blog_data)
        blog=BlogModel(user_id=user_id,**data).save()
        return BlogSchema.dump(self=BlogSchema(),obj=blog)
     except ValidationError as e:
                return {"status":404,"message":"error while validating Blogdata in mongodb"}
     except error.NotUniqueError as e:
                return {"status":404,"message":"Blog already exists"}
     except error.FieldDoesNotExist as e:
                 return {"status":404,"message":"required fields are empty"} 