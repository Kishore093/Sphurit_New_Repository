import uuid
import calendar
from datetime import date
from datetime import datetime
from datetime import datetime as dt
from datetime import timedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django.conf import settings
from django.core.cache import cache
from ckeditor.fields import RichTextField


import os
from django.db.models import Avg
from django.db import models
from core.models import*
from django.urls import reverse
from tinymce.models import HTMLField
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from moviepy.editor import VideoFileClip


import logging
logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    
    def create_user(self, email, mobile, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, mobile, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, mobile, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_Teacher = models.BooleanField(default=False)
    is_Student = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    mobile = models.IntegerField(null=True,blank=True,unique=True)
    profile_image = models.ImageField(upload_to='profile_images',null=True,blank=True)
    plateform = models.CharField(max_length=200,default="Website")
    date_of_birth = models.DateField(null=True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    intrest_area = TaggableManager(blank=True)
    about = models.TextField(null=True,blank=True)
    online_status = models.BooleanField(default=False)
    address = models.TextField(null=True,blank=True)
    gender = models.CharField(max_length=200,null=True,blank=True)
    experience = models.CharField(max_length=200,null=True,blank=True)
    reg_steps = models.IntegerField(default=0)
    youtube_link = models.URLField(max_length=200,null=True,blank=True)
    instagram_link = models.URLField(max_length=200,null=True,blank=True)
    facebook_link = models.URLField(max_length=200,null=True,blank=True)
    twitter_link = models.URLField(max_length=200,null=True,blank=True)
    linkedin_link = models.URLField(max_length=200,null=True,blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile"]

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = "Users"
    
    def __str__(self):
        return self.email
    
    @property
    def image_url(self):
        try:
            return self.profile_image.url
        except ValueError:
            return ""

    @property
    def full_name(self):
        "Returns the person's full name."
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name and not self.last_name:
            return f"{self.first_name}"
        elif not self.first_name and self.last_name:
            return f"{self.last_name}"
        else:
            return f"{self.email}"
    
    @property
    def user_subscription(self):
        try:
            um = UserMembership.objects.get(user=self)
            return Subscription.objects.filter(user_membership=um).order_by('-updated_at')[0]
        except:
            return None

@receiver(post_save, sender=CustomUser)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        if instance.is_Teacher:
            Wallet.objects.create(user=instance)

class Wallet(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, related_name="wallet", on_delete=models.CASCADE, null=True)
    balance = models.DecimalField(_("balance"), default=0.0, max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Banks(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, related_name="user_banks", on_delete=models.CASCADE, null=True)
    account_name = models.CharField(_("account name"), max_length=250)
    account_number = models.CharField(_("account number"), max_length=100)
    bank_name = models.CharField(_("bank"), max_length=100)
    ifsc_code = models.CharField(_("IFSC Code"), max_length=100)
    phone_number = models.CharField(_("phone number"), max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WalletTransaction(models.Model):
    class STATUS(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SUCCESS = 'success', _('Success')
        CANCEL = 'cancel', _('Cancel')
        DECLINE = 'decline', _('Decline')
        FAIL = 'fail', _('Fail')

    class TransactionType(models.TextChoices):
        PAYOUT_WALLET = 'payout', _('Payout Wallet')
        DEBIT_WALLET = 'debit', _('Debit Wallet')
        CREDIT_WALLET = 'credit', _('Credit Wallet')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(_("transaction id"), max_length=500,null=True,blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS.choices, default=STATUS.PENDING)
    transaction_type = models.CharField(max_length=200, default=TransactionType.PAYOUT_WALLET, choices=TransactionType.choices)
    wallet = models.ForeignKey(Wallet, related_name="wallet_transactions", on_delete=models.CASCADE, null=True)
    bank = models.ForeignKey(Banks, related_name="bank_transactions", on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(_("amount"), max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

coupon_type = (('Percent', 'Percent'),('Price', 'Price'))
class Coupon(models.Model):
    code = models.CharField(max_length=500)
    type = models.CharField(max_length=100, choices=coupon_type, default="Percent")
    rate = models.IntegerField()
    expire_date = models.DateField(null=True,blank=True)
    description = models.TextField()
    terms = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code +"->"+ self.type


@receiver(post_save, sender=CustomUser)
def create_cart(sender, instance, created, **kwargs):
    if created:
        if instance.is_Student:
            Cart.objects.create(user=instance)

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name="user_cart")
    coupon = models.OneToOneField(Coupon, on_delete=models.SET_NULL,related_name="cart_coupon",null=True,blank=True)

    def __str__(self):
        return f"Cart for {self.user.full_name}"
    
    @property
    def coupon_applied(self):
        if self.coupon:
            cart_items = self.cart_items.all()
            total = sum(item.course.discount_fee * item.quantity for item in cart_items)
            if self.coupon.type == "Price":
                return float(self.coupon.rate)
            elif self.coupon.type == "Percent":
                return float(total*self.coupon.rate / 100)
        else:
            total = 0.0
            cart_items = self.cart_items.all()
            for item in cart_items:
                if item.course.coupon_applied_by.contains(self.user):
                    total = total + float(item.course.discount_fee*item.course.coupon_percent / 100)
            return total
    
    @property
    def cart_total(self):
        if self.coupon:
            cart_items = self.cart_items.all()
            total = sum(item.course.discount_fee * item.quantity for item in cart_items)
            if self.coupon.type == "Price":
                return total - self.coupon.rate
            elif self.coupon.type == "Percent":
                return total - (total*self.coupon.rate) / 100
            else:
                return total
        else:
            total = 0.0
            cart_items = self.cart_items.all()
            for item in cart_items:
                if item.course.coupon_applied_by.contains(self.user):
                    total = total + (float(item.course.discount_fee) - float(item.course.discount_fee*item.course.coupon_percent / 100))
                else:
                    total = total+item.course.discount_fee
            return total



class Education(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user_educations", on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=1000,blank=True,null=True)
    institution_address = models.CharField(max_length=1000,blank=True,null=True)
    subject = models.CharField(max_length=500,blank=True,null=True)
    grade = models.CharField(max_length=500,blank=True,null=True)
    year = models.CharField(max_length=500,blank=True,null=True)

class UserKYC(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user_kycs", on_delete=models.CASCADE)
    kyc_name = models.CharField(max_length=500,blank=True,null=True)
    kyc_doc_number = models.CharField(max_length=500,blank=True,null=True)
    kyc_image_front = models.ImageField(upload_to="kyc_doc",blank=True,null=True)
    kyc_image_back = models.ImageField(upload_to="kyc_doc",blank=True,null=True)
    linked_number = models.CharField(max_length=500,blank=True,null=True)
    

# Membership
class Membership(models.Model):
    MEMBERSHIP_CHOICES = (
        ('Enterprise', 'Enterprise'),
        ('Advanced', 'Advanced'),
        ('Basic', 'Basic'),
        ('Free', 'Free')
    )
    PERIOD_DURATION = (
        ('Days', 'Days'),
        ('Week', 'Week'),
        ('Months', 'Months'),
    )
    
    image = models.ImageField(upload_to='membership',null=True,blank=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
    title = models.CharField(max_length=500,null=True,blank=True)
    duration = models.PositiveIntegerField(default=7)
    duration_period = models.CharField(max_length=100, default='Days', choices=PERIOD_DURATION)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    slug = models.SlugField(null=True, blank=True)
    description = HTMLField()

    def __str__(self):
        return self.membership_type

# User Payment History
class PayHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    paystack_charge_id = models.CharField(max_length=100, default='', blank=True)
    paystack_access_code = models.CharField(max_length=100, default='', blank=True)
    payment_for = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name

class UserMembership(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
    reference_code = models.CharField(max_length=100, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.full_name

@receiver(post_save, sender=UserMembership)
def create_subscription(sender, instance, *args, **kwargs):
    # Definir a função add_months aqui
    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        # Convert to date object (Converta para objeto date)
        return datetime(year, month, day).date()

    try:
        subscription = Subscription.objects.get(user_membership=instance)

        if instance.membership.duration_period == 'Months':
            # Calculate new expiration date taking into account months
            # (Calcule a nova data de validade levando em consideração os meses)
            new_expiration_date = add_months(
                datetime.now().date(), instance.membership.duration)
        else:
            # Calculate new expiration date for other duration periods (Days, Weeks)
            # Calcular nova data de vencimento para outros períodos de duração (dias, semanas)
            new_expiration_date = datetime.now().date(
            ) + timedelta(days=instance.membership.duration)

        subscription.expires_in = new_expiration_date
        subscription.save()
    except Subscription.DoesNotExist:
        if instance.membership.duration_period == 'Months':
            new_expiration_date = add_months(
                datetime.now().date(), instance.membership.duration)
        else:
            new_expiration_date = datetime.now().date(
            ) + timedelta(days=instance.membership.duration)

        Subscription.objects.create(
            user_membership=instance, expires_in=new_expiration_date)

# User Subscription
class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE, default=None)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_membership.user.full_name

class SupportQuery(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    mobile = models.CharField(max_length=500)
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CategoryRequest(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user_category_requests", on_delete=models.SET_NULL, null=True)
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TermsAndCondition(models.Model):
    name = models.CharField(max_length=500)
    content = RichTextField()
    image = models.ImageField(upload_to='terms_images/', blank=True, null=True)

    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name_plural = "Terms And Condition"

class PrivacyPolicy(models.Model):
    name = models.CharField(max_length=500)
    content = RichTextField()
    image = models.ImageField(upload_to='privacy_images/', blank=True, null=True)

    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name_plural = "Privacy Policy"


class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='about_us_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
    

class Testimonial(models.Model):
    title = models.CharField(max_length=300)
    sub_title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to="testimonials")
    created_at = models.DateTimeField(auto_now_add=True)

class Slider(models.Model):
    title_1 = models.CharField(max_length=30,null=True,blank=True)
    title_2 = models.CharField(max_length=80,null=True,blank=True)
    title_3 = models.CharField(max_length=25,null=True,blank=True)
    title_4 = models.CharField(max_length=90,null=True,blank=True)
    title_5 = models.CharField(max_length=500,null=True,blank=True)
    type = models.CharField(max_length=500)
    image = models.ImageField(upload_to='slider')
    created_at = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    user = models.ForeignKey(CustomUser, related_name="invoice_num", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=30)

""" Notification related manager and model """
class NotificationQuerySet(models.QuerySet):
    """Custom QuerySet for Notification model"""

    def update(self, *args, **kwargs):
        """Override update to ensure cache is invalidated on very call."""
        super().update(*args, **kwargs)
        user_pks = set(self.select_related("user").values_list('user__pk', flat=True))
        for user_pk in user_pks:
            NotificationManager.invalidate_user_notification_cache(user_pk)

class NotificationManager(models.Manager):

    USER_NOTIFICATION_COUNT_PREFIX = 'USER_NOTIFICATION_COUNT'
    USER_NOTIFICATION_COUNT_CACHE_DURATION = 86_400

    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def notify_user(
        self, user: object, title: str, message: str = None, level: str = 'info'
    ) -> object:
        """Sends a new notification to user. Returns newly created notification object.
        """
        max_notifications = self._max_notifications_per_user()
        if self.filter(user=user).count() >= max_notifications:
            to_be_deleted_qs = self.filter(user=user).order_by(
                "-timestamp"
            )[max_notifications - 1:]
            for notification in to_be_deleted_qs:
                notification.delete()

        if not message:
            message = title

        if level not in self.model.Level:
            level = self.model.Level.INFO
        obj = self.create(user=user, title=title, message=message, level=level)
        logger.info("Created notification %s", obj)
        return obj

    def _max_notifications_per_user(self) -> int:
        """Maximum number of notifications allowed per user."""
        max_notifications = getattr(
            settings,
            "NOTIFICATIONS_MAX_PER_USER",
            self.model.NOTIFICATIONS_MAX_PER_USER_DEFAULT
        )
        try:
            max_notifications = int(max_notifications)
        except ValueError:
            max_notifications = None
        if max_notifications is None or max_notifications < 0:
            logger.warning(
                "NOTIFICATIONS_MAX_PER_USER setting is invalid. Using default."
            )
            max_notifications = self.model.NOTIFICATIONS_MAX_PER_USER_DEFAULT
        return max_notifications

    def user_unread_count(self, user_pk: int) -> int:
        """returns the cached unread count for a user given by user PK

        Will return -1 if user can not be found
        """
        cache_key = self._user_notification_cache_key(user_pk)
        unread_count = cache.get(key=cache_key)
        if not unread_count:
            try:
                user = CustomUser.objects.get(pk=user_pk)
            except CustomUser.DoesNotExist:
                unread_count = -1
            else:
                logger.debug(
                    'Updating notification cache for user with pk %s', user_pk
                )
                unread_count = user.notification_set.filter(viewed=False).count()
                cache.set(
                    key=cache_key,
                    value=unread_count,
                    timeout=self.USER_NOTIFICATION_COUNT_CACHE_DURATION
                )
        else:
            logger.debug(
                'Returning notification count from cache for user with pk %s', user_pk
            )

        return unread_count

    @classmethod
    def invalidate_user_notification_cache(cls, user_pk: int) -> None:
        cache.delete(key=cls._user_notification_cache_key(user_pk))
        logger.debug('Invalided notification cache for user with pk %s', user_pk)

    @classmethod
    def _user_notification_cache_key(cls, user_pk: int) -> str:
        return f'{cls.USER_NOTIFICATION_COUNT_PREFIX}_{user_pk}'

class Notification(models.Model):
    """Notification to a user within Auth"""

    NOTIFICATIONS_MAX_PER_USER_DEFAULT = 50
    NOTIFICATIONS_REFRESH_TIME_DEFAULT = 30

    class Level(models.TextChoices):
        """A notification level."""

        DANGER = 'danger', _('danger')  #:
        WARNING = 'warning', _('warning')  #:
        INFO = 'info', _('info')  #:
        SUCCESS = 'success', _('success')  #:

        @classmethod
        def from_old_name(cls, name: str) -> object:
            """Map old name to enum.

            Raises ValueError for invalid names.
            """
            name_map = {
                "CRITICAL": cls.DANGER,
                "ERROR": cls.DANGER,
                "WARN": cls.WARNING,
                "INFO": cls.INFO,
                "DEBUG": cls.SUCCESS,
            }
            try:
                return name_map[name]
            except KeyError:
                raise ValueError(f"Unknown name: {name}") from None

    # LEVEL_CHOICES = (
    #     ('danger', 'CRITICAL'),
    #     ('danger', 'ERROR'),
    #     ('warning', 'WARN'),
    #     ('info', 'INFO'),
    #     ('success', 'DEBUG'),
    # )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    level = models.CharField(choices=Level.choices, max_length=10, default=Level.INFO)
    title = models.CharField(max_length=254)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    viewed = models.BooleanField(default=False, db_index=True)

    objects = NotificationManager()

    def __str__(self) -> str:
        return f"{self.user}: {self.title}: {self.level}"

    def save(self, *args, **kwargs):
        # overriden save to ensure cache is invaidated on very call
        super().save(*args, **kwargs)
        Notification.objects.invalidate_user_notification_cache(self.user.pk)

    def delete(self, *args, **kwargs):
        # overriden delete to ensure cache is invaidated on very call
        super().delete(*args, **kwargs)
        Notification.objects.invalidate_user_notification_cache(self.user.pk)

    def mark_viewed(self) -> None:
        """Mark notification as viewed."""
        logger.info("Marking notification as viewed: %s" % self)
        self.viewed = True
        self.save()

    def set_level(self, level_name: str) -> None:
        """Set notification level according to old level name, e.g. 'CRITICAL'.

        Raises ValueError on invalid level names.
        """
        self.level = self.Level.from_old_name(level_name)
        self.save()



CourseType = (('Pre Recorded', 'Pre Recorded'),('Live', 'Live'),('Hybrid','Hybrid'),)

class CourseCategory(models.Model):
    category_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length = 500,editable=True, null = True, blank = True)

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        self.slug = self.category_name.replace(" ","_")
        super(CourseCategory, self).save(*args, **kwargs)

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):    
    user = models.ForeignKey(CustomUser,related_name='user_course',on_delete=models.CASCADE,default=False)
    category = models.ForeignKey(CourseCategory,related_name='course_category',on_delete=models.CASCADE)
    type = models.CharField(max_length=200,default=False)
    course_name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField()
    thumb_image = models.ImageField(upload_to='course_file',null=True,blank=True)
    course_video = models.FileField(upload_to="course_file",null=True,blank=True)
    setup_file = models.FileField(upload_to="course_setup",null=True,blank=True)
    course_content = models.FileField(upload_to="course_content",null=True,blank=True)
    language = models.ManyToManyField(Language,blank=True)
    paid_course = models.BooleanField(default=False)
    actual_fee = models.FloatField(default=0.0,null=True,blank=True)
    discount_fee = models.FloatField(default=0.0,null=True,blank=True)
    total_discount = models.CharField(max_length=100,default=0.0,null=True,blank=True)
    generated_coupon = models.BooleanField(default=False,null=True,blank=True)
    coupon_code = models.CharField(max_length=100,null=True,blank=True)
    coupon_percent = models.FloatField(null=True,blank=True,default=0.0)
    coupon_applied_by = models.ManyToManyField(CustomUser, related_name="coupon_applied_user",blank=True)
    coupon_valid_date = models.DateField(null=True,blank=True)
    coupon_valid_time = models.TimeField(null=True,blank=True)
    schedule_date = models.DateField(null=True,blank=True)
    schedule_time = models.TimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hide = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    wishlist = models.ManyToManyField(CustomUser, related_name="wishlists",blank=True)

    url = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    about_host = models.TextField(null=True,blank=True)
    host_name = models.CharField(max_length=200,null=True,blank=True)
    fees = models.IntegerField(null=True, blank=True)
    


    def __str__(self):
        if self.course_name:
            return self.course_name
        elif self.host_name:
            return self.host_name
        else:
            return "Course object"
    
    def averagereview(self):
        review = Feedback.objects.filter(course=self).aggregate(avarage=Avg('rating'))
        avg=0
        if review["avarage"] is not None:
            avg=float(review["avarage"])
        return round(avg,1)
    
    @property
    def get_hit_count(self):
        return HitCount.objects.filter(course=self).count()
    
    @property
    def select_language(self):
        return ', '.join([language.name for language in self.language.all()])
    
    @property
    def video_url(self):
        try:
            return self.course_video.url
        except ValueError:
            return ""
        
    @property
    def img_url(self):
        try:
            return self.thumb_image.url
        except ValueError:
            return ""
    
    @property
    def setup_url(self):
        try:
            return self.setup_file.url
        except ValueError:
            return ""
        
    @property
    def content_url(self):
        try:
            return self.course_content.url
        except ValueError:
            return ""
        

    
    @property
    def img_url(self):
        try:
            return self.thumb_image.url
        except ValueError:
            return ""
        
       
class CourseProgress(models.Model):
    user = models.ForeignKey(CustomUser,related_name='user_course_progress',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='course_progress', on_delete=models.CASCADE)
    progress = models.FloatField(null=True,blank=True,default=0.0)

    def __str__(self):
        return f'{self.user.full_name} => {self.course.course_name} => {self.progress}'

class HitCount(models.Model):
    ip_address = models.GenericIPAddressField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
# , related_name='hitcount_set'
    def __str__(self):
        return f'{self.ip_address} => {self.course.course_name}'

class Chapter(models.Model):
    course = models.ForeignKey(Course,related_name='chapter_course',on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=200)
    description = HTMLField()
    hide = models.BooleanField(default=True)

class ChapterProgress(models.Model):
    user = models.ForeignKey(CustomUser,related_name='user_chapter_progress',on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter,related_name='chapter_progress', on_delete=models.CASCADE)
    progress = models.FloatField(null=True,blank=True,default=0.0)

    def __str__(self):
        return f'{self.user.full_name} => {self.chapter.chapter_name} => {self.progress}'

class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='topic_chapter', on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=200)
    description = models.TextField()
    topic_video = models.FileField(upload_to='topic_resources', null=True, blank=True)
    topic_video_thumbnail = models.ImageField(upload_to='topic_thumbnails', null=True, blank=True)

    @property
    def video_url(self):
        try:
            return self.topic_video.url
        except ValueError:
            return ""
    
    @property
    def thumbnail_url(self):
        try:
            return self.topic_video_thumbnail.url
        except ValueError:
            return ""

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.topic_video and not self.topic_video_thumbnail:
            self.generate_video_thumbnail()

    def generate_video_thumbnail(self):
        video_path = self.topic_video.path
        thumbnail_path = f"{video_path}_thumbnail.jpg"

        with VideoFileClip(video_path) as video:
            frame = video.get_frame(0)
            thumbnail = Image.fromarray(frame)
            thumbnail_io = BytesIO()
            thumbnail.save(thumbnail_io, format='JPEG')
            thumbnail_file = InMemoryUploadedFile(
                thumbnail_io, None, f"{self.topic_video.name.split('.')[0]}_thumbnail.jpg", 'image/jpeg',
                thumbnail_io.tell, None
            )
            self.topic_video_thumbnail.save(thumbnail_file.name, thumbnail_file)

    class Meta:
        ordering = ['id']

class TopicProgress(models.Model):
    user = models.ForeignKey(CustomUser,related_name='user_topic_progress',on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic,related_name='topic_progress', on_delete=models.CASCADE)
    progress = models.FloatField(null=True,blank=True,default=0.0)

    def __str__(self):
        return f'{self.user.full_name} => {self.topic.topic_name} => {self.progress}'

class CourseQuery(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500)
    mobile = models.CharField(max_length=500)
    course = models.ForeignKey(Course,related_name='course_query',on_delete=models.CASCADE)
    query = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser,related_name='user_feedbacks',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='course_feedbacks',on_delete=models.CASCADE)
    title = models.CharField(max_length=500,blank=True,null=True)
    description = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating']

class PurchasedCourse(models.Model):
    user = models.ForeignKey(CustomUser,related_name='user_purchased',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='course_purchased',on_delete=models.CASCADE)
    plateform = models.CharField(max_length=200,default="Website")
    order_id = models.CharField(max_length=200,)
    valid_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    @property
    def get_course_progress(self):
        cp = CourseProgress.objects.get(user=self.user,course=self.course)
        return cp.progress


@receiver(post_save, sender=PurchasedCourse)
def create_course_progress(sender, instance, created, **kwargs):
    if created:
        CourseProgress.objects.create(user=instance.user,course=instance.course)
        for ch in Chapter.objects.filter(course=instance.course):
            ChapterProgress.objects.create(chapter=ch,user=instance.user)
            for t in Topic.objects.filter(chapter=ch):
                TopicProgress.objects.create(topic=t,user=instance.user)


# class Wishlist(models.Model):
#     user = models.ForeignKey(CustomUser,related_name='user_wishlist',on_delete=models.CASCADE)
#     course = models.ForeignKey(Course,related_name='course_wishlist',on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user)
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events

class Event(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user_events",on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = EventManager()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="#"> {self.title} </a>'
        # return f'<a href="{url}"> {self.title} </a>'

# custome form models
class Choices(models.Model):
    choice = models.CharField(max_length=5000)
    is_answer = models.BooleanField(default=False)

class Questions(models.Model):
    question = models.CharField(max_length= 10000)
    question_type = models.CharField(max_length=20)
    required = models.BooleanField(default= False)
    answer_key = models.CharField(max_length = 5000, blank = True)
    score = models.IntegerField(blank = True, default=0)
    feedback = models.CharField(max_length = 5000, null = True)
    choices = models.ManyToManyField(Choices, related_name = "choices")

    def __str__(self):
        return self.question

class Answer(models.Model):
    answer = models.CharField(max_length=5000,null=True,blank=True)
    file = models.FileField(upload_to='answers',null=True,blank=True)
    answer_to = models.ForeignKey(Questions, on_delete = models.CASCADE ,related_name = "answer_to")

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
    
    
    
    



class Form(models.Model):
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=10000, blank = True)
    creator = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = "creator")
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE, related_name = "topic_assignments")
    background_color = models.CharField(max_length=20, default = "#d9efed")
    text_color = models.CharField(max_length=20, default="#272124")
    collect_email = models.BooleanField(default=False)
    authenticated_responder = models.BooleanField(default = False)
    edit_after_submit = models.BooleanField(default=False)
    confirmation_message = models.CharField(max_length = 10000, default = "Your response has been recorded.")
    is_quiz = models.BooleanField(default=False)
    allow_view_score = models.BooleanField(default= True)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    questions = models.ManyToManyField(Questions, related_name = "questions")

class Responses(models.Model):
    response_code = models.CharField(max_length=20)
    response_to = models.ForeignKey(Form, on_delete = models.CASCADE, related_name = "response_to")
    responder_ip = models.CharField(max_length=30)
    responder = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = "responder", blank = True, null = True)
    responder_email = models.EmailField(blank = True)
    response = models.ManyToManyField(Answer, related_name = "response")

class Certificate(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user_certificate", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="course_certificate", on_delete=models.CASCADE,default=False)
    certificate_image = models.FileField(upload_to='certificates')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name
    


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name="cart_items", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="cart_courses", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_price(self):
        return int(self.course.discount_fee)* self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.course.course_name}"


