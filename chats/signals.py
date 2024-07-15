# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import *
# import json

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# @receiver(post_save, sender=ChatNotification)
# def send_notification(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         notification_obj = ChatNotification.objects.filter(is_seen=False, user=instance).count()
#         user_id = str(instance.id)
#         data = {
#             'count':notification_obj
#         }

#         async_to_sync(channel_layer.group_send)(
#             user_id, {
#                 'type':'send_notification',
#                 'value':json.dumps(data)
#             }
#         )


# @receiver(post_save, sender=CustomUser)
# def send_onlineStatus(sender, instance, created, **kwargs):
#     if not created:
#         channel_layer = get_channel_layer()
#         data = {
#             'email':instance.email,
#             'status':instance.online_status
#         }
#         # async_to_sync(channel_layer.group_send)(
#         #     'user', {
#         #         'type':'send_onlineStatus',
#         #         'value':json.dumps(data)
#         #     }
#         # )