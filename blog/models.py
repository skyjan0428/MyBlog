from django.db import models
import datetime

# Create your models here.

class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=10)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=100)
	token = models.CharField(null = True, max_length=500)

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