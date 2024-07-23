# import os
# from django.db.models import Avg
# from django.db import models
# from core.models import*
# from django.urls import reverse
# from tinymce.models import HTMLField
# from django.db import models
# from PIL import Image
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from moviepy.editor import VideoFileClip

# CourseType = (('Pre Recorded', 'Pre Recorded'),('Live', 'Live'),('Hybrid','Hybrid'),)

# class CourseCategory(models.Model):
#     category_name = models.CharField(max_length=200)
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     slug = models.SlugField(max_length = 500,editable=True, null = True, blank = True)

#     def __str__(self):
#         return self.category_name
    
#     def save(self, *args, **kwargs):
#         self.slug = self.category_name.replace(" ","_")
#         super(CourseCategory, self).save(*args, **kwargs)

# class Language(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Course(models.Model):    
#     user = models.ForeignKey(CustomUser,related_name='user_course',on_delete=models.CASCADE,default=False)
#     category = models.ForeignKey(CourseCategory,related_name='course_category',on_delete=models.CASCADE)
#     type = models.CharField(max_length=200,default=False)
#     course_name = models.CharField(max_length=200,null=True,blank=True)
#     description = models.TextField()
#     thumb_image = models.ImageField(upload_to='course_file',null=True,blank=True)
#     course_video = models.FileField(upload_to="course_file",null=True,blank=True)
#     setup_file = models.FileField(upload_to="course_setup",null=True,blank=True)
#     course_content = models.FileField(upload_to="course_content",null=True,blank=True)
#     language = models.ManyToManyField(Language,blank=True)
#     paid_course = models.BooleanField(default=False)
#     actual_fee = models.FloatField(default=0.0,null=True,blank=True)
#     discount_fee = models.FloatField(default=0.0,null=True,blank=True)
#     total_discount = models.CharField(max_length=100,default=0.0,null=True,blank=True)
#     generated_coupon = models.BooleanField(default=False,null=True,blank=True)
#     coupon_code = models.CharField(max_length=100,null=True,blank=True)
#     coupon_percent = models.FloatField(null=True,blank=True,default=0.0)
#     coupon_applied_by = models.ManyToManyField(CustomUser, related_name="coupon_applied_user",blank=True)
#     coupon_valid_date = models.DateField(null=True,blank=True)
#     coupon_valid_time = models.TimeField(null=True,blank=True)
#     schedule_date = models.DateField(null=True,blank=True)
#     schedule_time = models.TimeField(null=True,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     hide = models.BooleanField(default=False)
#     approved = models.BooleanField(default=False)
#     wishlist = models.ManyToManyField(CustomUser, related_name="wishlists",blank=True)

#     url = models.URLField(null=True, blank=True)
#     title = models.CharField(max_length=200,null=True,blank=True)
#     about_host = models.TextField(null=True,blank=True)
#     host_name = models.CharField(max_length=200,null=True,blank=True)
#     fees = models.IntegerField(null=True, blank=True)
    


#     def __str__(self):
#         if self.course_name:
#             return self.course_name
#         elif self.host_name:
#             return self.host_name
#         else:
#             return "Course object"
    
#     def averagereview(self):
#         review = Feedback.objects.filter(course=self).aggregate(avarage=Avg('rating'))
#         avg=0
#         if review["avarage"] is not None:
#             avg=float(review["avarage"])
#         return round(avg,1)
    
#     @property
#     def get_hit_count(self):
#         return HitCount.objects.filter(course=self).count()
    
#     @property
#     def select_language(self):
#         return ', '.join([language.name for language in self.language.all()])
    
#     @property
#     def video_url(self):
#         try:
#             return self.course_video.url
#         except ValueError:
#             return ""
        
#     @property
#     def img_url(self):
#         try:
#             return self.thumb_image.url
#         except ValueError:
#             return ""
    
#     @property
#     def setup_url(self):
#         try:
#             return self.setup_file.url
#         except ValueError:
#             return ""
        
#     @property
#     def content_url(self):
#         try:
#             return self.course_content.url
#         except ValueError:
#             return ""
        

    
#     @property
#     def img_url(self):
#         try:
#             return self.thumb_image.url
#         except ValueError:
#             return ""
        
       
# class CourseProgress(models.Model):
#     user = models.ForeignKey(CustomUser,related_name='user_course_progress',on_delete=models.CASCADE)
#     course = models.ForeignKey(Course,related_name='course_progress', on_delete=models.CASCADE)
#     progress = models.FloatField(null=True,blank=True,default=0.0)

#     def __str__(self):
#         return f'{self.user.full_name} => {self.course.course_name} => {self.progress}'

# class HitCount(models.Model):
#     ip_address = models.GenericIPAddressField()
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
# # , related_name='hitcount_set'
#     def __str__(self):
#         return f'{self.ip_address} => {self.course.course_name}'

# class Chapter(models.Model):
#     course = models.ForeignKey(Course,related_name='chapter_course',on_delete=models.CASCADE)
#     chapter_name = models.CharField(max_length=200)
#     description = HTMLField()
#     hide = models.BooleanField(default=True)

# class ChapterProgress(models.Model):
#     user = models.ForeignKey(CustomUser,related_name='user_chapter_progress',on_delete=models.CASCADE)
#     chapter = models.ForeignKey(Chapter,related_name='chapter_progress', on_delete=models.CASCADE)
#     progress = models.FloatField(null=True,blank=True,default=0.0)

#     def __str__(self):
#         return f'{self.user.full_name} => {self.chapter.chapter_name} => {self.progress}'

# class Topic(models.Model):
#     chapter = models.ForeignKey(Chapter, related_name='topic_chapter', on_delete=models.CASCADE)
#     topic_name = models.CharField(max_length=200)
#     description = models.TextField()
#     topic_video = models.FileField(upload_to='topic_resources', null=True, blank=True)
#     topic_video_thumbnail = models.ImageField(upload_to='topic_thumbnails', null=True, blank=True)

#     @property
#     def video_url(self):
#         try:
#             return self.topic_video.url
#         except ValueError:
#             return ""
    
#     @property
#     def thumbnail_url(self):
#         try:
#             return self.topic_video_thumbnail.url
#         except ValueError:
#             return ""

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         if self.topic_video and not self.topic_video_thumbnail:
#             self.generate_video_thumbnail()

#     def generate_video_thumbnail(self):
#         video_path = self.topic_video.path
#         thumbnail_path = f"{video_path}_thumbnail.jpg"

#         with VideoFileClip(video_path) as video:
#             frame = video.get_frame(0)
#             thumbnail = Image.fromarray(frame)
#             thumbnail_io = BytesIO()
#             thumbnail.save(thumbnail_io, format='JPEG')
#             thumbnail_file = InMemoryUploadedFile(
#                 thumbnail_io, None, f"{self.topic_video.name.split('.')[0]}_thumbnail.jpg", 'image/jpeg',
#                 thumbnail_io.tell, None
#             )
#             self.topic_video_thumbnail.save(thumbnail_file.name, thumbnail_file)

#     class Meta:
#         ordering = ['id']

# class TopicProgress(models.Model):
#     user = models.ForeignKey(CustomUser,related_name='user_topic_progress',on_delete=models.CASCADE)
#     topic = models.ForeignKey(Topic,related_name='topic_progress', on_delete=models.CASCADE)
#     progress = models.FloatField(null=True,blank=True,default=0.0)

#     def __str__(self):
#         return f'{self.user.full_name} => {self.topic.topic_name} => {self.progress}'

# class CourseQuery(models.Model):
#     name = models.CharField(max_length=500)
#     email = models.EmailField(max_length=500)
#     mobile = models.CharField(max_length=500)
#     course = models.ForeignKey(Course,related_name='course_query',on_delete=models.CASCADE)
#     query = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     class Meta:
#         ordering = ['-id']

# class Feedback(models.Model):
#     user = models.ForeignKey(CustomUser,related_name='user_feedbacks',on_delete=models.CASCADE)
#     course = models.ForeignKey(Course,related_name='course_feedbacks',on_delete=models.CASCADE)
#     title = models.CharField(max_length=500,blank=True,null=True)
#     description = models.TextField()
#     rating = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-rating']

# class PurchasedCourse(models.Model):
#     user = models.ForeignKey(CustomUser,related_name='user_purchased',on_delete=models.CASCADE)
#     course = models.ForeignKey(Course,related_name='course_purchased',on_delete=models.CASCADE)
#     plateform = models.CharField(max_length=200,default="Website")
#     order_id = models.CharField(max_length=200,)
#     valid_date = models.DateField(null=True,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    

#     @property
#     def get_course_progress(self):
#         cp = CourseProgress.objects.get(user=self.user,course=self.course)
#         return cp.progress


# @receiver(post_save, sender=PurchasedCourse)
# def create_course_progress(sender, instance, created, **kwargs):
#     if created:
#         CourseProgress.objects.create(user=instance.user,course=instance.course)
#         for ch in Chapter.objects.filter(course=instance.course):
#             ChapterProgress.objects.create(chapter=ch,user=instance.user)
#             for t in Topic.objects.filter(chapter=ch):
#                 TopicProgress.objects.create(topic=t,user=instance.user)


# # class Wishlist(models.Model):
# #     user = models.ForeignKey(CustomUser,related_name='user_wishlist',on_delete=models.CASCADE)
# #     course = models.ForeignKey(Course,related_name='course_wishlist',on_delete=models.CASCADE)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)


# class EventManager(models.Manager):
#     """ Event manager """

#     def get_all_events(self, user):
#         events = Event.objects.filter(user=user)
#         return events

#     def get_running_events(self, user):
#         running_events = Event.objects.filter(
#             user=user,
#             end_time__gte=datetime.now().date(),
#         ).order_by("start_time")
#         return running_events

# class Event(models.Model):
#     user = models.ForeignKey(CustomUser, related_name="user_events",on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()

#     objects = EventManager()

#     @property
#     def get_html_url(self):
#         url = reverse('event_edit', args=(self.id,))
#         return f'<a href="#"> {self.title} </a>'
#         # return f'<a href="{url}"> {self.title} </a>'

# # custome form models
# class Choices(models.Model):
#     choice = models.CharField(max_length=5000)
#     is_answer = models.BooleanField(default=False)

# class Questions(models.Model):
#     question = models.CharField(max_length= 10000)
#     question_type = models.CharField(max_length=20)
#     required = models.BooleanField(default= False)
#     answer_key = models.CharField(max_length = 5000, blank = True)
#     score = models.IntegerField(blank = True, default=0)
#     feedback = models.CharField(max_length = 5000, null = True)
#     choices = models.ManyToManyField(Choices, related_name = "choices")

#     def __str__(self):
#         return self.question

# class Answer(models.Model):
#     answer = models.CharField(max_length=5000,null=True,blank=True)
#     file = models.FileField(upload_to='answers',null=True,blank=True)
#     answer_to = models.ForeignKey(Questions, on_delete = models.CASCADE ,related_name = "answer_to")

#     def extension(self):
#         name, extension = os.path.splitext(self.file.name)
#         return extension

# class Form(models.Model):
#     code = models.CharField(max_length=30)
#     title = models.CharField(max_length=200)
#     description = models.CharField(max_length=10000, blank = True)
#     creator = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = "creator")
#     topic = models.ForeignKey(Topic, on_delete = models.CASCADE, related_name = "topic_assignments")
#     background_color = models.CharField(max_length=20, default = "#d9efed")
#     text_color = models.CharField(max_length=20, default="#272124")
#     collect_email = models.BooleanField(default=False)
#     authenticated_responder = models.BooleanField(default = False)
#     edit_after_submit = models.BooleanField(default=False)
#     confirmation_message = models.CharField(max_length = 10000, default = "Your response has been recorded.")
#     is_quiz = models.BooleanField(default=False)
#     allow_view_score = models.BooleanField(default= True)
#     createdAt = models.DateTimeField(auto_now_add = True)
#     updatedAt = models.DateTimeField(auto_now = True)
#     questions = models.ManyToManyField(Questions, related_name = "questions")

# class Responses(models.Model):
#     response_code = models.CharField(max_length=20)
#     response_to = models.ForeignKey(Form, on_delete = models.CASCADE, related_name = "response_to")
#     responder_ip = models.CharField(max_length=30)
#     responder = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = "responder", blank = True, null = True)
#     responder_email = models.EmailField(blank = True)
#     response = models.ManyToManyField(Answer, related_name = "response")

# class Certificate(models.Model):
#     user = models.ForeignKey(CustomUser, related_name="user_certificate", on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, related_name="course_certificate", on_delete=models.CASCADE,default=False)
#     certificate_image = models.FileField(upload_to='certificates')
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.full_name

