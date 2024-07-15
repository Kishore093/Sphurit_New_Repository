
from django.contrib.admin.decorators import register
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.contrib import admin 
from .models import *
from teacher.models import*
admin.site.unregister(Group)


class CustomUserAdmin(UserAdmin):    
    model = CustomUser
    list_display = ("full_name","email","mobile","plateform","Teacher","Student","Active","action")
    list_filter = ()
    list_display_links = None 
    list_per_page = 5
    
    fieldsets = (
        ("Basic Informations", {"fields": ("email","mobile","first_name","last_name","gender","date_of_birth",)}),
        ("Other Informations", {"fields": ("plateform","profile_image","intrest_area","experience","address","about","date_joined",)}),
        ("Status", {"fields": ("is_active","is_Teacher","is_Student","online_status",)}),
        ("Social Links", {"fields": ("youtube_link","instagram_link","facebook_link","twitter_link","linkedin_link",)}),
        ("Permissions", {"fields": ("is_staff", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        ("Basic Informations", {"fields": ("email","mobile","first_name","last_name","gender","date_of_birth",)}),
        ("Other Informations", {"fields": ("plateform","profile_image","intrest_area","experience","address","about",)}),
        ("Status", {"fields": ("is_active","is_Teacher","is_Student","online_status",)}),
        ("Social Links", {"fields": ("youtube_link","instagram_link","facebook_link","twitter_link","linkedin_link",)}),
        ("Permissions", {"fields": ("is_staff", "groups", "user_permissions")}),
    )
    
    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_view = reverse('super_admin_purchased_courses', args=[obj.id])

        if obj.is_Student and obj.user_purchased.exists():  
            return format_html(
                '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a> <a href="{}" class="btn btn-secondary btn-sm">Course</a>'.format(url_edit,url_delete,url_view)
            )
        elif obj.is_Student:  
            return format_html(
                '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
            )
        else: 
            return format_html(
                '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
            )
    
    def Teacher(self, obj):
        return obj.is_Teacher

    def Student(self, obj):
        return obj.is_Student

    def Active(self, obj):
        return obj.is_active

    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = ('date_joined',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(AboutUs)
# admin.site.register(Coupon)

# admin.site.register(Membership)
# admin.site.register(PayHistory)
# admin.site.register(UserMembership)
# admin.site.register(Subscription)


# admin.site.register(Cart)
# admin.site.register(CartItem)
# admin.site.register(WalletTransaction)
# admin.site.register(Banks)
# admin.site.register(Education)
# admin.site.register(UserKYC)
# admin.site.register(Notification)
admin.site.register(CategoryRequest)
admin.site.register(TermsAndCondition)
admin.site.register(PrivacyPolicy)
admin.site.register(Slider)
# admin.site.register(Testimonial)


# class WalletApp(admin.app):
#    label = "Wallets"

# admin.add_app(WalletApp)

@register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user","balance","updated_at")



class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ("user","membership","created_at","updated_at","action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )



class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user_membership","expires_in","active", "created_at","updated_at","action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )



class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart","course","quantity", "action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )




class CartAdmin(admin.ModelAdmin):
    list_display = ("user","coupon", "action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )




class CouponAdmin(admin.ModelAdmin):
    list_display = ("code","type","rate","expire_date", "action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )



class  PayHistoryAdmin(admin.ModelAdmin):
    list_display = ("user","paystack_access_code","amount","date","action")
    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )



class  BanksAdmin(admin.ModelAdmin):
    list_display = ("user","account_name","account_number","bank_name")



class  EducationAdmin(admin.ModelAdmin):
    list_display = ("user","institution_name","institution_address","subject","grade","year","action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )
    



class  MembershipAdmin(admin.ModelAdmin):
    list_display = ("membership_type","title","duration","duration_period","price","action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )



class  NotificationAdmin(admin.ModelAdmin):
    list_display = ("user","level","title","action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )




class  TestimonialAdmin(admin.ModelAdmin):
    list_display = ("title","sub_title","created_at","action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )




class  UserKYCAdmin(admin.ModelAdmin):
    list_display = ("user","kyc_name","linked_number","action")

    def action(self, obj):
        url_edit = reverse('admin:%s_%s_change' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        url_delete = reverse('admin:%s_%s_delete' % (obj._meta.app_label,obj._meta.model_name),args=[obj.id])
        
        
        return format_html(
        '<a href="{}" class="btn btn-warning btn-sm">Edit</a> <a href="{}" class="btn btn-danger btn-sm">Delete</a>'.format(url_edit,url_delete)
        )


class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ("status", "transaction_type", "user_name", "bank_name", "amount", "created_at", "action")

    def user_name(self, obj):
        return obj.wallet.user.full_name
    user_name.short_description = 'User'

    def bank_name(self, obj):
        return obj.bank.bank_name
    bank_name.short_description = 'Bank'

    def action(self, obj):
        url_edit  = reverse('customuser_customuser_change', args=[obj.wallet.user.pk])
        return format_html('<a href="{}" class="btn btn-warning btn-sm">View User</a>', url_edit )
    action.short_description = 'Action'


admin.site.register(UserMembership, UserMembershipAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(PayHistory, PayHistoryAdmin)
admin.site.register(Banks, BanksAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(UserKYC, UserKYCAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ("timestamp", "_main", "_state", "title", "level", "viewed")
#     list_select_related = ("user", "user__profile__main_character", "user__profile__state")
#     list_filter = (
#         "level",
#         "timestamp",
#         "user__profile__state",
#         ('user__profile__main_character', admin.RelatedOnlyFieldListFilter),
#     )
#     ordering = ("-timestamp", )
#     search_fields = ["user__username", "user__profile__main_character__character_name"]

#     @admin.display(
#         ordering="user__profile__main_character__character_name"
#     )
#     def _main(self, obj):
#         try:
#             return obj.user.profile.main_character
#         except AttributeError:
#             return obj.user


#     @admin.display(
#         ordering="user__profile__state__name"
#     )
#     def _state(self, obj):
#         return obj.user.profile.state


#     def has_change_permission(self, request, obj=None):
#         return False

#     def has_add_permission(self, request) -> bool:
#         return False

