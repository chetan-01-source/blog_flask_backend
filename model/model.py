from datetime import datetime
from mongoengine import StringField,EmailField,Document,IntField,DateField,EmbeddedDocument,EmbeddedDocumentField,ListField,ReferenceField
from wtforms import DateTimeField




class PlainBlogModel(EmbeddedDocument):
    title=StringField(required=True)
    content=StringField(required=True,unique=True)
    author=StringField(default="unknown")
    Date= DateField()

    

class UserModel(Document):
    username=StringField(required=True,unique=True)
    email=EmailField(required=True,unique=True)
    password= StringField(required=True)
    blogs = ListField(EmbeddedDocumentField(PlainBlogModel))
    update_count= IntField(default=0)



class BlogModel(Document):
    title=StringField(required=True)
    content=StringField(required=True,unique=True)
    author=StringField(default="unknown")
    likecount=IntField(default=0)
    likedby=ListField(StringField())
    user_id =StringField()
    

