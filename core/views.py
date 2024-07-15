
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.template.loader import get_template
from django.views.generic.list import ListView
from django.contrib.auth import login, logout
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.db.models import Count
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.db import transaction
from teacher.models import*
from .backends import*
from xhtml2pdf import pisa
from .serializer import*
import datetime
import razorpay
import pyotp
import base64
import json
import io
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import redirect


from django.db.models import Sum

# from django.core.exceptions import MultipleObjectsReturned

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Create your views here.
# Time after which OTP will expire
EXPIRY_TIME = 120 # seconds

class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone)
        # return str(phone) + str(datetime.datetime.date(datetime.datetime.now())) + "Some Random Secret Key"


def Home(request):
    most_purchased_course = Course.objects.filter(type='Pre Recorded').annotate(num_purchases=Count('course_purchased')).order_by('-num_purchases')
    testimonial = Testimonial.objects.all()
    slider = Slider.objects.all()
    new_courses = Course.objects.filter(hide=False, approved=True, type='Pre Recorded').order_by('-created_at')[:3]
    most_viewed_courses = Course.objects.annotate(hit_count=Count('hitcount')).order_by('-hit_count')[:3]
    
    #live_courses = Course.objects.filter(hide=False, approved=True, host_name__isnull=False).order_by('-created_at')[:3]
    live_courses = Course.objects.filter(
        hide=False,
        approved=True,
        host_name__isnull=False,
        schedule_date__gte=timezone.now()  # Exclude courses with schedule dates in the past
    ).order_by('-created_at')[:3]



    for course in live_courses:
       
        current_datetime = timezone.now()
        scheduled_datetime = timezone.make_aware(
            timezone.datetime.combine(course.schedule_date, course.schedule_time),
            timezone.get_current_timezone()
        )
        if not current_datetime.tzinfo:
            current_datetime = timezone.make_aware(current_datetime, timezone.get_current_timezone())
        time_left = scheduled_datetime - current_datetime
        course.time_left = time_left.total_seconds()
            
            
    if request.user.is_authenticated:
        if request.user.is_Teacher:
            teacher_courses = Course.objects.filter(user=request.user)
            students = CustomUser.objects.filter(user_purchased__course__in=teacher_courses, is_Student=True).distinct()[:5]
            return render(request, 'teacher/index.html', {"students": students})
        elif request.user.is_Student:
            category = CourseCategory.objects.all()
            if category:
                user_purchased_course = Course.objects.filter(course_purchased__user=request.user)
                most_purchased_course = most_purchased_course.exclude(id__in=user_purchased_course)
                most_purchased_course = most_purchased_course[:3]
                course = Course.objects.filter(category=category[0], hide=False, approved=True)

                context = {"slider": slider, "most_purchased_course": most_purchased_course, "categories": category,
                           "course": course, 'category': category[0], "testimonial": testimonial,
                           'new_courses': new_courses, "live_courses": live_courses, "most_viewed_courses":most_viewed_courses}
            else:
                course = []
                context = {"slider": slider, "most_purchased_course": most_purchased_course, "categories": category,
                           "course": course, 'category': {"id": 0, "category_name": "", "title": "", "description": ""},
                           "testimonial": testimonial, 'new_courses': new_courses, "live_courses": live_courses, "most_viewed_courses":most_viewed_courses}
            return render(request, 'index_guest.html', context=context)
        else:
            return HttpResponseRedirect(reverse("admin:index"))
    else:
        category = CourseCategory.objects.all()

        if category:
            course = Course.objects.filter(category=category[0], hide=False, approved=True)

            context = {"slider": slider, "most_purchased_course": most_purchased_course[:3], "categories": category,
                       "course": course, 'category': category[0], "testimonial": testimonial,
                       'new_courses': new_courses, "live_courses": live_courses, "most_viewed_courses":most_viewed_courses}
        else:
            course = []
            context = {"slider": slider, "most_purchased_course": most_purchased_course[:3], "categories": category,
                       "course": course, 'category': {"id": 0, "category_name": "", "title": "", "description": ""},
                       "testimonial": testimonial, 'new_courses': new_courses, "live_courses": live_courses, "most_viewed_courses":most_viewed_courses}
        return render(request, 'index_guest.html', context=context)  





def GetUserDetails(request,id):
    user = CustomUser.objects.get(id = id)
    return render(request,'user-face/profile.html',{"user_details":user})

def categoryWiseCourse(request,cid):
    cat = CourseCategory.objects.get(id=cid)
    course = Course.objects.filter(category=cat,hide=False,approved=True)
    language = Language.objects.all()

    return render(request,'category_course.html',context={"courses":course,'category':cat,"language":language})


# def courseDetailView(request,id):
#     cobj = Course.objects.get(id=id)
#     qs = Course.objects.all()
#     HitCount.objects.get_or_create(ip_address=get_client_ip(request),course=cobj)
#     return render(request, 'user-face/course_details.html',{"course":cobj,"courses":qs})

def courseDetailView(request, id):
    cobj = Course.objects.get(id=id)
    total_topics = cobj.chapter_course.aggregate(total=Count('topic_chapter'))['total']
    HitCount.objects.get_or_create(ip_address=get_client_ip(request), course=cobj)
    return render(request, 'user-face/course_details.html', {"course": cobj, "total_topics": total_topics})



def livecourseDetailView(request,id):
    cobj = Course.objects.get(id=id)
    qs = Course.objects.all()
    gst_amount = cobj.fees * 0.18 
    HitCount.objects.get_or_create(ip_address=get_client_ip(request),course=cobj)
    return render(request, 'user-face/live_course_details.html',{"course":cobj,"courses":qs, "gst_amount": gst_amount})


# def playCourseView(request,id):
#     cobj = Course.objects.get(id=id)
#     cp = CourseProgress.objects.get(user=request.user,course=cobj)
#     if cp.progress == 0:
#         cp.progress = 1.0
#         cp.save()
#     return render(request, 'user-face/course_play.html',{"course":cobj})

# def playCourseView(request, id):
#     try:
#         cobj = Course.objects.get(id=id)
#         try:
#             cp = CourseProgress.objects.get(user=request.user, course=cobj)
            
#             if cp.progress == 0:
#                 cp.progress = 1.0
#                 cp.save()
            
#             return render(request, 'user-face/course_play.html', {"course": cobj})
        
#         except ObjectDoesNotExist:
#             cp = CourseProgress.objects.create(user=request.user, course=cobj, progress=1.0)
#             return render(request, 'user-face/course_play.html', {"course": cobj})
        
#     except MultipleObjectsReturned:
#         cp = CourseProgress.objects.filter(user=request.user, course=cobj).first()
#         return render(request, 'user-face/course_play.html', {"course": cobj}) 


def playCourseView(request, id):
    try:
        cobj = Course.objects.get(id=id)
        try:
            cp = CourseProgress.objects.get(user=request.user, course=cobj)
            
            if cp.progress == 0:
                cp.progress = 1.0
                cp.save()
            
            return render(request, 'user-face/course_play.html', {"course": cobj})
        
        except ObjectDoesNotExist:
            cp = CourseProgress.objects.create(user=request.user, course=cobj, progress=1.0)
            return render(request, 'user-face/course_play.html', {"course": cobj})
        
    except MultipleObjectsReturned:
        cp = CourseProgress.objects.filter(user=request.user, course=cobj).first()
        return render(request, 'user-face/course_play.html', {"course": cobj}) 


def NotFoundView(request):
    return render(request, 'user-face/404.html')

def UserRegistration(request):
    request.session['type'] = "user"
    request.session['from'] = "new_reg"
    if request.method == 'POST':
        f_name = request.POST['first_name']
        l_name = request.POST['last_name'] 
        email = request.POST['email']
        mobile = request.POST['mobile']
        date_of_birth = request.POST['date_of_birth']
        gender = request.POST['gender']
        area_of_intrest = request.POST.getlist('tags')

        if CustomUser.objects.filter(email = email).exists() or CustomUser.objects.filter(mobile = mobile).exists():
            messages.warning(request, f'Email id and Mobile number already used!')
            return redirect('user_registration')
        else:
            request.session['first_name'] = f_name
            request.session['last_name'] = l_name
            request.session['email'] = email
            request.session['mobile'] = mobile
            request.session['date_of_birth'] = date_of_birth
            request.session['gender'] = gender
            request.session['area_of_intrest'] = area_of_intrest

            # generate otp and send
            keygen = generateKey()
            key = base64.b32encode(keygen.returnValue(mobile).encode())
            OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)
            request.session['notp'] = OTP.now()
            messages.success(request, f'OTP send successfully')
            return render(request,'user-face/otp_login.html')

    return render(request,'user-face/registration.html')

def InstructorRegistration(request):
    request.session['type'] = "instructor"
    request.session['from'] = "new_reg"

    if request.method == 'POST':
        data = request.POST
        email = data['email']
        mobile = data['mobile']
        profile_image = request.FILES.get('profile_image')

        if CustomUser.objects.filter(email = email).exists() or CustomUser.objects.filter(mobile = mobile).exists():
            user = CustomUser.objects.get(email = email, mobile = mobile)
            error = "This email and mobile number already used!"
            messages.error(request, f' This email and mobile number already used!')
            # return JsonResponse({"message":error,"error":True})
            return redirect('instructor_registration')
        else:
            request.session['ins_data'] = data
            request.session['email'] = email
            request.session['mobile'] = mobile
            user = CustomUser.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'], 
                mobile = data['mobile'],
                gender = data['gender'],
                date_of_birth = data['date_of_birth'],
                experience = data['experience'],
                address = data['address'],
                about = data['about'],
                # profile_image = request.FILES['profile_image'],
                profile_image=profile_image,
                is_Teacher = True,
                is_active = False,
                reg_steps = 1
            )
            for tag in request.POST.getlist('tags'):
                user.intrest_area.add(tag)

            if user:
                UserKYC.objects.create(
                    user=user,kyc_name="Adhar Card",kyc_doc_number = data['adhar_number'],
                    linked_number=data['mobile'],kyc_image_front=request.FILES['adhar_image_front'],
                    kyc_image_back=request.FILES['adhar_image_back']
                )
                UserKYC.objects.create(
                    user=user,kyc_name="Pan Card",kyc_doc_number = data['pan_number'],
                    linked_number=data['mobile'],kyc_image_front=request.FILES['pan_image_front'],
                    kyc_image_back=request.FILES['pan_image_back']
                )
                Education.objects.create(
                    user=user,institution_name=data['institution_name'],institution_address=data['institution_address'],
                    subject=data['subject'],grade=data['grade'],year=data['year']
                )
                Banks.objects.create(
                    user=user,account_name=data['bank_user_name'],account_number=data['account_number'],bank_name=data['bank_name'],
                    ifsc_code=data['ifsc_code'],phone_number=data['mobile']
                )

                # generate otp and send
                keygen = generateKey()
                key = base64.b32encode(keygen.returnValue(mobile).encode())
                OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)
                request.session['notp'] = OTP.now()
                messages.success(request, f'OTP send successfully')
                return redirect('verify_otp')
            # return JsonResponse({"message":"OTP send successfully","error":False,"otp":OTP.now(),'from':"new_reg"})
            # return render(request,'user-face/otp_login.html', context={"otp":OTP.now(),'from':"new_reg"})

    return render(request,'user-face/registration.html')



def AddEducation(request):
    if request.method == 'POST':
        uobj = CustomUser.objects.get(id=request.session['user_id'])
        data = json.loads(request.body)
        Education.objects.create(
            user = uobj,
            institution_name = data['institution_name'],
            institution_address = data['institution_address'],
            subject = data['subject'],
            grade = data['grade'],
            year = data['year']
        )
        uobj.reg_steps = request.session['step']
        uobj.save()
        request.session['step'] = 3
        return JsonResponse({"message":"School/College Added","error":False})
    return redirect('instructor_registration')

def AddKycDocument(request):
    if request.method == 'POST':
        uobj = CustomUser.objects.get(id=request.session['user_id'])
        # data = json.loads(request.data)
        data = request.POST
        UserKYC.objects.create(
            user = uobj,
            kyc_name = data['kyc_name'],
            kyc_doc_number = data['kyc_doc_number'],
            kyc_image_front = data['kyc_image_front'],
            kyc_image_back = data['kyc_image_back'],
            linked_number = data['linked_number']
        )

        uobj.reg_steps = request.session['step']
        uobj.save()
        request.session['step'] = 4
        # return JsonResponse({"message":"KYC Document Added","error":False})
        return redirect('home')
    return redirect('instructor_registration')



def UserLogin(request):
    request.session['from'] = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        try:
            if "@" in username:
                user = CustomUser.objects.get(email = username)
            else:
                user = CustomUser.objects.get(mobile = username)
            if user.is_active:
                # generate otp and send
                keygen = generateKey()
                key = base64.b32encode(keygen.returnValue(username).encode())
                OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)
                request.session['notp'] = OTP.now()
                messages.success(request, f'OTP send successfully')
                return render(request,'user-face/otp_login.html', context={"user_name":username,"otp":OTP.now(),'from':"login"})
            else:
                messages.warning(request, f'account dose not active please contact to admin')
        except ObjectDoesNotExist:
            messages.warning(request, f'account dose not exit please sign in')
    return render(request,'user-face/login.html')



def VerifyOtp(request):
    if request.method == 'POST':
        if request.session['from'] == "new_reg":
            mobile = request.session['mobile']
            otp = request.POST["otp"]
            keygen = generateKey()
            key = base64.b32encode(keygen.returnValue(mobile).encode())
            OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)
            if OTP.verify(otp):
                if request.session['type'] == 'user':
                    user = CustomUser(
                        first_name = request.session['first_name'],
                        last_name = request.session['last_name'],
                        email = request.session['email'], 
                        mobile = request.session['mobile'],
                        gender = request.session['gender'],
                        date_of_birth = request.session['date_of_birth'],
                        
                        is_Student = True,
                        reg_steps = 1
                    )
                    user.save()
                    for tag in request.session['area_of_intrest']:
                        user.intrest_area.add(tag)
                    form = login(request, user)
                   #SendRegistrationMail(email=user.email)
                    request.session['mobile']=""
                    request.session['email']=""
                    request.session['notp']=""
                    messages.success(request, f' OTP verify successfully !!')
                    
                    # messages.success(request, f' welcome {user.first_name} {user.last_name}.')
                    return redirect("home")
                elif request.session['type'] == 'instructor':
                    user = CustomUser.objects.get(mobile=request.session['mobile'],email=request.session['email'])
                    user.is_active = True
                    user.save()
                    form = login(request, user)
                    SendRegistrationMail(email=user.email)
                    request.session['mobile']=""
                    request.session['email']=""
                    request.session['notp']=""
                    messages.success(request, f' OTP verify successfully !!')
                    return redirect('home')
                    # messages.success(request, f' OTP verify successfully !!')
                    # return render(request,'user-face/registration.html',{"type":"instructor","step":2,"user":user})
            else:
                messages.warning(request, f'Invalid OTP')
                return render(request,'user-face/otp_login.html')
        else:
            username = request.POST['username']
            otp = request.POST["otp"]
            keygen = generateKey()
            key = base64.b32encode(keygen.returnValue(username).encode())
            OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)
            if OTP.verify(otp):
                if "@" in username:
                    user = CustomUser.objects.get(email = username)
                else:
                    user = CustomUser.objects.get(mobile = username)
                form = login(request, user)
                user.online_status = True
                user.save()
                messages.success(request, f' OTP verify successfully !!')
                return redirect("home")
            else:
                messages.warning(request, f'Invalid OTP')
                return render(request,'user-face/otp_login.html', context={"user_name":username,})  
    return render(request,'user-face/otp_login.html',{'from':request.GET.get('from')})



def LogOut(request):
    user = CustomUser.objects.get(id=request.user.id)
    user.online_status = False
    user.save()
    logout(request)
    return redirect('home')

def userDashboard(request):
    if request.user.is_authenticated:
        course = sorted(Course.objects.all(), key=lambda a: a.get_hit_count, reverse=True)[:3]
        return render(request,'user-face/index.html',{"course":course})
    return HttpResponseRedirect(reverse("user_login"))

def viewUserProfile(request):
    if request.user.is_authenticated:
        return render(request, 'user-face/profile_self.html')
    return HttpResponseRedirect(reverse("user_login"))

def uploadUserProfile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    obj = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        data = request.POST
        if data['date_of_birth'] != "":
            cdate = request.POST['date_of_birth']
        else:
            cdate = None
        obj.first_name = data['first_name']
        obj.last_name = data['last_name']
        obj.date_of_birth = cdate
        obj.gender = data['gender']
        obj.about = data['about']
        obj.save()
        for tag in request.POST.getlist('tags'):
            obj.intrest_area.add(tag)
        return HttpResponseRedirect(reverse("view_user_profile"))
    return redirect('view_user_profile')

def ApproveUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        obj = CustomUser.objects.get(id=data['id'])
        obj.is_active = True
        obj.save()
        return JsonResponse({"message": "Approved"})

def DisapproveUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        obj = CustomUser.objects.get(id=data['id'])
        obj.is_active = False
        obj.save()
        return JsonResponse({"message": "Approved"})

def DeleteUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        obj = CustomUser.objects.get(id=data['id'])
        obj.delete()
        return JsonResponse({"message": "Deleted"})

@login_required()
def CartDetails(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    gst_rate = settings.GST_RATE
    gst_price = cart.cart_total * gst_rate / 100
    total_price = cart.cart_total + gst_price
    return render(
        request, 'user-face/cart.html',
        {
            'cart':cart,'cart_items': cart_items,
            "gst_price":gst_price,'gst_rate':gst_rate,
            'coupon_applied':cart.coupon_applied,
            'total_price': cart.cart_total, 'to_pay':total_price,
        }
    )

# @login_required()
# def addToCart(request, id):
#     course = Course.objects.get(pk=id)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, course=course)
    
#     if not item_created:
#         cart_item.quantity += 1
#         cart_item.save()
    
#     return redirect('cart')


@login_required()
def addToCart(request, id):
    course = get_object_or_404(Course, pk=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, course=course)
    
    context = {
        'course': course,
        'cart': cart,
        'cart_item': cart_item,  # Pass the cart_item to the context
    }
    return render(request, 'user-face/course_details.html', context)



@login_required()
def removeFromCart(request, id):
    cart_item = CartItem.objects.get(id=id)
    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart')

@login_required()
def deleteFromCart(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect('cart')



@login_required()
def ApplyCartCoupon(request,id):
    # if request.method == "POST":
    coupon = Coupon.objects.get(id=id)
    cart = request.user.user_cart
    for i in cart.cart_items.all():
        c = Course.objects.get(id=i.course.id)
        # if request.user in c.coupon_applied_by:
        c.coupon_applied_by.remove(request.user)

    if cart.coupon:
        if cart.coupon.id == id:
            cart.coupon = None
            cart.save()
        else:
            cart.coupon = coupon
            cart.save()
    else:
        cart.coupon = coupon
        cart.save()
    return redirect('cart')



@login_required()
def ApplyCourseCoupon(request,id):
    if request.method == 'POST':
        cobj = Course.objects.get(id=id)
        if cobj.coupon_code == request.POST['coupon_code']:
            cobj.coupon_applied_by.add(request.user)
        cart = request.user.user_cart
        cart.coupon = None
        cart.save()

        return redirect('cart')
    return redirect('cart')

def RemoveCourseCoupon(request,id):
    cobj = Course.objects.get(id=id)
    cobj.coupon_applied_by.remove(request.user)
    return redirect('cart')

@login_required()
def cartCheckout(request):
    if request.method == "POST":
        uobj = request.user
        data = json.loads(request.body)
        cart_items = CartItem.objects.filter(cart=Cart.objects.get(user=uobj))
        for i in cart_items:
            cobj = Course.objects.get(id=i.course.id)
            pc = PurchasedCourse.objects.create(user=uobj,course=cobj,order_id=data['order_id'])
            w = Wallet.objects.get(user=cobj.user)
            w.balance = float(w.balance)+ float(cobj.discount_fee)
            w.save()
            i.delete()
        return JsonResponse({"message": "Course Purchased Success",})



# @login_required()
# def PurchaseCourse(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         uobj = request.user
#         cobj = Course.objects.get(id=data['course_id'])
#         po = PurchasedCourse.objects.create(user=uobj,course=cobj,order_id=data['order_id'])
#         wallet = Wallet.objects.get(user=cobj.user)
#         wallet.balance = float(wallet.balance)+float(cobj.discount_fee)
#         wallet.save()

#         global client
#         client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#         trusted_order = client.order.fetch(po.order_id)
#         invoice_number = get_next_invoice_number(po.user)
#         gst_rate = settings.GST_RATE
#         gst_price = po.course.discount_fee * gst_rate / 100
#         sub_total = po.course.discount_fee
#         total_price = trusted_order['amount']/100

#         mail_data = {
#             'email': uobj.email,
#             'name': uobj.full_name,
#             'invoice_number': invoice_number,
#             'order_date': po.created_at,
#             'items':po.course,
#             'subtotal':sub_total,
#             'gst_rate':gst_rate,
#             'gst_price':gst_price,
#             'total':total_price,
#         }
#         SendInvoicMail(data=mail_data)
#         return JsonResponse({"message": "Course Purchased Success",})
#     else:
#         return JsonResponse({"message": "Get method not allowed",})
    


# @login_required
# @require_POST
# def PurchaseCourse(request):
#     try:
#         data = json.loads(request.body)
#         user = request.user
#         course_id = data.get('course_id')
#         order_id = data.get('order_id')
#         course = Course.objects.get(id=course_id)
#         purchased_course = PurchasedCourse.objects.create(user=user, course=course, order_id=order_id)
#         wallet = Wallet.objects.get(user=user)
#         wallet.balance = float(wallet.balance) + float(course.discount_fee)
#         wallet.save()
#         trusted_order = client.order.fetch(order_id)   
#         invoice_number = get_next_invoice_number(user)
#         gst_rate = settings.GST_RATE
#         gst_price = course.discount_fee * gst_rate / 100
#         sub_total = course.discount_fee
#         total_price = trusted_order['amount'] / 100

        
#         mail_data = {
#             'email': user.email,
#             'name': user.full_name,
#             'invoice_number': invoice_number,
#             'order_date': purchased_course.created_at,
#             'items': course,
#             'subtotal': sub_total,
#             'gst_rate': gst_rate,
#             'gst_price': gst_price,
#             'total': total_price,
#         }
#         SendInvoicMail(data=mail_data)

#         return JsonResponse({"message": "Course Purchased Successfully"})
#     except Course.DoesNotExist:
#         return JsonResponse({"error": "Course not found"}, status=404)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)



@login_required
@require_POST
def PurchaseCourse(request):
    try:
        data = json.loads(request.body)
        user = request.user
        course_id = data.get('course_id')
        order_id = data.get('order_id')
        course = Course.objects.get(id=course_id)
        purchased_course = PurchasedCourse.objects.create(user=user, course=course, order_id=order_id)
        wallet = Wallet.objects.get(user=course.user)
        wallet.balance = float(wallet.balance) + float(course.discount_fee)
        wallet.save()
        trusted_order = client.order.fetch(order_id)   
        invoice_number = get_next_invoice_number(user)
        gst_rate = settings.GST_RATE
        gst_price = course.discount_fee * gst_rate / 100
        sub_total = course.discount_fee
        total_price = trusted_order['amount'] / 100

        
        mail_data = {
            'email': user.email,
            'name': user.full_name,
            'invoice_number': invoice_number,
            'order_date': purchased_course.created_at,
            'items': course,
            'subtotal': sub_total,
            'gst_rate': gst_rate,
            'gst_price': gst_price,
            'total': total_price,
        }
        SendInvoicMail(data=mail_data)

        return JsonResponse({"message": "Course Purchased Successfully"})
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def custom_user_change_view(request, pk):
    # Your view logic here
    # For example:
    return HttpResponse("This is a placeholder response")



@login_required()
def UserPurchasedCourse(request):
    user = CustomUser.objects.get(id=request.user.id)
    qs = PurchasedCourse.objects.filter(user=user, course__type='Pre Recorded')
    return render(request, 'user-face/user_purchased.html', context={'courses':qs})



@login_required()
def UserPurchasedliveCourse(request):
    user = CustomUser.objects.get(id=request.user.id)
    qs = PurchasedCourse.objects.filter(user=user, course__type='Live')
    return render(request, 'user-face/user_purchased_live.html', context={'courses':qs})



@login_required()
def UserWishlist(request):
    user = CustomUser.objects.get(id=request.user.id)
    qs = user.wishlists.all()
    return render(request, 'user-face/wishlist.html',context={'courses':qs})

@login_required()
def AddToWishlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cobj = Course.objects.get(id=data['id'])
        if cobj.wishlist.contains(request.user):
            cobj.wishlist.remove(request.user)
            # messages.add_message(request, messages.SUCCESS, "Course removed from Wishlist")
            return JsonResponse({"status":"remove","message": "Course removed from Wishlist",})
        else:
            cobj.wishlist.add(request.user)
            # messages.add_message(request, messages.SUCCESS, "Course added in Wishlist")
            return JsonResponse({"status":"add","message": "Course added in Wishlist",})

@login_required()
def RemoveFromWishlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cobj = Course.objects.get(id=data['id'])
        cobj.wishlist.remove(request.user)
        #messages.add_message(request, messages.SUCCESS, "Course Removed Successfully!")
        return JsonResponse({"message": "Course removed from Wishlist",})

@login_required()
def subscription(request):
    subscriptions = Membership.objects.all()
    context = {'subscriptions': subscriptions}
    return render(request, 'teacher/planning.html', context)

@login_required()
def checkoutSubscription(request):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = data['amount']
        currency = data['currency']
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount" : amount, "currency" : currency,}
        payment = client.order.create(data=data)
        return JsonResponse({"message": "Success","RAZOR_KEY_ID":settings.RAZOR_KEY_ID,"RAZOR_KEY_SECRET":settings.RAZOR_KEY_SECRET, "result": payment})

@login_required()
def initEnrollPayment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = float(data['amount'])
        gst_rate = settings.GST_RATE
        gst_price = amount * gst_rate / 100
        total_amount = amount + gst_price
        currency = data['currency']
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount" : total_amount*100, "currency" : currency,}
        payment = client.order.create(data=data)
        return JsonResponse({"message": "Success","RAZOR_KEY_ID":settings.RAZOR_KEY_ID,"RAZOR_KEY_SECRET":settings.RAZOR_KEY_SECRET, "result": payment})

@login_required()
def VerifySignature(request):
    if request.method == "POST":
        data = json.loads(request.body)
        global client
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        params_dict = {
            'razorpay_payment_id' : data['razorpay_paymentId'],
            'razorpay_order_id' : data['razorpay_orderId'],
            'razorpay_signature' : data['razorpay_signature']
        }
        res = client.utility.verify_payment_signature(params_dict)
        return JsonResponse({"message": "Success","result":res})

@login_required()
def subscribe(request):
    if request.method == "POST":
        print("=======")
        data = json.loads(request.body)
        print(data['plan_id'])
        payment_for = Membership.objects.get(id=data['plan_id'])
        paystack_charge_id = get_random_string(50)
        paystack_access_code = get_random_string(50)
        amount = payment_for.price

        payhistory = PayHistory.objects.create(
            user=request.user, payment_for=payment_for,
            paystack_charge_id=paystack_charge_id,
            paystack_access_code=paystack_access_code, amount=amount, paid=True)
        payhistory.save()
        try:
            subscribeplan = UserMembership.objects.get(user=request.user)
            subscribeplan.membership = payment_for
            subscribeplan.save()
        except:
            subscribeplan = UserMembership.objects.create(user=request.user,membership = payment_for)
        
        return JsonResponse({"message": "Course Purchased Success",})
        # callback_url = reverse('callback')
        # return redirect(callback_url + f'?paystack_charge_id={payhistory.paystack_charge_id}')

@login_required()
def callback(request):
    paystack_charge_id = request.GET.get('paystack_charge_id')

    # Retrieve the PayHistory instance or return a 404 response
    payhistory = get_object_or_404(PayHistory, paystack_charge_id=paystack_charge_id)

    # Retrieve the Membership instance associated with the PayHistory
    membership_instance = payhistory.payment_for

    # Retrieve the UserMembership instance for the current user
    # try:
    subscribeplan = UserMembership.objects.get_or_create(user=request.user)
    # except:
    #     subscribeplan = UserMembership.objects.create(user=request.user, membership=membership_instance)

    # Update the membership attribute of the UserMembership instance

    subscribeplan.membership = membership_instance
    subscribeplan.save()

    return redirect('home')

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def usercertificate(request, cid):
    course = Course.objects.get(id=cid)
    pur_his = PurchasedCourse.objects.get(course=course,user=request.user)
    if course and pur_his:
        return render_to_pdf('certificate2.html',{'customerName':request.user.first_name,'customerNamelast':request.user.last_name,
        'customerEmail':request.user.email,"course":course})

    return render_to_pdf('certificate2.html', {'course':course})

def support(request):
    if request.method == "POST":
        SupportQuery.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            mobile = request.POST['mobile'],
            query = request.POST['query'],
        )
        messages.success(request, f'Query created successfully')
        return redirect('support')    
    return render(request,'support.html')

def aboutUs(request):
    return render(request,'about_us.html')

def ContactUs(request):
    return render(request,'contact_us.html')

def TermsAndConditions(request):
    tc = TermsAndCondition.objects.all()
    return render(request,'terms_and_conditions.html',{"terms":tc[0]})

def Privacy_Policy(request):
    pp = PrivacyPolicy.objects.all()
    return render(request,'privacy_policy.html',{"privacy":pp[0]})

def courseQuery(request):
    if request.method == "POST":
        course = Course.objects.get(id=request.POST['course'])
        CourseQuery.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            mobile = request.POST['mobile'],
            course = course,
            query = request.POST['query'],
        )
        messages.success(request, f'Query created successfully')
        return redirect('course_query')    
    return render(request,'user-face/course_query.html')

def NewCategoryRequest(request):
    if request.method == "POST":
        data = json.loads(request.body)
        obj = CustomUser.objects.get(id=data['id'])
        CategoryRequest.objects.create(
            user=obj,
            query = data['query']
        )
        return JsonResponse({"message": "Request created successfully"})

class GlobalSearchView(ListView):
    
    model = Course
    template_name = 'search.html'

    # def get_queryset(self):
    #     query = self.request.GET.get('q', '')

        
    #     course_results = Course.objects.filter(course_name__icontains=query)

    #     return course_results
    
    # def get_queryset(self):
    #     query = self.request.GET.get('q', '')
    #     blog_results = Course.objects.filter(category__category_name__icontains=query)
    #     catefories = CourseCategory.objects.filter(category_name__icontains=query)
    #     ct_course = Course.objects.none()
    #     for c in catefories:
    #         qs = Course.objects.filter(category=c)
    #         ct_course = ct_course|qs
    #     # Combine and return the results
    #     print(blog_results | ct_course)
    #     return blog_results | ct_course
      
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        blog_results = Course.objects.filter(category__category_name__icontains=query)
        categories = CourseCategory.objects.filter(category_name__icontains=query)
        ct_course = Course.objects.none()
        for category in categories:
            qs = Course.objects.filter(category=category)
            ct_course = ct_course | qs
        combined_results = blog_results | ct_course
        return combined_results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')  # Pass 'q' value to the template
        return context


#===================Notification related views======================#
@login_required
def notification_list(request):
    notifications_qs = Notification.objects.filter(user=request.user).order_by("-timestamp")
    new_notifs = notifications_qs.filter(viewed=False)
    old_notifs = notifications_qs.filter(viewed=True)
    context = {"notifications":old_notifs|new_notifs,}
    return render(request, 'teacher/notification.html', context)

@login_required
def notification_view(request, notif_id):
    notif = get_object_or_404(Notification, pk=notif_id)
    if notif.user == request.user:
        context = {'notif': notif}
        notif.mark_viewed()
        return render(request, 'notifications/view.html', context)
    else:
        messages.error(request, 'You are not authorized to view that notification.')
        return redirect('notification_list')

@login_required
def remove_notification(request, notif_id):
    notif = get_object_or_404(Notification, pk=notif_id)
    if notif.user == request.user:
        if Notification.objects.filter(id=notif_id).exists():
            notif.delete()
            messages.success(request, 'Deleted notification.')
    else:
        messages.error(request, 'Failed to locate notification.')
    return redirect('notification_list')

@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user).update(viewed=True)
    messages.success(request, 'Marked all notifications as read.')
    return redirect('notification_list')

@login_required
def delete_all_read(request):
    Notification.objects.filter(user=request.user).filter(viewed=True).delete()
    messages.success(request, 'Deleted all read notifications.')
    return redirect('notification_list')

def user_notifications_count(request, user_pk: int):
    """returns to notifications count for the give user as JSON

    This view is public and does not require login
    """
    unread_count = Notification.objects.user_unread_count(user_pk)
    data = {'unread_count': unread_count}
    return JsonResponse(data, safe=False)

#--------------for discharge patient bill (pdf) download and printing
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



# def get_next_invoice_number(user):
#     qs = Invoice.objects.all().order_by('-date')
#     last_in = 'SPRT0000'
#     if qs:
#         last_in = qs[0].invoice_number
#     a = last_in.split('SPRT')[1]
#     new_invoice_number = "SPRT{}".format(str(int(a)+1))
#     invoice, created = Invoice.objects.get_or_create(user=user)
#     if created:
#         if last_in != '':
#             invoice.invoice_number = new_invoice_number
#             invoice.save()
#             return new_invoice_number
#         else:
#             invoice.invoice_number = f"SPRT0001"
#             invoice.save()
#             return new_invoice_number
#     else:
#         invoice.invoice_number = new_invoice_number
#         invoice.save()
#         return new_invoice_number
    

def get_next_invoice_number(user):
    with transaction.atomic():
        last_invoice = Invoice.objects.filter(user=user).order_by('-date').first()
        last_invoice_number = last_invoice.invoice_number if last_invoice else 'SPRT0000'
        invoice_number_prefix = 'SPRT'
        invoice_number_suffix = int(last_invoice_number[4:])
        new_invoice_number_suffix = invoice_number_suffix + 1
        new_invoice_number = f"{invoice_number_prefix}{new_invoice_number_suffix:04d}"

        
        if last_invoice:
            last_invoice.invoice_number = new_invoice_number
            last_invoice.save()
        else:
            
            Invoice.objects.create(user=user, invoice_number=new_invoice_number)

    return new_invoice_number


# @login_required()
# def download_invoice_view(request, id):
#     po = PurchasedCourse.objects.get(id=id)
#     global client
#     client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#     trusted_order = client.order.fetch(po.order_id)
#     order_date = datetime.datetime.fromtimestamp(trusted_order['created_at'])
#     invoice_number = get_next_invoice_number(po.user)
#     gst_rate = settings.GST_RATE
#     gst_price = (trusted_order['amount']/100) * gst_rate / 100
#     total_price = (trusted_order['amount']/100) + gst_price
#     mydict={
#         'orderDate':order_date,
#         'user':po.user,
#         'orderStatus':trusted_order['status'],
#         'product':po.course,
#         'invoiceNumber': invoice_number,
#         'gst_rate':gst_rate,
#         'gst_price':gst_price,
#         'total':total_price,
#     }
#     return render(request,'test.html', mydict)



@login_required()
def download_invoice_view(request, id):
    po = PurchasedCourse.objects.get(id=id)
    global client
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    trusted_order = client.order.fetch(po.order_id)
    order_date = datetime.datetime.fromtimestamp(trusted_order['created_at'])
    invoice_number = get_next_invoice_number(po.user)
    gst_rate = settings.GST_RATE
    total_price = trusted_order['amount'] / 100  # Convert amount to rupees
    subtotal = total_price / (1 + gst_rate / 100)  # Calculate subtotal
    gst_price = total_price - subtotal  # Calculate GST amount
    mydict = {
    'orderDate': order_date,
    'user': po.user,
    'orderStatus': trusted_order['status'],
    'product': po.course,
    'invoiceNumber': invoice_number,
    'gst_rate': gst_rate,
    'gst_price': gst_price,
    'total': total_price,  # Total price including GST
}


    return render(request,'test.html', mydict)



def filterCourse(request):
    data = json.loads(request.body)
    if data['price']:
        min_price = data['price'][0]['min_price']
        max_price = data['price'][0]['max_price']
    

    rating = data['ratings']
    language = data['languages']
    try:
        cat = CourseCategory.objects.get(id=request.GET.get('cid'))
        course = Course.objects.filter(category=cat,hide=False,approved=True)
    except:
        course = Course.objects.filter(hide=False,approved=True)
    
    courseList = course
    if len(data['price'])>0:
        if min_price >= 10000:
            courseList = courseList.filter(discount_fee__gte=min_price)
        else:
            courseList = courseList.filter(discount_fee__range=(min_price,max_price))
    if len(rating)>0:
        courseList = courseList.filter(course_feedbacks__rating__in = rating).distinct()
    if len(language)>0:
        courseList = courseList.filter(language__in=language).distinct()
    
    t = render_to_string('product_card.html',{"user":request.user,"courses":courseList})
    return JsonResponse({'courses':t})


class CourseQueryAPIView(APIView):
    @staticmethod
    def post(request):
        qs = CourseQuerySerializer(data=request.data)
        if qs.is_valid():
            qs.save()
            return Response({'message': 'Query created successfully',"data":qs.data}, status=status.HTTP_201_CREATED)
        return Response(qs.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserQueriesAPIView(APIView):
    @staticmethod
    def get(request):
        user_queries = CourseQuery.objects.all()
        serializer = UserQueriesSerializer(user_queries, many=True)
        return Response(serializer.data)

def updateTopicProgress(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prg = float(data['progress'])
        topic = Topic.objects.get(id=data['topic_id'])
        topic_progress = TopicProgress.objects.get(topic=topic,user=request.user)
        if prg > topic_progress.progress:
            topic_progress.progress = prg
            topic_progress.save()
        chapter_progress = updateChapterProgress(cid=topic.chapter.id,uid=request.user.id)
        return JsonResponse({"status":"200","message": "Topic progress updated","chapter_progress":chapter_progress})
    return JsonResponse({"status":"400","message":"Get method not allowed"})

def updateChapterProgress(cid,uid):
    chapter = Chapter.objects.get(id=cid)
    user = CustomUser.objects.get(id=uid)
    chapter_progress = ChapterProgress.objects.get(chapter=chapter,user=user)
    topics = Topic.objects.filter(chapter=chapter)
    total_topics = topics.count()
    total_progress_percent = sum(TopicProgress.objects.get(topic=topic,user=user).progress for topic in topics)
    chapter_progress_percent = int(round((total_progress_percent / (total_topics * 100)) * 100,2))
    chapter_progress.progress = chapter_progress_percent
    chapter_progress.save()
    updateCourseProgress(cid=chapter.course.id,uid=uid)
    return chapter_progress.progress

def updateCourseProgress(cid,uid):
    course = Course.objects.get(id=cid)
    user = CustomUser.objects.get(id=uid)
    course_progress = CourseProgress.objects.get(course=course,user=user)
    chapters = Chapter.objects.filter(course=course)
    total_chapters = chapters.count()
    total_progress_percent = sum(ChapterProgress.objects.get(chapter=chapter,user=user).progress for chapter in chapters)
    course_progress_percent = int(round((total_progress_percent / (total_chapters * 100)) * 100,2))
    course_progress.progress = course_progress_percent
    course_progress.save()


@login_required
def teacher_revenue(request):
    try:       
        teacher = request.user
        teacher_courses = Course.objects.filter(user=teacher)      
        purchased_courses = PurchasedCourse.objects.filter(course__in=teacher_courses)      
        total_discount_fees = purchased_courses.aggregate(total_discount_fees=Sum('course__discount_fee'))['total_discount_fees'] or 0

        return JsonResponse({'total_discount_fees': total_discount_fees})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while fetching teacher revenue: {}'.format(str(e))}, status=500)
    


