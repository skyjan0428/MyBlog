from django.shortcuts import render
from blog.models import User, Post, Token, LikePost, Message, Relationship, Photo
from .forms import SignUpForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from urllib.parse import unquote
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
import datetime
# Create your views here.


global forms

forms = {'form':SignUpForm, 'signin': LoginForm,}

def photopage(request):
	return render(request, 'photo.html', locals())

def index(request):
	token = request.COOKIES['token']
	user = getUserByToken(token)
	if user:
		return information(request, id=user.id)
	return render(request, 'login.html', locals())

def information(request, id=None):
	token = request.COOKIES['token']
	user = getUserByToken(token)
	informations = User.objects.get(id=id)
	replyDic = {}
	replyDic['User'] = informations
	replyDic['posts'] = getPosts(request,informations, user)
	replyDic['chats'] = getChatList(request, user)
	replyDic['photo'] = getUserPhoto(informations)

	# if user and user!=informations:
	# 	relationship1 = Relationship.objects.filter(user_id1 = user, user_id2 = informations).first()
	# 	relationship2 = Relationship.objects.filter(user_id1 = informations, user_id2 = user).first()
	# 	if relationship1:
	# 		if relationship1.value == 0:
	# 			replyDic['text'] = 'waiting'
	# 			# return render(request, 'information.html', {'User': informations, 'text':"waiting"})
	# 		else:
	# 			replyDic['text'] = 'AlreadyFriend'
	# 			# return render(request, 'information.html', {'User': informations, 'text':"AlreadyFriend"})
	# 	elif relationship2:
	# 		if relationship2.value == 0:
	# 			replyDic['waitConfirm'] = informations.user_id
	# 			# return render(request, 'information.html', {'User': informations, 'waitConfirm': informations.user_id})
	# 		else:
	# 			replyDic['text'] = 'AlreadyFriend'
	# 			# return render(request, 'information.html', {'User': informations, 'text':"AlreadyFriend"})
	# 	else:
	# 		replyDic['addFriend'] = True
	# 		# return render(request, 'information.html', {'User': informations, 'addFriend':True})

	return render(request, 'information.html', replyDic)


def getChatList(request, user=None):
	if user:
		users = User.objects.exclude(id=user.id)
	else:
		users = User.objects.all()
	lst = []
	for user in users:
		dic = {}
		dic['user_id'] = user.id
		dic['name'] = user.name
		dic['photo'] = getUserPhoto(user)
		lst.append(dic)
	return lst


def getPosts(request, user=None, onwer=None):
	if user:
		posts = Post.objects.filter(user=user, attach_id=None).order_by('-date')
	else:
		posts = Post.objects.all().order_by('-date')
	lst = []
	for post in posts:
		data = {
			'date':post.date.strftime("%Y-%m-%d"),
			'content': post.content,
			'id': post.id,
			'name': post.user.name,
			'likes': len(LikePost.objects.filter(post=post)),
			'hasLike': LikePost.objects.filter(post=post, user=onwer).first(),
			'userPhoto': getUserPhoto(post.user)
		}
		attachPost = Post.objects.filter(attach=post)
		messages = []
		for p in attachPost:
			m = {
				'id': p.id,
				'name': p.user.name,
				'user_id':p.user_id,
				'content':p.content,
				'userPhoto': getUserPhoto(p.user)
			}
			messages.append(m)
		data['messages'] = messages
		photo = Photo.objects.filter(post=post).first()
		if photo:
			data['contentPhoto'] = photo.photo.url
		lst.append(data)
	return lst

@csrf_exempt
def addFriend(request):
	if not checkLogin(request):
		return JsonResponse({'status':False, 'data':{}})
	# try:
	user_id = getRequestData(request)['user_id']
	user_other = User.objects.get(user_id = user_id)
	user_self = getUserByToken(request.COOKIES['token'])
	relationship = Relationship.objects.filter(user_id1=user_other, user_id2=user_self).first()
	if relationship:
		relationship.value += 1
		relationship.save();
	else:
		relationship = Relationship(value=0, user_id1=user_self, user_id2=user_other)
		relationship.save()
		# return JsonResponse({'status':False, 'data':{}})
	return JsonResponse({'status':True, 'data':{}})

@csrf_exempt
def openChatRoom(request):
	if request.method == 'POST':
		token = request.POST.get('token')
		user = getUserByToken(token)
	if user:
		reciever = User.objects.filter(id=request.POST.get('reciever')).first()
		messages = Message.objects.filter(Q(sender=user, reciever=reciever) | Q(sender=reciever, reciever=user)).order_by("date")
		lst = []
		for message in messages:
			dic = {}
			dic['user_id'] = message.sender.id
			dic['message_id'] = message.id
			dic['text'] = message.text
			lst.append(dic)
		data = { 
			'messages':lst,
			'reciever':{
					'id': reciever.id,
					'photo' : getUserPhoto(reciever),
					'name':reciever.name 
			}
		}
		return JsonResponse({'status':True, 'data':data})
	# except Exception as e:
		# print(e)
		# return JsonResponse({'status':False, 'data':{}})




@csrf_exempt
def postOperation(request):
	global operate
	if request.method == 'POST':
		token = request.POST.get('token')
		user = getUserByToken(token)
		if user:
			return operate[request.POST.get('type')](request, user)
	return JsonResponse({'status':False, 'data':{}})


def likePost(request, user):
	post = Post.objects.filter(id = request.POST.get('post_id')).first()
	if post:
		likePost = LikePost.objects.filter(post=post, user=user).first()
		if likePost:
			likePost.delete()
			like = False
		else:
			likePost = LikePost(post = post, user=user)
			likePost.save()
			like = True
		return JsonResponse({'status':True, 'data':{'likes': len(LikePost.objects.filter(post_id=post)),
													'like':like,}})
	return JsonResponse({'status':False, 'data':{}})


def uploadPost(request, user):
	image = request.FILES.get('files')
	is_valid, response = isvalidImage(image)
	if not is_valid:
		return JsonResponse(response)
	content = request.POST.get('content')
	attach_id = request.POST.get('attach_id')
	new_post = Post(content = content, user = user, attach=Post.objects.filter(id = attach_id).first())
	new_post.save()
	data = {
		'content': new_post.content,
		'date': new_post.date.strftime("%Y-%m-%d"),
		'post_id': new_post.id,
		'name':user.name,
		'userPhoto': getUserPhoto(user),
	}
	if image:
		photo = Photo(user=user, photo=image, post = new_post)
		photo.save()
		data['contentPhoto'] = photo.photo.url
	if attach_id:
		data['attach_id'] = attach_id	
	return JsonResponse({'status':True, 'data':data})



global operate
operate={
	'likepost':likePost,
	'uploadPost': uploadPost,
}


@csrf_exempt
def revise(request):
	global revise_action
	if request.method == 'POST':
		token = request.POST.get('token')
		user = getUserByToken(token)
		if user:
			return revise_action[data[request.POST.get('type')]](request, user)
	return JsonResponse({'status':False, 'data':{}})


def createDescription(request, user):
	user.description = request.POST.get('description').replace('+', ' ')
	user.save()
	return JsonResponse({'status':True, 'data':{}})


global revise_action

revise_action = {
	'1': createDescription,
}




def signup(request):
	global forms
	if request.method == 'POST':
		name = request.POST.get('Username');
		password = request.POST.get('Password');
		email = request.POST.get('Email');
		user = User(name=name, password=make_password(password), email=email)
		user.save()
	return render(request, 'login.html', forms)


def login(request):
	global forms
	# if checkLogin(request):
	# 	return render(request, 'main.html', {'posts': getPosts(request)})
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if not form.is_valid():
			return render(request, 'login.html', forms)
		user = User.objects.get(email=form.cleaned_data['email'])
		password = user.password
		if check_password(form.cleaned_data['password'], password):
			token = generate_token(user.email)
			t = Token(user=user, token=token)
			t.save()
			response = HttpResponseRedirect("/")
			response.set_cookie(key='token', value=token)
			return response
	return render(request, 'login.html', forms)




import time
import base64
import hmac

def generate_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest() 
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")


def getUserByToken(token):
	try:
		return Token.objects.get(token=token.replace('\"', '')).user
	except:
		return None
def getUserPhoto(user):
	blank_photo_id = 1
	photo = Photo.objects.filter(user=user, is_sticker=True).first()
	return photo.photo.url if photo else Photo.objects.get(id=blank_photo_id).photo.url

def isvalidImage(image):
	if not image:
		return True, {}
	image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
        ]
	if image.content_type not in image_types:
		data = {
			'status': False,
			'error': 'Bad image format.'
		}
		return False, data
	else:
		return True, {}

def SignIn(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = User.objects.get(email=email)
		if not user:
			return JsonResponse({'status':True, 'data':{
				'SignIn': False,
				'Message': 'input email is not exist.'
			}})
		if check_password(user.password, password):
			loginByToken(user)
	return JsonResponse({'status':True, 'data':{
				'SignIn': False,
				'Message': 'password is not correct',
			}})	
def SignUpApi(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		if User.objectl.get(email=email):
			return JsonResponse({'status':True, 'data':{
				'SignIn': False,
				'Message': 'input email is not exist.'
			}})
		user = User(name=request.POST.get('name'),password=make_password(request.POST.get('password')),email=email)
		user.save()
		return loginByToken(user)
	return render(request, 'login.html', forms)

def loginByToken(user):
	token = generate_token(user.email)
	t = Token(user=user, token=token)
	t.save()
	return JsonResponse({'status':True, 'data':{
			'SignIn': True,
			'Message': '',
			'token': t 
	}})
# class RequestOperate():
# 	def __init__(self, request):
# 		self.request = request
# 		self.data = getRequestData()
# 		self.user = getUserByToken()
# 		self.isAuth = self.user==None
# 	def getRequestData(self):
# 		rows = self.request.body.decode().split('&')
# 		data = {}
# 		for row in rows:
# 			row = row.split('=')
# 			data[row[0]] = unquote(row[1])
# 		return data		
# 	def getUserByToken(self):
# 		try:
# 			return Token.objects.get(token=self.data['token']).user_id
# 		except:
# 			return None


# def certify_token(key, token):
#     token_str = base64.urlsafe_b64decode(token).decode('utf-8')
#     token_list = token_str.split(':')
#     if len(token_list) != 2:
#         return False
#     ts_str = token_list[0]
#     if float(ts_str) < time.time():
#         # token expired
#         return False
#     known_sha1_tsstr = token_list[1]
#     sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
#     calc_sha1_tsstr = sha1.hexdigest()
#     if calc_sha1_tsstr != known_sha1_tsstr:
#         # token certification failed
#         return False 
#     # token certification success
#     return True 
