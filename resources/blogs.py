from flask_smorest import Blueprint
from flask.views import MethodView
from marshmallow import ValidationError
import mongoengine.errors as error
from model.model import BlogModel,UserModel,PlainBlogModel
from schema import BlogSchema,UpdateBlogSchema,PlainBlogSchema
from flask import request,jsonify
from bson import ObjectId
from datetime import date
blp=Blueprint("Blogs","blogs")
from flask_jwt_extended import jwt_required

@blp.route("/blog/<string:userid>")

class Blogoperation(MethodView):
    
    @blp.response(200,PlainBlogSchema(many=True))   
    def get(self,userid):
           user=UserModel.objects.get(id=userid)
           return user.blogs

    @jwt_required()
    def post(self,userid):
     try:              
        Blog_data=request.json 
        user=UserModel.objects.get(id=userid)
        bloga=PlainBlogSchema.load(self=PlainBlogSchema(),data=Blog_data)
        blogappend=PlainBlogModel(**bloga)
        BlogSchema.load(self=BlogSchema(),data=Blog_data)
        blog=BlogModel(user_id=userid,**Blog_data).save()
        # blog=BlogModel.objects.get(content=Blog_data["content"])
        user.blogs.append(blogappend)
        user.save()     
        return BlogSchema.dump(self=BlogSchema(),obj=blog)
     except ValidationError as e:
                return {"status":404,"message":"error while validating Blogdata in mongodb"}
     except error.NotUniqueError as e:
                return {"status":404,"message":"Blog already exists"}
     except error.FieldDoesNotExist as e:
                 return {"status":404,"message":"required fields are empty"} 

@blp.route("/blog/<string:blogid>")
class SingleBlogOperation(MethodView):
       @jwt_required
       def delete(self,blogid):
              blog=BlogModel.objects.get(id=blogid)
              user=UserModel.objects.get(id=blog.user_id)
              for i in user.blogs:
                     if i.content==blog.content:
                            print(i)
                            user.blogs.remove(i)
                            user.save()
                            
              # user.blogs.remove(blog)
              blog.delete()
              blog.save()
              return{"status":200,"messsage":"blog deleted successfully"}
       @blp.response(200,BlogSchema)
       @jwt_required
       def get(self,blogid):
              blog=BlogModel.objects.get(id=blogid)
              return blog

@blp.route("/blog/<string:blog_id>/like")
class Likeblog(MethodView):
       @blp.response(200,BlogSchema)
       def post(self,blog_id):
              user_id= request.json.get("user_id")
              blog=BlogModel.objects.get(id=blog_id)
              if(len(blog.likedby)==0):
                            blog.likecount+=1
                            blog.likedby.append(user_id)
                            blog.save()
              else:
                     for i in blog.likedby:
                            if i==user_id:
                                   return jsonify({"message":"you already liked the post"})
                            else:
                                   blog.likecount+=1
                                   blog.likedby.append(user_id)
                                   blog.save()
              return blog
@blp.route("/blog/<string:blog_id>/unlike")
class Likeblog(MethodView):
       @blp.response(200,BlogSchema)
       def post(self,blog_id):
              user_id= request.json.get("user_id")
              blog=BlogModel.objects.get(id=blog_id)
              for i in blog.likedby:
                     if i==user_id:
                            blog.likedby.remove(i)
                            blog.likecount-=1
                            return blog
                     else:
                            return jsonify({"message":"post not found"})

