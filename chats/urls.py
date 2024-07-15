from django.urls import path
from .views import*

urlpatterns = [
    path('chats', MyChats,name="chats"),
    path('chatPage/<str:username>', ChatPage,name="chatPage"),

    path('initiate_pusher',InitiatePusher.as_view(), name="initiate_pusher"),
    path('send_messages',sendMessage.as_view(), name="send_messages"),
    path('fetch_messages',FetchMessagesView.as_view(),name="fetch_messages"),
    path('fetch_thread', FetchChatThreadView.as_view(),name="fetch_thread"),
]