from django.urls import path
from django.http import HttpResponseRedirect
from .models import*
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import ChatThread

# Register your models here.

# admin.site.register(Message)
# admin.site.register(ChatThread)


class ChatThreadAdmin(admin.ModelAdmin):
    list_display = ('Name', 'action')
    list_display_links = None

    def Name(self, obj):
        return f"Discussed {obj.first_user.full_name} & {obj.second_user.full_name}"

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        url_block = reverse('admin:block_chat', args=[obj.id])  
        
        
        button_text = "Block"
        if obj.block:
            button_text = "Blocked"
        
        return format_html(
            '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a> <a href="{}" class="btn btn-secondary btn-sm">{}</a>',
            url_edit, url_delete, url_block, button_text
        )
    action.short_description = 'Actions'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('block_chat/<int:chat_id>/', self.block_chat, name='block_chat'),
        ]
        return custom_urls + urls

    def block_chat(self, request, chat_id):
        chat_thread = ChatThread.objects.get(id=chat_id)
        chat_thread.block = not chat_thread.block  
        chat_thread.save()
        self.message_user(request, "Chat block status updated successfully.")
        return HttpResponseRedirect(reverse('admin:chats_chatthread_changelist'))

    
    


class MessageAdmin(admin.ModelAdmin):
    list_display = ('Name', "action")
    list_display_links = None

    def Name(self, obj):
        return "Disscussed  " +  obj.sender.full_name + "  &  " + obj.receiver.full_name 
   
    
    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )

    
admin.site.register(ChatThread,ChatThreadAdmin)
admin.site.register(Message,MessageAdmin)