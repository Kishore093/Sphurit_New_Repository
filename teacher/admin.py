from django.db.models import Count
from django.contrib import admin
from django.urls import reverse

from .models import*
from django.utils.html import format_html
from django.db.models import Sum
from .models import HitCount, Course

# Register your models here.
# admin.site.register(Choices)
# admin.site.register(Answer)




# admin.site.register(CourseCategory)
# admin.site.register(Language)
# admin.site.register(Course)
# admin.site.register(Chapter)
# admin.site.register(Topic)
# admin.site.register(Feedback)
# admin.site.register(PurchasedCourse)
# custom form models
# admin.site.register(Questions)

admin.site.register(Form)
admin.site.register(Responses)
# admin.site.register(Event)
# admin.site.register(Certificate)
# admin.site.register(HitCount)
admin.site.register(CourseProgress)
admin.site.register(ChapterProgress)
# admin.site.register(TopicProgress)



# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('get_course_name_or_host_name', 'type','hit_count', 'created_at', 'approved',"action")  
#     search_fields = ('title', 'description') 
#     list_display_links = None 
#     list_per_page = 5
    
#     def get_course_name_or_host_name(self, obj):
#         """
#         Custom method to display either 'course_name' or 'host_name' with ellipsis if too long
#         """
#         course_name = obj.course_name if obj.course_name else obj.host_name
#         max_length = 25
#         if len(course_name) > max_length:
#             return course_name[:max_length-3] + '...'
#         else:
#             return course_name
        
#     def hit_count(self, obj):
#         """
#         Custom method to display hit count for each course
#         """
#         return obj.hitcount_set.count() 

#     hit_count.short_description = 'Hit Count'
        
    
#     def action(self, obj):
#         url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
#         url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
#         url_view = reverse('course_detail', args=[obj.id])
#         url_chapter = reverse('course_chapter', args=[obj.id])
        
#         return format_html(
#         '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a> <a href="{}" class="btn btn-secondary btn-sm">View</a>  <a href="{}" class="btn btn-secondary btn-sm">Chapter</a>'.format(url_edit,url_delete,url_view,url_chapter)
#         )
    
    
#     get_course_name_or_host_name.short_description = 'Course/Host Name'
    

#     fieldsets = (
#             ('Basic Information', {
#                 'fields': ('user', 'category', 'type', 'course_name', 'description', 'thumb_image', 'course_video', 'setup_file', 'course_content', 'language', 'paid_course', 'actual_fee', 'discount_fee', 'total_discount', 'generated_coupon', 'coupon_code', 'coupon_percent', 'coupon_applied_by', 'coupon_valid_date', 'coupon_valid_time', 'schedule_date', 'schedule_time')
#             }),
#             ('Other Information', {
#                 'fields': ('url', 'title', 'about_host', 'host_name', 'fees', 'wishlist', 'hide', 'approved')
#             }),
#         )


class CourseAdmin(admin.ModelAdmin):
    list_display = ('get_course_name_or_host_name', 'type', 'hit_count', 'created_at', 'approved', 'action')  
    search_fields = ('title', 'description') 
    list_display_links = None 
    list_per_page = 5
    
    def get_course_name_or_host_name(self, obj):
        """
        Custom method to display either 'course_name' or 'host_name' with ellipsis if too long
        """
        course_name = obj.course_name if obj.course_name else obj.host_name
        max_length = 25
        if len(course_name) > max_length:
            return course_name[:max_length-3] + '...'
        else:
            return course_name
        
    def hit_count(self, obj):
        """
        Custom method to display hit count for each course
        """
        return obj.hitcount_set.count() 

    hit_count.short_description = 'Hit Count'
        
    
    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        url_view = reverse('course_detail', args=[obj.id])
        url_chapter = reverse('course_chapter', args=[obj.id])
        
        # Check if there are any chapters associated with the current course
        if Chapter.objects.filter(course=obj).exists():
            # If chapters exist, display the Chapter button
            return format_html(
                '<a href="{}" class="btn btn-warning btn-sm">Edit</a> '
                '<a href="{}" class="btn btn-danger btn-sm">Delete</a> '
                '<a href="{}" class="btn btn-secondary btn-sm">View</a> '
                '<a href="{}" class="btn btn-secondary btn-sm">Chapter</a>'.format(
                    url_edit, url_delete, url_view, url_chapter)
            )
        else:
            # If no chapters exist, exclude the Chapter button
            return format_html(
                '<a href="{}" class="btn btn-warning btn-sm">Edit</a> '
                '<a href="{}" class="btn btn-danger btn-sm">Delete</a> '
                '<a href="{}" class="btn btn-secondary btn-sm">View</a>'.format(
                    url_edit, url_delete, url_view)
            )
    
    
    get_course_name_or_host_name.short_description = 'Course/Host Name'
    

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'user', 'category', 'type', 'course_name', 'description', 'thumb_image', 'course_video',
                'setup_file', 'course_content', 'language', 'paid_course', 'actual_fee', 'discount_fee',
                'total_discount', 'generated_coupon', 'coupon_code', 'coupon_percent', 'coupon_applied_by',
                'coupon_valid_date', 'coupon_valid_time', 'schedule_date', 'schedule_time')
        }),
        ('Other Information', {
            'fields': ('url', 'title', 'about_host', 'host_name', 'fees', 'wishlist', 'hide', 'approved')
        }),
    )


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('get_truncated_chapter_name', 'get_truncated_course', 'hide', "action") 
    search_fields = ('chapter_name', 'course')  
    list_display_links = None 
    list_per_page = 5

    
    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )
    
    def get_truncated_chapter_name(self, obj):
        max_length = 25
        if len(obj.chapter_name) > max_length:
            return obj.chapter_name[:max_length-3] + '...'
        else:
            return obj.chapter_name
    get_truncated_chapter_name.short_description = 'Chapter Name'
    
    def get_truncated_course(self, obj):
        course_name = obj.course.course_name
        max_length = 25
        if len(course_name) > max_length:
            return course_name[:max_length-3] + '...'
        return course_name

    get_truncated_course.short_description = 'Course Name'

    

class TopicAdmin(admin.ModelAdmin):
    list_display = ('get_truncated_topic_name', 'get_truncated_chapter_name', "action") 
    search_fields = ('topic_name', 'chapter') 
    list_display_links = None 
    list_per_page = 5

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )
    
    def get_truncated_topic_name(self, obj):
        max_length = 25
        if len(obj.topic_name) > max_length:
            return obj.topic_name[:max_length-3] + '...'
        return obj.topic_name
    get_truncated_topic_name.short_description = 'Topic Name'
    
    def get_truncated_chapter_name(self, obj):
        chapter_name = obj.chapter.chapter_name
        max_length = 25
        if len(chapter_name) > max_length:
            return chapter_name[:max_length-3] + '...'
        return chapter_name
    get_truncated_chapter_name.short_description = 'Chapter Name'


class PurchasedCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'get_course_type', 'created_at', 'valid_date', 'action') 
    search_fields = ('course__course_name', 'user__username')
    list_per_page = 5  

    def get_course_type(self, obj):
        return obj.course.type if obj.course else ''  

    get_course_type.short_description = 'Course Type' 

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        return format_html(
            '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )
    
 

    
    
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'title', 'action') 
    search_fields = ('category_name', 'title')

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )
      
     
    
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'title', 'action') 
    list_per_page = 5

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )
    

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time','action') 

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )
    


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_type', 'required', 'action') 

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )


class HitCountAdmin(admin.ModelAdmin):
    list_display = ('course', 'action') 

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )
    

class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'progress', 'action') 

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )



class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'action') 

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )



class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', "certificate_image") 
    
    list_per_page = 5

           
# Register the Course model with the custom admin class
admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(PurchasedCourse, PurchasedCourseAdmin)
admin.site.register(CourseCategory,CourseCategoryAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Questions,QuestionsAdmin)
admin.site.register(HitCount,HitCountAdmin)
admin.site.register(TopicProgress,TopicProgressAdmin)
admin.site.register(Language,LanguageAdmin)
admin.site.register(Certificate, CertificateAdmin)

