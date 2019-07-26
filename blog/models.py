from django.db import models
import datetime

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=10)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=100)
	description = models.TextField(null=True)
	

class Relationship(models.Model):
	date = models.DateTimeField('Datetime', auto_now=True)
	value = models.IntegerField()
	user1 = models.ForeignKey(User,related_name='self', on_delete=models.PROTECT , default='')
	user2 = models.ForeignKey(User,related_name='other', on_delete=models.PROTECT, default='')

class Post(models.Model):
	date = models.DateTimeField('Datetime', auto_now=True)
	content = models.TextField()
	user = models.ForeignKey(User,related_name='post_user_id', on_delete=models.PROTECT,  default='')
	attach = models.ForeignKey('self',related_name='attach_to_post', on_delete=models.PROTECT, null = True)



class Message(models.Model):
	sender = models.ForeignKey(User,related_name='sender', on_delete=models.PROTECT)
	reciever = models.ForeignKey(User,related_name='reciever', on_delete=models.PROTECT)
	date = models.DateTimeField('Datetime', auto_now=True)
	text = models.TextField(null=True)


class LikePost(models.Model):
	post = models.ForeignKey(Post,related_name='like_post_id', on_delete=models.PROTECT , default='')
	user = models.ForeignKey(User,related_name='like_user_id', on_delete=models.PROTECT, default='')

class Client(models.Model):
	date = models.DateTimeField('Datetime', auto_now=True)
	channel_name = models.CharField(max_length=100)
	user = models.ForeignKey(User,related_name='client_user_id', on_delete=models.PROTECT, default='')

class Photo(models.Model):
	photo = models.ImageField(upload_to='photo/')
	user = models.ForeignKey(User,related_name='photo_user_id', on_delete=models.PROTECT, default='', null = True)
	is_sticker = models.BooleanField(default=False)
	date = models.DateTimeField('Datetime', auto_now=True)
	post = models.ForeignKey(Post,related_name='photo_post_id', on_delete=models.PROTECT, default='', null = True)

class Token(models.Model):
	date = models.DateTimeField('Datetime', auto_now=True)
	token = models.CharField(unique = True, null = True, max_length=255)
	user = models.ForeignKey(User,related_name='token_user', on_delete=models.PROTECT, default='')
