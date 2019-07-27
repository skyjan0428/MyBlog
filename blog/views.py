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
	return JsonResponse({'id':1, 'name': 'abc', 'description':'des'})
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
	informations = User.userChat.get(id=id)
	replyDic = {}
	replyDic['User'] = informations
	replyDic['posts'] = Post.mainPost.get(user=informations)
	replyDic['chats'] = User.userChat.getChatList(user=user)
	replyDic['photo'] = Photo.blogPhoto.getUserPhoto(informations)

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
		messages = Message.messages.getMessages(sender=user, reciever=reciever)
		data = { 
			'messages':messages,
			'reciever':{
					'id': reciever.id,
					'photo' : Photo.blogPhoto.getUserPhoto(reciever),
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
		postLikes, is_like = LikePost.postLikes.likePress(post=post, user=user)
		return JsonResponse({'status':True, 'data':{'likes': postLikes,
													'like':is_like,}})
	return JsonResponse({'status':False, 'data':{}})


def uploadPost(request, user):
	image = request.FILES.get('files')
	is_valid, response = isvalidImage(image)
	if not is_valid:
		return JsonResponse(response)
	content = request.POST.get('content')
	attach = request.POST.get('attach_id')
	data = Post.mainPost.uploadPost(user=user, content=content, attach=attach, image=image)
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
