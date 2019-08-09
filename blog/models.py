from django.db import models
import datetime
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
# from blog.managers import MainPostManager, BlogPhotoManager, PostLiksManager

# Create your models here.


class MainPostManager(models.Manager):
	def get(self, user=None, post_id = None, owner=None):
		if post_id:
			posts = self.get_queryset().filter(id=post_id, is_delete=False)
		else:
			posts = self.get_queryset().filter(owner=owner, attach_id=None, is_delete=False).order_by('-date')
		
		lst = []
		for post in posts:
			data = {
				'date':post.date.strftime("%Y-%m-%d"),
				'content': post.content,
				'id': post.id,
				'name': post.user.name,
				'user_id':post.user.id,
				'likes': LikePost.postLikes.getPostLikesCount(post),
				'hasLike': LikePost.postLikes.is_like(post, user),
				'userPhoto': Photo.blogPhoto.getUserPhoto(post.user),
				'contentPhotos': Photo.blogPhoto.getContentPhoto(post),
				'has_auth': user == post.user or user==post.owner,
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
			'name': post.owner.name,
			'user_id':post.owner.id,
			'content':post.content,
			'userPhoto': Photo.blogPhoto.getUserPhoto(post.user),
		}
		return p
	def getAttachs(self, post):
		return self.filter(attach=post)

	def uploadPost(self, user, content, attach, image, owner):
		new_post = Post(content=content, user=user, attach=Post.objects.filter(id=attach).first(), owner=owner)
		new_post.save()
		data = {
			'content': new_post.content,
			'date': new_post.date.strftime("%Y-%m-%d"),
			'post_id': new_post.id,
			'user_id':user.id,
			'name':user.name,
			'userPhoto': Photo.blogPhoto.getUserPhoto(user),
			'attach_id': attach
		}
		Photo.blogPhoto.uploadPostPhoto(image, data, new_post)
		return data


class BlogPhotoManager(models.Manager):
	def getUserPhoto(self, user):
		blank_photo_id = 1
		photo = self.get_queryset().filter(user=user, is_sticker=True).first()
		return photo.photo.url if photo else '/static/images/blank.jpg' #self.get_queryset().get(id=blank_photo_id).photo.url
	def getContentPhoto(self, post):
		return self.get_queryset().filter(post=post)
	def uploadPostPhoto(self, image, data, post):
		if image:
			photo = Photo(user=post.user, photo=image, post = post)
			photo.save()
			data['contentPhoto'] = photo.photo.url
	def getUserPhotoAll(self, user):
		return self.get_queryset().filter(user=user).order_by("-date")


class ClientNotifyManager(models.Manager):
	def sendPostLikeNotify(self, user, post):
		notification = Notification(category='postLike', user=post.user, post=post)
		notification.save()
		clients = Client.objects.filter(user=notification.user)
		for client in clients:
			async_to_sync(channel_layer.send)(client.channel_name, {"type": notification.category, "post": post.id, "user":post.user.id, "content": user.name + " likes your post."})
	def sendPostMessageNotify(self, user, post):
		notification = Notification(category='postMessage', user=post.user, post=post)
		notification.save()
		clients = Client.objects.filter(user=post.user)
		for client in clients:
			async_to_sync(channel_layer.send)(client.channel_name, {"type": notification.category, "post": post.id, "user":post.user.id, "content": user.name + " leave message on your post."})




class PostLikesManager(models.Manager):
	def getPostLikesCount(self, post):
		return self.get_queryset().filter(post=post).count()
	def is_like(self, post, user):
		return self.get_queryset().filter(post=post, user=user).first() != None
	def likePress(self, post, user):
		is_like = self.is_like(post=post, user=user)
		if is_like:
			self.get_queryset().get(post=post, user=user).delete()
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
			print(message.text)
			dic = {
			  'user_id' : message.sender.id,
			  'message_id': message.id,
			  'text' : message.text
			}
			lst.append(dic)
		return lst
		

class NotificationManager(models.Manager):
	def getAllNotifications(self, user):
		notis = self.get_queryset().filter(user=user).order_by("-date")
		lst = []
		for noty in notis:
			dic = {
				'date':noty.date.strftime("%Y-%m-%d"),
				'category': noty.category,
				'user': noty.user,
			}
			if noty.category == 'postMessage':
				dic['post_id'] = noty.post.id
				dic['content'] = noty.user.name + " leaves a message on your post."
				dic['post'] = noty.post
				dic['photo'] = Photo.blogPhoto.getUserPhoto(user=noty.user)
			elif noty.category == 'postLike':
				dic['post_id'] = noty.post.id
				dic['content'] = noty.user.name + " likes your post."
				dic['post'] = noty.post
				dic['photo'] = Photo.blogPhoto.getUserPhoto(user=noty.user)
			else:
				dic['content'] = noty.user.name + " send a message to you."
				dic['sender_id'] = noty.message.sender.id
				dic['photo'] = Photo.blogPhoto.getUserPhoto(user=noty.message.sender)
			lst.append(dic)
		return lst










class User(models.Model):
	name = models.CharField(max_length=10)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=100)
	description = models.TextField(default='新增個人簡介，讓大家更瞭解你。')
	
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
	owner = models.ForeignKey(User,related_name='post_owner_id', on_delete=models.PROTECT,  default='')
	attach = models.ForeignKey('self',related_name='attach_to_post', on_delete=models.PROTECT, null = True)
	is_delete = models.BooleanField(default=False)

	objects = models.Manager()
	mainPost = MainPostManager()



class Message(models.Model):
	sender = models.ForeignKey(User,related_name='sender', on_delete=models.PROTECT)
	reciever = models.ForeignKey(User,related_name='reciever', on_delete=models.PROTECT)
	date = models.DateTimeField('Datetime', auto_now=True)
	text = models.TextField(null=True)

	objects = models.Manager()
	messages = MessageManager()


class LikePost(models.Model):
	post = models.ForeignKey(Post,related_name='like_post_id', on_delete=models.PROTECT , default='')
	user = models.ForeignKey(User,related_name='like_user_id', on_delete=models.PROTECT, default='')

	objects = models.Manager()
	postLikes = PostLikesManager()

class Client(models.Model):
	date = models.DateTimeField('Datetime', auto_now=True)
	channel_name = models.CharField(max_length=100)
	user = models.ForeignKey(User,related_name='client_user_id', on_delete=models.PROTECT, default='')

	objects = models.Manager()
	clientNotify = ClientNotifyManager()

class Photo(models.Model): 
	photo = models.ImageField(upload_to='photo/')
	user = models.ForeignKey(User,related_name='photo_user_id', on_delete=models.PROTECT, default='', null=True)
	is_sticker = models.BooleanField(default=False)
	date = models.DateTimeField('Datetime', auto_now=True)
	post = models.ForeignKey(Post,related_name='photo_post_id', on_delete=models.PROTECT, default='', null=True)

	objects = models.Manager()
	blogPhoto = BlogPhotoManager()

class Token(models.Model):
	date = models.DateTimeField('Datetime', auto_now=True)
	token = models.CharField(unique = True, null = True, max_length=255)
	user = models.ForeignKey(User,related_name='token_user', on_delete=models.PROTECT, default='')


class Notification(models.Model):
	date = models.DateTimeField('Datetime', auto_now=True)
	category = models.CharField(max_length=50)
	user = models.ForeignKey(User,related_name='user_notify', on_delete=models.PROTECT, default='')
	message = models.ForeignKey(Message,related_name='message_notify', on_delete=models.PROTECT, null=True, default='')
	post = models.ForeignKey(Post,related_name='post_notify', on_delete=models.PROTECT, null=True, default='')
	is_read = models.BooleanField(default=False)

	objects = models.Manager()
	notification = NotificationManager()
















