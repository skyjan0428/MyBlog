from django.db import models
import datetime

# Create your models here.

class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=10)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=100)
	description = models.TextField(null=True)
	

class Relationship(models.Model):
	relationship_id = models.AutoField(primary_key=True)
	date = models.DateTimeField('Datetime', auto_now=True)
	value = models.IntegerField()
	user_id1 = models.ForeignKey(User,related_name='self', on_delete=models.PROTECT)
	user_id2 = models.ForeignKey(User,related_name='other', on_delete=models.PROTECT)

class Post(models.Model):
	post_id = models.AutoField(primary_key=True)
	date = models.DateTimeField('Datetime', auto_now=True)
	content = models.TextField()
	user_id = models.ForeignKey(User,related_name='post_user_id', on_delete=models.PROTECT)
	attach = models.ForeignKey('self',related_name='attach_to_post', on_delete=models.PROTECT, null = True)

class Token(models.Model):
	token_id = models.AutoField(primary_key=True)
	date = models.DateTimeField('Datetime', auto_now=True)
	token = models.CharField(unique = True, null = True, max_length=255)
	user_id = models.ForeignKey(User,related_name='token_user_id', on_delete=models.PROTECT, default='')

class Message(models.Model):
	message_id = models.AutoField(primary_key=True)
	sender = models.ForeignKey(User,related_name='sender', on_delete=models.PROTECT)
	reciever = models.ForeignKey(User,related_name='reciever', on_delete=models.PROTECT)
	date = models.DateTimeField('Datetime', auto_now=True)
	text = models.TextField(null=True)


class LikePost(models.Model):
	likePost_id = models.AutoField(primary_key=True)
	post_id = models.ForeignKey(Post,related_name='like_post_id', on_delete=models.PROTECT)
	user_id = models.ForeignKey(User,related_name='like_user_id', on_delete=models.PROTECT, default='')

class Client(models.Model):
	client_id = models.AutoField(primary_key=True)
	date = models.DateTimeField('Datetime', auto_now=True)
	channel_name = models.CharField(max_length=100)
	user_id = models.ForeignKey(User,related_name='client_user_id', on_delete=models.PROTECT, default='')

class Photo(models.Model):
	photo_id = models.AutoField(primary_key=True)
	photo = models.ImageField(upload_to='photo/')
	user_id = models.ForeignKey(User,related_name='photo_user_id', on_delete=models.PROTECT, default='')
	is_sticker = models.BooleanField(default=False)
	date = models.DateTimeField('Datetime', auto_now=True)
	post_id = models.ForeignKey(Post,related_name='photo_post_id', on_delete=models.PROTECT, default='', null = True)




