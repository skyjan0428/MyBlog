from django.db import models
import datetime
from django.db.models import Q
# from blog.managers import MainPostManager, BlogPhotoManager, PostLiksManager

# Create your models here.


class MainPostManager(models.Manager):
	def get(self, user):
		posts = self.get_queryset().filter(user=user, attach_id=None).order_by('-date')
		lst = []
		for post in posts:
			data = {
				'date':post.date.strftime("%Y-%m-%d"),
				'content': post.content,
				'id': post.id,
				'name': post.user.name,
				'likes': LikePost.postLikes.getPostLikesCount(post),
				'hasLike': LikePost.postLikes.is_like(post, user),
				'userPhoto': Photo.blogPhoto.getUserPhoto(post.user)
			}
			attachPost = self.getAttachs(post)
			messages = []
			for p in attachPost:
				messages.append(self.getAttachPost(p))
			data['messages'] = messages
			lst.append(data)
		return lst
	def getAttachPost(self, post):
		p = {
			'id': post.id,
			'name': post.user.name,
			'user_id':post.user_id,
			'content':post.content,
			'userPhoto': Photo.blogPhoto.getUserPhoto(post.user),
			'contentPhoto': Photo.blogPhoto.getContentPhoto(post)
		}
		return p
	def getAttachs(self, post):
		return self.filter(attach=post)

	def uploadPost(self, user, content, attach, image):
		new_post = Post(content=content, user=user, attach=Post.objects.filter(id = attach).first())
		new_post.save()
		data = {
			'content': new_post.content,
			'date': new_post.date.strftime("%Y-%m-%d"),
			'post_id': new_post.id,
			'name':user.name,
			'userPhoto': Photo.blogPhoto.getUserPhoto(user),
			'attach_id': attach
		}
		Photo.blogPhoto.uploadPostPhoto(image, data)
		return data


class BlogPhotoManager(models.Manager):
	def getUserPhoto(self, user):
		blank_photo_id = 1
		photo = self.get_queryset().filter(user=user, is_sticker=True).first()
		return photo.photo.url if photo else self.get_queryset().get(id=blank_photo_id).photo.url
	def getContentPhoto(self, post):
		return self.get_queryset().filter(post=post)
	def uploadPostPhoto(self, image, data):
		if image:
			photo = Photo(user=user, photo=image, post = new_post)
			photo.save()
			data['contentPhoto'] = photo.photo.url

	




class PostLikesManager(models.Manager):
	def getPostLikesCount(self, post):
		return self.get_queryset().filter(post=post).count()
	def is_like(self, post, user):
		return self.get_queryset().filter(post=post, user=user).exists(),
	def likePress(self, post, user):
		is_like = self.is_like(post=post, user=user)
		if is_like:
			LikePost.objects.get(post=post, user=user).delete()
		else:
			likePost = LikePost(post=post, user=user)
			likePost.save()
		return self.getPostLikesCount(post), not is_like


class UserChatManager(models.Manager):
	def getChatList(self, user):
		users = self.get_queryset().exclude(id=user.id)
		lst = []
		for user in users:
			dic = {}
			dic['user_id'] = user.id
			dic['name'] = user.name
			dic['photo'] = Photo.blogPhoto.getUserPhoto(user)
			lst.append(dic)
		return lst

class MessageManager(models.Manager):
	def getMessages(self, sender, reciever):
		messages = self.get_queryset().filter(Q(sender=sender, reciever=reciever) | Q(sender=reciever, reciever=sender)).order_by("date")
		lst = []
		for message in messages:
			dic = {
			  'user_id' : message.sender.id,
			  'message_id': message.id,
			  'text' : message.text
			}
		lst.append(dic)
		return lst
		











class User(models.Model):
	name = models.CharField(max_length=10)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=100)
	description = models.TextField(null=True)

	objects = models.Manager()
	userChat = UserChatManager()
	

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

	mainPost = MainPostManager()



class Message(models.Model):
	sender = models.ForeignKey(User,related_name='sender', on_delete=models.PROTECT)
	reciever = models.ForeignKey(User,related_name='reciever', on_delete=models.PROTECT)
	date = models.DateTimeField('Datetime', auto_now=True)
	text = models.TextField(null=True)

	messages = MessageManager()


class LikePost(models.Model):
	post = models.ForeignKey(Post,related_name='like_post_id', on_delete=models.PROTECT , default='')
	user = models.ForeignKey(User,related_name='like_user_id', on_delete=models.PROTECT, default='')

	postLikes = PostLikesManager()

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

	blogPhoto = BlogPhotoManager()

class Token(models.Model):
	date = models.DateTimeField('Datetime', auto_now=True)
	token = models.CharField(unique = True, null = True, max_length=255)
	user = models.ForeignKey(User,related_name='token_user', on_delete=models.PROTECT, default='')





















