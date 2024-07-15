from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Message , ChatThread
from rest_framework import status
from .serializers import MessageSerializer
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Q
from django.utils import dateformat
from django.shortcuts import render
from .models import*
import pusher

pusher_client = pusher.Pusher(
  app_id=settings.PUSHER_APP_ID,
  key=settings.PUSHER_KEY,
  secret=settings.PUSHER_SECRET,
  cluster=settings.PUSHER_CLUSTER,
  ssl=True
)

class InitiatePusher(APIView):
    def get(self , request):
        return Response({"message":"Pusher Initiated","key":settings.PUSHER_KEY,"cluster":settings.PUSHER_CLUSTER})


def MyChats(request):
    if request.user.is_Teacher == True and request.user.is_Student == False:
        return render(request, 'teacher/chat.html')
    elif request.user.is_Teacher == False and request.user.is_Student == True:
        return render(request, 'user-face/chats.html')
    
def ChatPage(request, username):
    user_obj = CustomUser.objects.get(email=username)
    if request.user.is_Teacher == False and request.user.is_Student == True:
        users = CustomUser.objects.filter(is_Teacher=True,is_Student=False).exclude(email=request.user.email)
    else:
        users = CustomUser.objects.filter(is_Teacher=False,is_Student=True).exclude(email=request.user.email)

    return render(request, 'user-face/messages.html', context={'user': user_obj, 'users': users,})

class sendMessage(APIView):
    def post(self, request):
        data = request.data
        sender = CustomUser.objects.get(id=data['sender'])
        receiver = CustomUser.objects.get(id=data['receiver'])
        
        if sender.is_Student:
            chat_channel = f'chat_{receiver.id}_{sender.id}'
        else:
            chat_channel = f'chat_{sender.id}_{receiver.id}'
        if (sender.is_authenticated):
            
            try:
                cth = ChatThread.objects.get(first_user=sender , second_user=receiver)
                if not cth.block:
                    message = Message.objects.create(sender = sender , receiver=receiver,description=data['message'])
                    cth.message=message
                    cth.save()
                    msg = MessageSerializer(message).data
                    pusher_client.trigger(chat_channel, chat_channel, {'message': msg})
                    return Response({"status":True,"msg":"Message sent","data":msg})
                else:
                    return Response({"status":False,"msg":"Can't send message, You blocked by admin!","data":{}})
            except:
                message = Message.objects.create(sender = sender , receiver=receiver,description=data['message'])
                ChatThread.objects.create(first_user=sender , second_user=receiver, message=message)
                msg = MessageSerializer(message).data
                pusher_client.trigger(chat_channel, chat_channel, {'message': msg})
                return Response({"status":True,"msg":"Message sent","data":msg})
            
            
        
        
class FetchMessagesView(APIView):
    def post(self , request):
        data = request.data
        sender = CustomUser.objects.get(id=data['sender'])
        if (sender.is_authenticated):
            try :
                #confirming if the receiver of this message actuall exists
                receiver = CustomUser.objects.get(id=data['receiver'])
                messages = Message.objects.fetch_messages(sender , receiver)
                context = {
                    "receiver_id":receiver.id,
                    "receiver_name":receiver.full_name,
                    "receiver_image":receiver.image_url,
                    "online_status":receiver.online_status,
                    "data":[
                        {
                            "id":message.id,
                            "sender":message.sender.id,
                            "receiver":message.receiver.id,
                            "description":message.description,
                            "time_stamp":dateformat.format(message.time_stamp, 'd-m-Y H:i A'),
                        } for message in messages
                    ]
                }
                # check if both users have a previous chat thread
                chat_thread = ChatThread.objects.get_thread(sender, receiver)
                if len(chat_thread) == 0 :
                    new_message = Message.objects.create(sender=sender , receiver=receiver)
                    ChatThread.objects.create(first_user=sender , second_user=receiver , message=new_message)
                return Response(context, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                context = {"error":"User does not exist"}
                return Response(context)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class FetchChatThreadView(APIView):
    def get(self , request):
        user = CustomUser.objects.get(id=request.headers['sender'])
        first_lookup = Q(first_user=user)
        second_lookup = Q(second_user=user)
        third_lookup = (~Q(message__description =''))
        queryset = ChatThread.objects.filter((first_lookup | second_lookup) & third_lookup).order_by("-message__time_stamp")
        serializer = [
            {
                "id":thread.id,
                "seen":thread.seen,
                "first_user":{
                    "id":thread.first_user.id,
                    "name":f"{thread.first_user.full_name}",
                    "email":f"{thread.first_user.email}",
                    "image":thread.first_user.image_url
                    },
                "second_user":{
                    "id":thread.second_user.id,
                    "name":f"{thread.second_user.full_name}",
                    "email":f"{thread.second_user.email}",
                    "image":thread.second_user.image_url
                    },
                "message":thread.message.description,
                "time_stamp":dateformat.format(thread.time_stamp, 'd-m-Y H:i A')
            } for thread in queryset
        ]
        # adding the ids of all the users the use has ever sent a message to , to a list
        ids = [chatthread.first_user.id if chatthread.first_user.id != user.id else
                chatthread.second_user.id for chatthread in queryset
                ]
        context = {
                "ids":f"{ids}",
                "data":serializer
            }
        return Response(context ,status=status.HTTP_200_OK)

    def post(self , request):
        data = request.data
        user = CustomUser.objects.get(id=data['sender'])
        receiver = data['receiver']
        try:
            receiver = CustomUser.objects.get(id=receiver)
            first_lookup = Q(first_user=user, second_user=receiver)
            second_lookup = Q(first_user=receiver , second_user=user)
            queryset = ChatThread.objects.filter(first_lookup | second_lookup).order_by('time_stamp')
            serializer = [
                {
                    "id":thread.id,
                    "seen":thread.seen,
                    "first_user":{
                        "name":f"{thread.first_user.email}",
                        "id":f"{thread.first_user.id}"
                        },
                    "second_user":{
                        "name":f"{thread.second_user.email}",
                        "id":f"{thread.second_user.id}"
                        },
                    "message":thread.message.description
                } for thread in queryset
            ]
            return Response(serializer, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            context = {
                "error": "User does not exist"
            }
            return Response(context)


