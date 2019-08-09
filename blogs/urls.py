"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from blog.views import *
from django.conf.urls.static import static
from django.conf import settings

from django.shortcuts import render



urlpatterns = [
    path('admin/', admin.site.urls),
    path('photo/', photopage, name="photo"),
    path(r'', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('information/<int:id>/', information, name='information'),
    path('post/<int:id>/', post, name='post'),
    path('information/addFriend/', addFriend, name='addFriend'),
    path('information/revise/', revise, name='revise'),
    path('postoperation/', postOperation, name='postoperation'),
    path('openChatRoom/', openChatRoom, name='openChatRoom'),
    path('readNotifications/', readNotifications, name='readNotifications'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



