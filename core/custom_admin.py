
from django.contrib import admin
from taggit.models import Tag

class CustomTagAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Add Tags'  # Change the display name here

admin.site.unregister(Tag)
admin.site.register(Tag, CustomTagAdmin)