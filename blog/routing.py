from django.urls import path
from blog.consumers import Consumer

websocket_urlpatterns = [
    path('blog/', Consumer),
]