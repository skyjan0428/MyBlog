from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Message)
admin.site.register(LikePost)
admin.site.register(Notification)
admin.site.register(Photo)

