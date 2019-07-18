from django.shortcuts import render
from blog.models import User, Post, Token, LikePost
from .forms import SignUpForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from urllib.parse import unquote
import json
from django.http import JsonResponse
# import datetime
# Create your views here.


global forms

forms = {'form':SignUpForm, 'signin': LoginForm,}


def testJson(request):
	return JsonResponse({'foo':'bar'})


def index(request):
	global forms
	if checkLogin(request):
		return render(request, 'main.html', {'posts': getPosts(request)})
	return render(request, 'login.html', forms)

def getPosts(request):
	posts = Post.objects.all()
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

def information(request):
	user = getUserByToken(request.COOKIES['token'])
	if user:
		return render(request, 'information.html', {'User': user})
	return render(request, 'login.html', forms)

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
		return render(request, 'success.html', forms)
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
		rows = request.body.decode().split('&')
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
	if request.COOKIES['token']:
		try:
			tokens = Token.objects.get(token=request.COOKIES['token'])
			return True
		except:
			return False
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
