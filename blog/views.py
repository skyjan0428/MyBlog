from django.shortcuts import render
from blog.models import User, Post, Token, LikePost, Message, Relationship, Photo
from .forms import SignUpForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from urllib.parse import unquote
import json
from django.http import JsonResponse
from django.db.models import Q
# import datetime
# Create your views here.


global forms

forms = {'form':SignUpForm, 'signin': LoginForm,}


def testJson(request):
	posts = Post.objects.filter(attach=None)
	for post in posts:
		print(post.content)
	return JsonResponse({'foo':'bar'})



def add(request):
    if request.method == "POST":
        user_img = request.FILES.get('user_image')
        photo = Photo(user_id=getUserByToken(request.COOKIES['token']), photo=user_img)
        photo.save()
        
    return render(request, 'adPhoto.html', locals())


def index(request):
	global forms
	if checkLogin(request):
		user = getUserByToken(request.COOKIES['token'])
		return information(request, user)
		# return render(request, 'main.html', {'posts': getPosts(request), 'users':getUserList(request)})
	return render(request, 'login.html', forms)

def getUserList(request, user=None):
	if user:
		users = User.objects.exclude(user_id=user.user_id)
	else:
		users = User.objects.all()
	return users

def getPosts(request, user=None):
	if user:
		posts = Post.objects.filter(user_id=user).order_by('-date')
	else:
		posts = Post.objects.all().order_by('-date')
	lst = []
	for post in posts:
		data = {
		'date':post.date,
		'content': post.content,
		'id': post.post_id,
		'name': post.user_id.name
		}
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
	if not checkLogin(request):
		return JsonResponse({'status':False, 'data':{}})
	try:
		user = getUserByToken(request.COOKIES['token'])
		reciever = getRequestData(request)['reciever']
		messages = Message.objects.filter(Q(sender=user, reciever=reciever) | Q(sender=reciever, reciever=user)).order_by("date")
		lst = []
		for message in messages:
			dic = {}
			dic['message_id'] = message.message_id
			dic['text'] = ('You : ' if message.sender == user else (message.sender.name + " : ")) + message.text
			lst.append(dic)
		return JsonResponse({'status':True, 'data':lst})
	except:
		return JsonResponse({'status':False, 'data':{}})




@csrf_exempt
def postOperation(request):
	global operate
	if request.method == 'POST':
		data = getRequestData(request)
		return operate[data['operate']](request, data)
	return JsonResponse({'status':False, 'data':{}})

def likePost(request, data):
	post = Post.objects.filter(post_id = data['post_id']).first()
	if post:
		user = getUserByToken(request.COOKIES['token'])
		likePost = LikePost.objects.filter(post_id=post, user_id=user).first()
		if likePost:
			likePost.delete()
		else:
			likePost = LikePost(post_id = post, user_id=user)
			likePost.save()
		return JsonResponse({'status':True, 'data':{}})
	else:
		return JsonResponse({'status':False, 'data':{}})

global operate
operate={
	'1':likePost,
}



@csrf_exempt
def revise(request):
	global revise_action
	if not checkLogin(request):
		return JsonResponse({'status':False, 'data':{}})
	data = getRequestData(request)
	return revise_action[data['type']](request, data)

def createDescription(request, data):
	user = getUserByToken(request.COOKIES['token'])
	user.description = data['description'].replace('+', ' ')
	user.save()
	return JsonResponse({'status':True, 'data':{}})


global revise_action

revise_action = {
	'1': createDescription,
}

def information(request, informations):
	if not checkLogin(request):
		return JsonResponse({'status':False, 'data':{}})
	# informations = User.objects.filter(user_id=id).first()
	user = getUserByToken(request.COOKIES['token'])
	replyDic = {}
	replyDic['User'] = informations
	replyDic['posts'] = getPosts(request,informations)
	replyDic['chats'] = getUserList(request, user)
	photos = Photo.objects.filter(user_id = informations)
	replyDic['photos'] = photos

	if user and user!=informations:
		relationship1 = Relationship.objects.filter(user_id1 = user, user_id2 = informations).first()
		relationship2 = Relationship.objects.filter(user_id1 = informations, user_id2 = user).first()
		if relationship1:
			if relationship1.value == 0:
				replyDic['text'] = 'waiting'
				# return render(request, 'information.html', {'User': informations, 'text':"waiting"})
			else:
				replyDic['text'] = 'AlreadyFriend'
				# return render(request, 'information.html', {'User': informations, 'text':"AlreadyFriend"})
		elif relationship2:
			if relationship2.value == 0:
				replyDic['waitConfirm'] = informations.user_id
				# return render(request, 'information.html', {'User': informations, 'waitConfirm': informations.user_id})
			else:
				replyDic['text'] = 'AlreadyFriend'
				# return render(request, 'information.html', {'User': informations, 'text':"AlreadyFriend"})
		else:
			replyDic['addFriend'] = True
			# return render(request, 'information.html', {'User': informations, 'addFriend':True})

	return render(request, 'information.html', replyDic)

def signup(request):
	global forms
	if checkLogin(request):
		return render(request, 'success.html', forms)
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if not form.is_valid():
			return render(request, 'login.html', forms)
		user = User(name = form.cleaned_data['name'], password = make_password(form.cleaned_data['password']), email = form.cleaned_data['email'])
		user.save()
	return render(request, 'login.html', forms)


def login(request):
	global forms
	if checkLogin(request):
		return render(request, 'main.html', {'posts': getPosts(request)})
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if not form.is_valid():
			return render(request, 'login.html', forms)
		user = User.objects.get(email=form.cleaned_data['email'])
		password = user.password
		if check_password(form.cleaned_data['password'], password):
			token = generate_token(user.email)
			t = Token(user_id=user, token=token)
			t.save()
			response = render(request, 'main.html', locals())
			response.set_cookie(key='token', value=token)
			return response
	return render(request, 'login.html', forms)

@csrf_exempt
def post(request):
	if request.method == 'POST':
		data = getRequestData(request)
		token = data['token'].replace('\"', '')
		user_id = Token.objects.get(token=token).user_id
		if user_id:
			new_post = Post(content = data['content'], user_id = user_id)
			new_post.save()
			data = {
			'content': new_post.content,
			'date': new_post.date,
			}
			return JsonResponse({'status':True, 'data':data})

	return JsonResponse({'status':False, 'data':{}})

def getRequestData(request):
	rows = request.body.decode().split('&')
	print(rows)
	data = {}
	for row in rows:
		row = row.split('=')
		data[row[0]] = unquote(row[1])
	return data		

import time
import base64
import hmac

def checkLogin(request):
	global forms
	try: 
		token = request.COOKIES['token']
		tokens = Token.objects.get(token=token)
		return True
	except:
		print('token:' , 0)
		return False

def generate_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest() 
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

def getUserByToken(token):
	user = Token.objects.get(token=token).user_id
	if user:
		return user
	return None
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
