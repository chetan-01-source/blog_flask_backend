from datetime import datetime
from marshmallow import Schema,fields,ValidationError
from bson import ObjectId


class ObjectIdField(fields.String):
    def _serialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, ObjectId):
            raise ValidationError("Invalid ObjectID")
        return str(value)

class PlainBlogSchema(Schema):
        id= ObjectIdField(dump_only=True)
        title=fields.String(required=True)
        content=fields.String(required=True)
        author=fields.String()
        likecount=fields.Integer(dump_only=True)

       
        
class BlogSchema(PlainBlogSchema):
        likedby=fields.List(fields.String()) 
        user_id=fields.String(dump_only=True)
        


class UserSchema(Schema):
        id= ObjectIdField(dump_only=True)
        username=fields.String(required=True,unique=True)
        email=fields.String(required=True,unique=True)
        password=fields.String(required=True)
        blogs=fields.Nested(BlogSchema,many=True)
        update_count=fields.Integer(dump_only=True)

class updateUserSchema(Schema):
        id= ObjectIdField(dump_only=True)
        username=fields.String(unique=True)
        email=fields.String(unique=True)
        password=fields.String()
        blogs=fields.Nested(BlogSchema,many=True)
        update_count=fields.Integer(dump_only=True)



class UpdateBlogSchema(Schema):
        id= ObjectIdField(dump_only=True)
        title=fields.String()
        content=fields.String()
        author=fields.String()
        likecount=fields.Integer(dump_only=True)
        likedby=fields.String(dump_only=True)
        user_id=fields.String(dump_only=True)
