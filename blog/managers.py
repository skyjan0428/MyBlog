from django.db import models
# from .models import LikePost, Photo

class MainPostManager(models.Manager):
	def get(self, user):
		posts = self.filter(user=user, attach_id=None).order_by('-date')
		lst = []
		for post in posts:
			data = {
				'date':post.date.strftime("%Y-%m-%d"),
				'content': post.content,
				'id': post.id,
				'name': post.user.name,
				'likes': LikePost.postLikes.getPostLikesCount(post),
				'hasLike': LikePost.postLikes.is_like(post, user),
				'userPhoto': Photo.blogPhoto.get(post.user)
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
			'userPhoto': Photo.blogPhoto.get(post.user),
			'contentPhoto': Photo.blogPhoto.getContentPhoto(post)
		}
		return p
	def getAttachs(self, post):
		return self.filter(attach=post)


class BlogPhotoManager(models.Manager):
	def getUserPhoto(self, user):
		blank_photo_id = 1
		photo = self.filter(user=user, is_sticker=True).first()
		return photo.photo.url if photo else self.get(id=blank_photo_id).photo.url
	def getContentPhoto(self, post):
		return self.filter(post=post)



class PostLikesManager(models.Manager):
	def getPostLikesCount(self, post):
		return self.filter(post=post).count()
	def is_like(self, post, user):
		return self.filter(post=post, user=user).isExist(),
