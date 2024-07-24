from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.shortcuts import render, get_object_or_404

from django.conf import settings

from django.urls import reverse
from django.views import generic
from itertools import chain
from django.template.loader import render_to_string
import razorpay
from django.views.decorators.http import require_POST

import datetime
from datetime import timedelta
from razorpay.resources import Payment
from django.conf import settings
from django.http import JsonResponse


from core.views import get_next_invoice_number
from .utils import*
from core.models import*
import json
import random
import string
import csv
from core.views import updateChapterProgress
from decimal import Decimal

from django.db.models import Q

from core.models import UserKYC  # Import your KYC details model
from django.contrib import messages

# @login_required
# def home(request):
#     return render(request, 'teacher/index.html')

@login_required
def NotFoundView(request):
    return render(request, 'teacher/404.html')

@login_required
def WalletDetails(request):
    return render(request, 'teacher/wallet.html')

# @login_required
# def MakePayoutRequest(request):
#     msg = ""
#     if request.method == "POST": 
#         # payload = json.loads(request.body)
#         wallet = Wallet.objects.get(user=request.user)
#         # wallet.balance -= request.POST["amount"]
#         # wallet.save()
#         amount = request.POST["amount"]
#         bank = Banks.objects.get(uid=request.POST["bank_id"])
#         tqs = sum(WalletTransaction.objects.filter(wallet=wallet,status="pending").values_list('amount',flat=True,))
#         print(tqs)
#         print(wallet.balance)
        
#         # if tqs < wallet.balance:
#         if float(amount) <= wallet.balance-tqs:
#             print("request created")
#             transaction =  WalletTransaction.objects.create(
#                 wallet = wallet,
#                 bank = bank,
#                 amount = amount,
#             )
#             # msg = "Payout request created"
#         else:
#             msg = "Insufficiant balance in wallet"
#         # else:
#         #     msg = "Insufficiant balance in wallet"
        
#         return render(request, 'teacher/wallet.html', {"message":msg})
#     return render(request, 'teacher/wallet.html', {"message":msg})



@login_required
def MakePayoutRequest(request):
    msg = ""
    if request.method == "POST":
        wallet = Wallet.objects.get(user=request.user)
        print(wallet)
        amount = Decimal(request.POST["amount"])
        bank = Banks.objects.get(uid=request.POST["bank_id"])
        print(bank)

        # Check if there are any pending payout requests for the user
        pending_requests = WalletTransaction.objects.filter(wallet=wallet, status="pending").exists()
        if not pending_requests:
            # No pending requests, proceed with creating a new one
            transaction = WalletTransaction.objects.create(
                wallet=wallet,
                bank=bank,
                amount=amount,
            )
            # Deduct the payout amount from the user's wallet balance
            wallet.balance -= amount
            wallet.save()
            msg = "Payout request created"
        else:
            msg = "A payout request is already pending. Please wait until it is completed or canceled."
        
        # Redirect to the same view to prevent form resubmission upon refreshing the page
        return redirect(request.path)

    return render(request, 'teacher/wallet.html', {"message": msg})




@login_required
def AddBank(request):
    if request.method == "POST":
        bank = Banks(
            user = request.user,
            account_name = request.POST['account_name'],
            account_number = request.POST['account_number'],
            bank_name = request.POST['bank_name'],
            ifsc_code = request.POST['ifsc_code'],
            phone_number = request.POST['phone_number']
        )
        bank.save()
        return HttpResponseRedirect('wallet_details')
    return render(request, 'teacher/wallet.html')

def DeleteBank(request, id):
    obj = Banks.objects.get(uid=id)

    obj.delete()
    return redirect('wallet_details')

@login_required
def AddCourseModule(request):
    if request.method == 'POST':
        name = request.POST['module_name']
        description = request.POST['description']
        title = request.POST['title']
        data = CourseCategory(
            category_name=name,
            title=title,
            description=description
            )
        data.save()
        return HttpResponseRedirect('/teacher/add_module')
    else:
        return render(request, 'teacher/add_modules.html')

@login_required
def AddCourse(request):
    modules = CourseCategory.objects.all()
    language = Language.objects.all()

    if request.method == 'POST':
        # actual fee
        try:
            if request.POST['paid_course'] == "No":
                pc = True
            else:
                pc = False
        except:
            pc = False
        try:
            if request.POST['generated_coupon'] == "No":
                cc = True
            else:
                cc = False
        except:
            cc = False

        # discount fee
        try:
            acf = float(request.POST['actual_fee'])
        except:
            acf = 0.0
        try:
            dsf = float(request.POST['discount_fee'])
        except:
            dsf = 0.0
        try:
            timg = float(request.POST['thumb_image'])
        except:
            timg = 0.0
        try:
            video = float(request.POST['course_video'])
        except:
            video = 0.0
        try:
            sf = float(request.POST['setup_file'])
        except:
            sf = 0.0
        try:
            cc = float(request.POST['course_content'])
        except:
            cc = 0.0

        if request.POST['coupon_valid_date'] != "":
            cdate = request.POST['coupon_valid_date']
        else:
            cdate = None
        if request.POST['coupon_valid_time'] != "":
            ctime = request.POST['coupon_valid_time']
        else:
            ctime = None
        # schedule date time
        if request.POST['schedule_date'] != "":
            scdate = request.POST['schedule_date']
        else:
            scdate = None
        if request.POST['schedule_time'] != "":
            sctime = request.POST['schedule_time']
        else:
            sctime = None
        
        data = Course(
            user = CustomUser.objects.get(id=request.user.id),
            category = CourseCategory.objects.get(id=request.POST['category_id']),
            type = request.POST['course_type'],
            course_name = request.POST['course_name'],
            description = request.POST['description'],
            paid_course = pc,
            actual_fee = acf,
            discount_fee = dsf,
            total_discount = request.POST['total_discount'],
            generated_coupon = cc,
            coupon_code = request.POST['coupon_code'],
            coupon_percent = request.POST['coupon_percent'],
            coupon_valid_date = cdate,
            coupon_valid_time = ctime,
            schedule_date = scdate,
            schedule_time = sctime
        )
        data.save()
    
        for obj in request.POST.getlist('tags'):
            data.language.add(obj)
        
        if request.FILES:
            thumb_image_file = request.FILES.get('thumb_image')
            if thumb_image_file:
                data.thumb_image.save(thumb_image_file.name, thumb_image_file, save=True)

            course_video_file = request.FILES.get('course_video')
            if course_video_file:
                data.course_video.save(course_video_file.name, course_video_file, save=True)

            setup_file = request.FILES.get('setup_file')
            if setup_file:
                data.setup_file.save(setup_file.name, setup_file, save=True)

            course_content_file = request.FILES.get('course_content')
            if course_content_file:
                data.course_content.save(course_content_file.name, course_content_file, save=True)
           
        return HttpResponseRedirect(reverse('course_list',args=[request.user.id]))
    else:
        return render(request, 'teacher/add_course.html',context={"modules":modules,"language":language })

@login_required
def UpdateCourse(request,id):
    modules = CourseCategory.objects.all()
    course = Course.objects.get(id=id)
    languages = Language.objects.all()
    if request.method == 'POST':
        # actual fee
        try:
            if request.POST['paid_course'] == "No":
                pc = True
            else:
                pc = False
        except:
            pc = False
        try:
            if request.POST['generated_coupon'] == "No":
                cc = True
            else:
                cc = False
        except:
            cc = False

        # discount fee
        try:
            acf = float(request.POST['actual_fee'])
        except:
            acf = 0.0

        try:
            cvid = float(request.POST['course_video'])
        except:
            cvid = 0.0


        try:
            dsf = float(request.POST['discount_fee'])
        except:
            dsf = 0.0
        if request.POST['coupon_valid_date'] != "":
            cdate = request.POST['coupon_valid_date']
        else:
            cdate = None
        if request.POST['coupon_valid_time'] != "":
            ctime = request.POST['coupon_valid_time']
        else:
            ctime = None
        # schedule date time
        if request.POST['schedule_date'] != "":
            scdate = request.POST['schedule_date']
        else:
            scdate = None
        if request.POST['schedule_time'] != "":
            sctime = request.POST['schedule_time']
        else:
            sctime = None
        
        course.category = CourseCategory.objects.get(id=request.POST['category_id'])
        course.type = request.POST['course_type']
        course.course_name = request.POST['course_name']
        course.description = request.POST['description']
        course.paid_course = pc
        course.actual_fee = acf
        course.discount_fee = dsf
        course.total_discount = request.POST['total_discount']
        course.generated_coupon = cc
        course.coupon_code = request.POST['coupon_code']
        course.coupon_percent = request.POST['coupon_percent']
        course.coupon_valid_date = cdate
        course.coupon_valid_time = ctime
        course.schedule_date = scdate
        course.schedule_time = sctime
        
        course.save()
        if request.FILES:
            course.thumb_image = request.FILES['thumb_image']
            course.course_video = cvid
            course.save()
        selected_languages = request.POST.getlist('tags')
        course.language.clear()  
        for lang_id in selected_languages:
            language = get_object_or_404(Language, id=lang_id)
            course.language.add(language)
        course.save()
        
        return redirect('course_list', id=request.user.id)
    else:
        return render(request, 'teacher/update_course.html',context={"modules":modules,"obj":course,"languages": languages})


# @login_required
# def CourseList(request,id):

#     modules = CourseCategory.objects.all()
#     user = CustomUser.objects.get(id=id)
#     course_list = []
#     if user.is_Student:
#         cpqs = PurchasedCourse.objects.filter(user=user)
#         pc = []
#         for c in cpqs:
#             pc.append(c.course)
#         course_list = pc
#     else:
#         course_list = Course.objects.filter(user=user, type = "Pre Recorded")
#     return render(request, 'teacher/course_list.html',context={'course':course_list,"modules":modules})



@login_required
def CourseList(request, id):
    # Retrieve the currently logged-in user (teacher)
    teacher = request.user

    # Ensure that the logged-in user is a teacher
    if not teacher.is_authenticated or not teacher.is_Teacher:
        # Redirect to a different page or show an error message
        return HttpResponse("You do not have permission to access this page.")

    try:
        # Retrieve the student based on the student_id
        student = CustomUser.objects.get(id=id)

        # Get the courses that the student has enrolled in
        if student.is_Student:
            enrolled_courses = PurchasedCourse.objects.filter(user=student).values_list('course', flat=True)
            course_list = Course.objects.filter(id__in=enrolled_courses, user=teacher, type="Pre Recorded")
        else:
            # If the user is not a student, show all pre-recorded courses
            course_list = Course.objects.filter(user=teacher, type="Pre Recorded")

        # Render the template with the enrolled courses and student details
        return render(request, 'teacher/course_list.html', context={"course": course_list, "modules": CourseCategory.objects.all()})
    except CustomUser.DoesNotExist:
        # Handle the case where the student does not exist
        return HttpResponse("Student does not exist.")













@login_required
def Live_Course(request, id):
    modules = CourseCategory.objects.all()
    user = get_object_or_404(CustomUser, id=id)
    live_courses = []  # Corrected variable name

    if user.is_Student:
        cpqs = PurchasedCourse.objects.filter(user=user)
        pc = [c.course for c in cpqs]
        live_courses = pc
    else:
        live_courses = Course.objects.filter(user=user, type="Live")
        print(live_courses)
    return render(request, 'teacher/live_course.html', context={'live_courses': live_courses, "modules": modules})  






@login_required
def AddLiveCourse(request):
    modules = CourseCategory.objects.all()

    if request.method == 'POST':
        # schedule date time
        if request.POST['schedule_date'] != "":
            scdate = request.POST['schedule_date']
        else:
            scdate = None
        if request.POST['schedule_time'] != "":
            sctime = request.POST['schedule_time']
        else:
            sctime = None

        data = Course(
            user = CustomUser.objects.get(id=request.user.id),
            category = CourseCategory.objects.get(id=request.POST['category_id']),
            type = request.POST['course_type'],
            description = request.POST['description'],

            url = request.POST['url'],
            host_name = request.POST['host_name'],
            title = request.POST['title'],
            about_host = request.POST['about_host'],
            fees = request.POST['fees'],  
            schedule_date = scdate,
            schedule_time = sctime,
        )
        data.save()
        
        if request.FILES:
            data.thumb_image = request.FILES.get('thumb_image')
            data.save()
        
        return HttpResponseRedirect(reverse('live_course',args=[request.user.id]))
    else:
        return render(request, 'teacher/add_live_course.html',context={"modules":modules})


@login_required
def LiveCourseUpdate(request, id):
    modules = CourseCategory.objects.all()
    course = get_object_or_404(Course, id=id)
    print(course)
    if request.method == 'POST':

        if request.POST['schedule_date'] != "":
            scdate = request.POST['schedule_date']
        else:
            scdate = None

        if request.POST['schedule_time'] != "":
            sctime = request.POST['schedule_time']
        else:
            sctime = None
        
        course.category = CourseCategory.objects.get(id=request.POST['category_id'])
        course.type = request.POST['course_type']

        course.description = request.POST['description']
        course.url = request.POST['url']
        course.host_name = request.POST['host_name']
        course.title = request.POST['title']
        course.about_host = request.POST['about_host']
        course.fees = request.POST['fees']
        course.schedule_date = scdate
        course.schedule_time = sctime
        
        course.save()
        
        if request.FILES:
            course.thumb_image = request.FILES['thumb_image']
            course.save()
        
        return redirect('live_course', id=request.user.id)
    else:
        return render(request, 'teacher/live_course_update.html', context={"modules": modules, "obj": course})
    


@login_required
def GetCourse(request):
    qs = Course.objects.filter(
        user = request.user,
        category=CourseCategory.objects.get(id=request.GET.get('category_id'))
    ).values("id","course_name","type")
    return JsonResponse({'courses':json.dumps(list(qs))})

@login_required
def AddChapter(request,id):
    course = Course.objects.get(id=id)
    if request.method == 'POST':
        data = Chapter(
            course = Course.objects.get(id=request.POST['course_id']),
            chapter_name = request.POST['chapter_name'],
            description = request.POST['description']
        )
        data.save()
        return HttpResponseRedirect('/teacher/add_topic/{}'.format(data.id),)
    else:
        return render(request, 'teacher/add_chapter.html',context={"course":course})

@login_required
def UpdateChapter(request, id):
    course = Course.objects.all()
    chapter = Chapter.objects.get(id=id)
    if request.method == 'POST':
        
        chapter.chapter_name = request.POST['chapter_name']
        chapter.description = request.POST['description']
        chapter.save()
        return redirect('chapter_list', id=chapter.course.id)
    else:
        return render(request, 'teacher/update_chapter.html',context={"course":course,"chapter":chapter})

@login_required
def GetChapter(request):
    qs = Chapter.objects.filter(course=Course.objects.get(id=request.GET.get('course_id'))).values("id","chapter_name","description")
    return JsonResponse({'chapters':json.dumps(list(qs))})

@login_required
def ChapterList(request,id):
    obj = Course.objects.get(id=id)
    qs = Chapter.objects.filter(course=obj)
    return render(request, 'teacher/chapter_list.html',context={'chapter':qs,"course":obj})
    

@login_required
def AddTopic(request,id):
    chapter = Chapter.objects.get(id=id)
    if request.method == 'POST':
        data = Topic(
            chapter = Chapter.objects.get(id=request.POST['chapter_id']),
            topic_name = request.POST['topic_name'],
            description = request.POST['description']
        )
        data.save()
        return HttpResponseRedirect('/teacher/topic_list/{}'.format(id),)
    else:
        return render(request, 'teacher/add_topic.html',context={"chapter":chapter,})

@login_required
def GetTopic(request):
    data = json.loads(request.body)
    ch_obj = Chapter.objects.get(id=data['chapter_id'])
    qs = Topic.objects.filter(chapter=ch_obj)
    t = render_to_string('teacher/add_contant_card.html',{"user":request.user,"topics":qs})
    return JsonResponse({'topics':t})

@login_required
def TopicList(request,id):
    # try:
        obj = Chapter.objects.get(id=id)
        qs = Topic.objects.filter(chapter=obj)
        return render(request, 'teacher/topic_list.html',context={'topic':qs,"chapter":obj})
    # except:
        # pass

@login_required
def AddTopicVideo(request,id):
    topic = Topic.objects.get(id=id)
    if request.method == 'POST' and request.FILES:
        
        topic.topic_video = request.FILES['topic_video']
        topic.save()
        return JsonResponse({'status':False,'message':"Error!"})
    else:
        return render(request, 'teacher/add_topic_video.html',context={"topic":topic})

@login_required
def AddTopicVideoJson(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        topic = Topic.objects.get(id=data['id'])
        topic.topic_video = data['topic_video']
        topic.save()
        return JsonResponse({'status':True,'message':"File uploaded successfully!"})
    else:
        return JsonResponse({'status':False,'message':"Error!"})

def CourseStudentList(request,id):
    cobj = Course.objects.get(id=id)
    qs = cobj.course_purchased.values('user')
    users = []
    for i in qs:
        uobj = CustomUser.objects.get(id=i['user'])
        users.append(uobj)
    context = {"course":cobj,"students":users}
    return render(request,'teacher/course_inrolled_students.html',context=context)


@login_required
def CourseFeedbackList(request,id):
    course = Course.objects.get(id=id)
    qs = Feedback.objects.filter(course=course).order_by('-rating')
    return render(request, 'teacher/course_feedback_list.html',context={'feedbacks':qs,"course":course})

def HideCourse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cobj = Course.objects.get(id=data['id'])
        cobj.hide = True
        cobj.save()
        return JsonResponse({"message": "Success"})

def ShowCourse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cobj = Course.objects.get(id=data['id'])
        ch = Chapter.objects.filter(course=cobj)
        qs = []
        for i in ch:
            ts = Topic.objects.filter(chapter=i)
            qs.extend(ts)
        if len(ch) > 0 and len(qs) > 0:
            cobj.hide = False
            cobj.save()
            return JsonResponse({"message": "Success","status":True})
        else:
            return JsonResponse({"message": "Please add Chaptors and topics","status":False})

def DeleteCourse(request, id):
    cobj = Course.objects.get(id=id)
    cobj.delete()
    print(id)
    return redirect('course_list', id=request.user.id)



def DeleteCourseLive(request, id):
    lobj = Course.objects.get(id=id)
    lobj.delete()
    return redirect('live_course', id=request.user.id)


def HideChapter(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cobj = Chapter.objects.get(id=data['id'])
        cobj.hide = True
        cobj.save()
        return JsonResponse({"message": "Success"})

def ShowChapter(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cobj = Chapter.objects.get(id=data['id'])
        cobj.hide = False
        cobj.save()
        return JsonResponse({"message": "Success","status":True})

def DeleteChapter(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cobj = Chapter.objects.get(id=data['cid'])
        cobj.delete()
        return JsonResponse({"message": "Success","status":True})

# def DeleteTopic(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         obj = Topic.objects.get(id=data['tid'])
#         obj.delete()
#         return JsonResponse({"message": "Success","status":True})


def DeleteTopic(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            obj = Topic.objects.get(id=data['tid'])
            obj.delete()
            return JsonResponse({"message": "Success", "status": True})
        except Topic.DoesNotExist:
            return JsonResponse({"message": "Topic does not exist", "status": False})
        except Exception as e:
            return JsonResponse({"message": str(e), "status": False})
    return JsonResponse({"message": "Invalid request method", "status": False})



@login_required
def CreateCourseReview(request,id):
    cobj = Course.objects.get(id=id)
    try:
        r = request.POST['rating']
    except:
        r = 0
    if request.method == "POST":
        obj = Feedback.objects.create(
            user = request.user,
            course = cobj,
            title = request.POST['title'],
            description = request.POST['description'],
            rating = r
        )
    return JsonResponse({"message": "Success","status":True})


@login_required
def UpdateCourseReview(request,id):
    
    try:
        r = request.POST['rating']
    except:
        r = 0
    if request.method == "POST":
        robj = Feedback.objects.get(id=request.POST['review'])
        robj.title = request.POST['title']
        robj.description = request.POST['description']
        robj.rating = r
        robj.save()
        return redirect('detail_course', id=id)
    else:
        return redirect('detail_course', id=id)

@login_required
def UpdateCourseReview1(request,id):
    
    try:
        r = request.POST['rating']
    except:
        r = 0
    if request.method == "POST":
        robj = Feedback.objects.get(id=request.POST['review'])
        robj.title = request.POST['title']
        robj.description = request.POST['description']
        robj.rating = r
        robj.save()
        return redirect('play_course', id=id)
    else:
        return redirect('play_course', id=id)


@login_required
def DeleteCourseReview(request, rid):
    obj = Feedback.objects.get(id=rid)
    obj.delete()
    return JsonResponse({"message": "Success","status":True})

@login_required
def CourseStatistics(request):
    user = CustomUser.objects.get(id=request.user.id)
    qs = Course.objects.filter(user=user)
    account_info = []
    for obj in qs:
        sqs = obj.course_purchased.all()
        if sqs:
            account_info = list(chain(account_info, sqs))
    return render(request, 'teacher/course_statistics.html',context={'account_info':account_info})

# def CreateInvoice(request, id):
#     po = PurchasedCourse.objects.get(id=id)
#     global client
#     client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#     trusted_order = client.order.fetch(po.order_id)
#     order_date = datetime.fromtimestamp(trusted_order['created_at'])
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
#     return render(request, 'teacher/invoice.html', mydict)

def CreateInvoice(request, id):
    po = PurchasedCourse.objects.get(id=id)
    global client
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    trusted_order = client.order.fetch(po.order_id)
    order_date = datetime.fromtimestamp(trusted_order['created_at'])
    invoice_number = get_next_invoice_number(po.user)
    gst_rate = settings.GST_RATE
    gst_price = (trusted_order['amount']/100) * gst_rate / 100
    subtotal = po.course.discount_fee
    total_price = subtotal + gst_price
    mydict={
        'orderDate': order_date,
        'user': po.user,
        'orderStatus': trusted_order['status'],
        'product': po.course,
        'invoiceNumber': invoice_number,
        'gst_rate': gst_rate,
        'gst_price': gst_price,
        'total': total_price,
    }
    return render(request, 'teacher/invoice.html', mydict)




def Planning(request):
    return render(request, 'teacher/planning.html')

def import_users(request):
    course = Course.objects.filter(user=request.user)
    imported_course = []
    for obj in course:
        pc = PurchasedCourse.objects.filter(course=obj,plateform = "imported")
        if pc:
            imported_course.append(obj)

    if request.method == 'POST':
        cobj = Course.objects.get(id=request.POST['course_id'])
        csv_file = request.FILES['user_file'].read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(csv_file)
        user_list = []
        emails = CustomUser.objects.all().values_list('email',flat=True)
        mobiles = CustomUser.objects.all().values_list('mobile',flat=True)
        for row in csv_reader:
            uobj = CustomUser(
                first_name = row['first_name'],
                last_name = row['last_name'],
                email = row['email'],
                mobile = row['mobile'],
                is_active = False,
                is_Student = True,
                plateform = "imported"
            )
            if not uobj.email in emails and not uobj.mobile in mobiles:
                user_list.append(uobj)
        
        qs = CustomUser.objects.bulk_create(user_list)
        if qs:
            pc_list = []
            for obj in qs:
                pc = PurchasedCourse(user = obj,course = cobj,valid_date=request.POST['valid_date'],plateform = "imported")
                pc_list.append(pc)
            
            PurchasedCourse.objects.bulk_create(pc_list)
        
        return HttpResponseRedirect(reverse("import_users"))

    return render(request, 'teacher/import_users.html',context={"course":course,"imported_course":imported_course})

def addSingleUser(request):
    if request.method == 'POST':
        cobj = Course.objects.get(id=request.POST['course_id'])
        uobj = CustomUser.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            mobile = request.POST['mobile'],
            is_active = False,
            is_Student = True,
            plateform = "imported"
        )   
        PurchasedCourse.objects.create(user = uobj,course = cobj,valid_date=request.POST['valid_date'],plateform = "imported")
        return HttpResponseRedirect(reverse("import_users"))
    else:
        return HttpResponseRedirect(reverse("import_users"))

def get_imported_users(request,id):
    co = Course.objects.get(id=id)
    pc = PurchasedCourse.objects.filter(course=co,plateform = "imported")
    imported_users = []
    for c in pc:
        obj = CustomUser.objects.get(id=c.user.id)
       
        imported_users.append(obj)
    return render(request, 'teacher/course_alloted_users.html',{"imported_users":imported_users})

def ApproveAllUsers(request):
    if request.method == "POST":
        data = json.loads(request.body)
        co = Course.objects.get(id=data["id"])
        pc = PurchasedCourse.objects.filter(course=co,plateform = "imported")
        for obj in pc:
            u = CustomUser.objects.get(id=obj.user.id)
            u.is_active=True
            u.save()
        return JsonResponse({"message": "Approved"})

def DeleteAllUsers(request):
    if request.method == "POST":
        data = json.loads(request.body)
        co = Course.objects.get(id=data["id"])
        pc = PurchasedCourse.objects.filter(course=co,plateform = "imported")
        for obj in pc:
            u = CustomUser.objects.get(id=obj.user.id)
            u.delete()
        return JsonResponse({"message": "Deleted"})

@login_required
def Chats(request):
    return render(request, 'teacher/chat.html',)



def viewProfile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    return render(request, 'teacher/profile.html',{'user':request.user})



def uploadProfile(request):
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
        obj.youtube_link = data['youtube_link']
        obj.instagram_link = data['instagram_link']
        obj.facebook_link = data['facebook_link']
        obj.twitter_link = data['twitter_link']
        obj.linkedin_link = data['linkedin_link']
        obj.save()
        obj.intrest_area.add(data['tags'])
        return HttpResponseRedirect(reverse("view_profile"))

def uploadProfileImage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    obj = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST": 
        obj.profile_image = request.FILES["image"]
        obj.save()
        return JsonResponse({"message": "Success",})

# Quiz Functions
# def create_quiz(request):
    
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("user_login"))
    
#     if request.method == "POST":
#         data = json.loads(request.body)
#         title = data["title"]
#         topic = Topic.objects.get(id = data["topic_id"])
#         code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
#         choices = Choices(choice = "Option 1")
#         choices.save()
#         question = Questions(question_type = "multiple choice", question= "", required= False)
#         question.save()
#         question.choices.add(choices)
#         question.save()
#         form = Form(code = code, title = title, creator=request.user, topic=topic, is_quiz=True)
#         form.save()
#         form.questions.add(question)
#         form.save()
#         return JsonResponse({"message": "Sucess", "code": code})
def create_quiz(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))

    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title", "")
        topic_id = data.get("topic_id")
        
        if not topic_id:
            return JsonResponse({"message": "Error", "error": "No topic_id provided"}, status=400)

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            return JsonResponse({"message": "Error", "error": "Topic not found"}, status=404)

        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
        choices = Choices(choice="Option 1")
        choices.save()
        question = Questions(question_type="multiple choice", question="", required=False)
        question.save()
        question.choices.add(choices)
        question.save()
        form = Form(code=code, title=title, creator=request.user, topic=topic, is_quiz=True)
        form.save()
        form.questions.add(question)
        form.save()
        return JsonResponse({"message": "Success", "code": code})






def edit_quiz(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    return render(request, "teacher/quiz/quiz_form.html", {
        "code": code,
        "form": formInfo
    })

def edit_quiz_title(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        if len(data["title"]) > 0:
            formInfo.title = data["title"]
            formInfo.save()
        else:
            formInfo.title = formInfo.title[0]
            formInfo.save()
        return JsonResponse({"message": "Success", "title": formInfo.title})

def edit_quiz_description(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        formInfo.description = data["description"]
        formInfo.save()
        return JsonResponse({"message": "Success", "description": formInfo.description})

def edit_quiz_question(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        question_id = data["id"]
        question = Questions.objects.filter(id = question_id)
        if question.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else: question = question[0]
        question.question = data["question"]
        question.required = data["required"]
        if(data.get("score")): question.score = data["score"]
        if(data.get("answer_key")): question.answer_key = data["answer_key"]
        question.save()
        return JsonResponse({'message': "Success"})

def edit_quiz_choice(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        choice_id = data["id"]
        choice = Choices.objects.filter(id = choice_id)
        if choice.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else: choice = choice[0]
        choice.choice = data["choice"]
        if(data.get('is_answer')): choice.is_answer = data["is_answer"]
        choice.save()
        return JsonResponse({'message': "Success","id":choice_id,"choice":choice.choice})



# def add_quiz_choice(request, code):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("user_login"))
#     formInfo = Form.objects.filter(code = code)
    
#     if formInfo.count() == 0:
#         return HttpResponseRedirect(reverse('404'))
#     else: formInfo = formInfo[0]
    
#     if formInfo.creator != request.user:
#         return HttpResponseRedirect(reverse("403"))
#     if request.method == "POST":
#         data = json.loads(request.body)
#         choice = Choices(choice="Option")
#         choice.save()
#         print(choice)
#         formInfo.questions.get(pk = data["question"]).choices.add(choice)
#         formInfo.save()
#         return JsonResponse({"message": "Success", "choice": choice.choice, "id": choice.id,"is_answer":choice.is_answer})
    

def add_quiz_choice(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code=code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        
        if formInfo.questions.get(pk=data["question"]).choices.count() >= 4:
            return JsonResponse({"error": "You can only add four options."}, status=400)
        choice = Choices(choice="Option")
        choice.save()
        print(choice)
        formInfo.questions.get(pk=data["question"]).choices.add(choice)
        formInfo.save()
        return JsonResponse({"message": "Success", "choice": choice.choice, "id": choice.id, "is_answer": choice.is_answer})





# def add_quiz_choice(request, code):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("user_login"))
    
#     form_info = get_object_or_404(Form, code=code)
    
#     # Checking if form creator is the current user
#     if form_info.creator != request.user:
#         return HttpResponseRedirect(reverse("403"))
    
#     if request.method == "POST":
#         data = request.POST  # Use request.POST instead of json.loads(request.body)
#         question_id = data.get("question_id")
        
#         # Fetch the question object
#         question = form_info.questions.filter(pk=question_id).first()
#         if not question:
#             return JsonResponse({"error": "Question not found."}, status=404)
        
#         # Check if the number of choices for the question is less than four
#         if question.choices.count() >= 4:
#             return JsonResponse({"error": "You can only add four options."}, status=400)
        
#         # Create a new choice object and add it to the question
#         choice = Choices.objects.create(choice="Option")
#         question.choices.add(choice)
        
#         return JsonResponse({
#             "message": "Success",
#             "choice": choice.choice,
#             "id": choice.id,
#             "is_answer": choice.is_answer
#         })
#     else:
#         return JsonResponse({"error": "Invalid request method."}, status=405)









def remove_quiz_choice(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        choice = Choices.objects.filter(pk = data["id"])
        if choice.count() == 0:
            return JsonResponse({"message": "Error"})
        else: 
            choice_id = choice[0].id
            choice = choice[0]
        choice.delete()
        return JsonResponse({"message": "Success","id":choice_id})

def add_quiz_question(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        choices = Choices(choice = "Option 1")
        choices.save()
        question = Questions(question_type = "multiple choice", question= "", required= False)
        question.save()
        question.choices.add(choices)
        question.save()
        formInfo.questions.add(question)
        formInfo.save()

        t = render_to_string('index/new_question_card.html',{"question":question})
        return JsonResponse({'question':t})

def delete_quiz_question(request, code, question):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
   
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "DELETE":
        question = Questions.objects.filter(id = question)
        if question.count() == 0: return HttpResponseRedirect(reverse("404"))
        else: question = question[0]
        for i in question.choices.all():
            i.delete()
        question.delete()
        
        return JsonResponse({"message": "Success"})

def edit_quiz_score(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if not formInfo.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args = [code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question_id = data["question_id"]
            question = formInfo.questions.filter(id = question_id)
            if question.count() == 0:
                return HttpResponseRedirect(reverse("edit_form", args = [code]))
            else: question = question[0]
            score = data["score"]
            if score == "": score = 0
            question.score = score
            question.save()
            return JsonResponse({"message": "Success"})


    
def quiz_answer_key(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if not formInfo.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args = [code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question = Questions.objects.filter(id = data["question_id"])
            if question.count() == 0: return HttpResponseRedirect(reverse("edit_form", args = [code]))
            else: question = question[0]
            if question.question_type == "short" or question.question_type == "paragraph" or question.question_type == "date" or question.question_type == "time":
                question.answer_key = data["answer_key"]
                question.save()
            else:
                for i in question.choices.all():
                    i.is_answer = False
                    i.save()
                if question.question_type == "multiple choice" or question.question_type == "dropdown":
                    choice = question.choices.get(pk = data["answer_key"])
                    choice.is_answer = True
                    choice.save()
                else:
                    for i in data["answer_key"]:
                        choice = question.choices.get(id = i)
                        choice.is_answer = True
                        choice.save()
                question.save()
            return JsonResponse({'message': "Success"})

def quiz_responses(request, code):
    formInfo = Form.objects.get(code = code)
    return render(request, "teacher/quiz/responses.html", {
        "form": formInfo,
        "responses": Responses.objects.filter(response_to = formInfo)
    })

def single_response(request, code, response_code):
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if not formInfo.allow_view_score:
        if formInfo.creator != request.user:
            return HttpResponseRedirect(reverse("403"))
    total_score = 0
    score = 0
    responseInfo = Responses.objects.filter(response_code = response_code)
    if responseInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: responseInfo = responseInfo[0]
    if formInfo.is_quiz:
        for i in formInfo.questions.all():
            total_score += i.score
        for i in responseInfo.response.all():
            if i.answer_to.question_type == "short" or i.answer_to.question_type == "paragraph" or i.answer_to.question_type == "date" or i.answer_to.question_type == "time":
                if i.answer == i.answer_to.answer_key: score += i.answer_to.score
            elif i.answer_to.question_type == "multiple choice" or i.answer_to.question_type == "dropdown":
                answerKey = None
                for j in i.answer_to.choices.all():
                    if j.is_answer: answerKey = j.id
                if answerKey is not None and int(answerKey) == int(i.answer):
                    score += i.answer_to.score
        _temp = []
        for i in responseInfo.response.all():
            if i.answer_to.question_type == "checkbox" and i.answer_to.pk not in _temp:
                answers = []
                answer_keys = []
                for j in responseInfo.response.filter(answer_to__pk = i.answer_to.pk):
                    answers.append(int(j.answer))
                    for k in j.answer_to.choices.all():
                        if k.is_answer and k.pk not in answer_keys: answer_keys.append(k.pk)
                    _temp.append(i.answer_to.pk)
                if answers == answer_keys: score += i.answer_to.score
    return render(request, "teacher/quiz/response.html", {
        "form": formInfo,
        "response": responseInfo,
        "score": score,
        "total_score": total_score
    })


def create_form(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title", "")
            topic_id = data.get("topic_id")
            if not topic_id:
                return JsonResponse({"error": "Topic ID is required"}, status=400)
            
            topic = Topic.objects.get(id=topic_id)
            code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
            choices = Choices(choice="Option 1")
            choices.save()
            question = Questions(question_type="multiple choice", question="", required=False)
            question.save()
            question.choices.add(choices)
            question.save()
            form = Form(code=code, title=title, creator=request.user, topic=topic)
            form.save()
            form.questions.add(question)
            form.save()
            return JsonResponse({"message": "Success", "code": code})
        except Topic.DoesNotExist:
            return JsonResponse({"error": "Topic not found"}, status=404)
        except KeyError as e:
            return JsonResponse({"error": f"Missing key: {str(e)}"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)






# def edit_form(request, code):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("user_login"))
#     formInfo = Form.objects.filter(code = code)
   
#     if formInfo.count() == 0:
#         return HttpResponseRedirect(reverse("404"))
#     else: formInfo = formInfo[0]
    
#     if formInfo.creator != request.user:
#         return HttpResponseRedirect(reverse("403"))
#     return render(request, "index/form.html", {
#         "code": code,
#         "form": formInfo
#     })

def edit_form(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code=code)
   
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        formInfo = formInfo.first()
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    return render(request, "index/form.html", {
        "code": code,
        "form": formInfo
    })



def edit_title(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        if len(data["title"]) > 0:
            formInfo.title = data["title"]
            formInfo.save()
        else:
            formInfo.title = formInfo.title[0]
            formInfo.save()
        return JsonResponse({"message": "Success", "title": formInfo.title})

def edit_description(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        formInfo.description = data["description"]
        formInfo.save()
        return JsonResponse({"message": "Success", "description": formInfo.description})

def edit_bg_color(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        formInfo.background_color = data["bgColor"]
        formInfo.save()
        return JsonResponse({"message": "Success", "bgColor": formInfo.background_color})

def edit_text_color(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        formInfo.text_color = data["textColor"]
        formInfo.save()
        return JsonResponse({"message": "Success", "textColor": formInfo.text_color})

def edit_setting(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        formInfo.collect_email = data["collect_email"]
        formInfo.is_quiz = data["is_quiz"]
        formInfo.authenticated_responder = data["authenticated_responder"]
        formInfo.confirmation_message = data["confirmation_message"]
        formInfo.edit_after_submit = data["edit_after_submit"]
        formInfo.allow_view_score = data["allow_view_score"]
        formInfo.save()
        return JsonResponse({'message': "Success"})

def delete_form(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "DELETE":
        
        for i in formInfo.questions.all():
            for j in i.choices.all():
                j.delete()
            i.delete()
        for i in Responses.objects.filter(response_to = formInfo):
            for j in i.response.all():
                j.delete()
            i.delete()
        formInfo.delete()
        return JsonResponse({'message': "Success"})

def edit_question(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        question_id = data["id"]
        question = Questions.objects.filter(id = question_id)
        if question.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else: question = question[0]
        question.question = data["question"]
        question.question_type = data["question_type"]
        question.required = data["required"]
        if(data.get("score")): question.score = data["score"]
        if(data.get("answer_key")): question.answer_key = data["answer_key"]
        question.save()
        return JsonResponse({'message': "Success"})

# def edit_choice(request, code):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("user_login"))
#     formInfo = Form.objects.filter(code = code)
#     #Checking if form exists
#     if formInfo.count() == 0:
#         return HttpResponseRedirect(reverse('404'))
#     else: formInfo = formInfo[0]
#     #Checking if form creator is user
#     if formInfo.creator != request.user:
#         return HttpResponseRedirect(reverse("403"))
#     if request.method == "POST":
#         data = json.loads(request.body)
#         choice_id = data["id"]
#         choice = Choices.objects.filter(id = choice_id)
#         if choice.count() == 0:
#             return HttpResponseRedirect(reverse("404"))
#         else: choice = choice[0]
#         choice.choice = data["choice"]
#         if(data.get('is_answer')): choice.is_answer = data["is_answer"]
#         choice.save()
#         return JsonResponse({'message': "Success"})
def edit_choice(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    
    form_info = get_object_or_404(Form, code=code)
    
    # Checking if form creator is the current user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    
    if request.method == "POST":
        data = json.loads(request.body)
        choice_id = data.get("id")
        choice = Choices.objects.filter(id=choice_id).first()
        
        if not choice:
            return HttpResponseRedirect(reverse("404"))
        
        # Check if the number of choices for the question is less than four
        if form_info.questions.filter(choices=choice).count() >= 4:
            return JsonResponse({"error": "You can only have four options."}, status=400)
        
        choice.choice = data["choice"]
        if data.get('is_answer'):
            choice.is_answer = data["is_answer"]
        choice.save()
        
        return JsonResponse({"message": "Success"})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
def add_choice(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        choice = Choices(choice="Option")
        choice.save()
        formInfo.questions.get(pk = data["question"]).choices.add(choice)
        formInfo.save()
        return JsonResponse({"message": "Success", "choice": choice.choice, "id": choice.id})
    

# def add_choice(request, code):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("user_login"))
    
#     form_info = Form.objects.filter(code=code).first()
    
#     # Checking if form exists
#     if not form_info:
#         return HttpResponseRedirect(reverse('404'))
    
#     # Checking if form creator is user
#     if form_info.creator != request.user:
#         return HttpResponseRedirect(reverse("403"))
    
#     if request.method == "POST":
#         data = json.loads(request.body)
#         question = form_info.questions.filter(pk=data["question"]).first()
        
#         if not question:
#             return JsonResponse({"error": "Question does not exist."}, status=400)
        
#         # Check if the number of choices for the question is equal to four
#         if question.choices.count() >= 4:
#             return JsonResponse({"error": "You can only add four options."}, status=400)
        
#         # Check if the choice data is valid
#         if "choice" not in data:
#             return JsonResponse({"error": "Choice data is missing."}, status=400)
        
#         choice = Choices(choice=data["choice"])
#         choice.save()
#         question.choices.add(choice)
#         form_info.save()
#         return JsonResponse({"message": "Success", "choice": choice.choice, "id": choice.id})
    
#     return JsonResponse({"error": "Invalid request method."}, status=400)

def remove_choice(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        choice = Choices.objects.filter(pk = data["id"])
        if choice.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else: choice = choice[0]
        choice.delete()
        return JsonResponse({"message": "Success"})

def get_choice(request, code, question):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "GET":
        question = Questions.objects.filter(id = question)
        if question.count() == 0: return HttpResponseRedirect(reverse('404'))
        else: question = question[0]
        choices = question.choices.all()
        choices = [{"choice":i.choice, "is_answer":i.is_answer, "id": i.id} for i in choices]
        return JsonResponse({"choices": choices, "question": question.question, "question_type": question.question_type, "question_id": question.id})

def add_question(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        choices = Choices(choice = "Option 1")
        choices.save()
        question = Questions(question_type = "multiple choice", question= "Untitled Question", required= False)
        question.save()
        question.choices.add(choices)
        question.save()
        formInfo.questions.add(question)
        formInfo.save()
        return JsonResponse({'question': {'question': "Untitled Question", "question_type": "multiple choice", "required": False, "id": question.id}, 
        "choices": {"choice": "Option 1", "is_answer": False, 'id': choices.id}})

def delete_question(request, code, question):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "DELETE":
        question = Questions.objects.filter(id = question)
        if question.count() == 0: return HttpResponseRedirect(reverse("404"))
        else: question = question[0]
        for i in question.choices.all():
            i.delete()
        question.delete()

        return JsonResponse({"message": "Success"})
    


# def score(request, code):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("user_login"))
#     formInfo = Form.objects.filter(code = code)
#     #Checking if form exists
#     if formInfo.count() == 0:
#         return HttpResponseRedirect(reverse('404'))
#     else: formInfo = formInfo[0]
#     #Checking if form creator is user
#     if formInfo.creator != request.user:
#         return HttpResponseRedirect(reverse("403"))
    
#     if not formInfo.is_quiz:
#         return HttpResponseRedirect(reverse("edit_form", args = [code]))
#     else:
#         return render(request, "index/score.html", {"form": formInfo})


# def edit_score(request, code):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("user_login"))
#     formInfo = Form.objects.filter(code = code)
#     #Checking if form exists
#     if formInfo.count() == 0:
#         return HttpResponseRedirect(reverse('404'))
#     else: formInfo = formInfo[0]
#     #Checking if form creator is user
#     if formInfo.creator != request.user:
#         return HttpResponseRedirect(reverse("403"))
#     if not formInfo.is_quiz:
#         return HttpResponseRedirect(reverse("edit_form", args = [code]))
#     else:
#         if request.method == "POST":
#             data = json.loads(request.body)
#             question_id = data["question_id"]
#             question = formInfo.questions.filter(id = question_id)
#             if question.count() == 0:
#                 return HttpResponseRedirect(reverse("edit_form", args = [code]))
#             else: question = question[0]
#             score = data["score"]
#             if score == "": score = 0
#             question.score = score
#             question.save()
#             return JsonResponse({"message": "Success"})

def score(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    
    form_info = Form.objects.filter(code=code).first()
    
    # Check if the form exists
    if not form_info:
        return HttpResponseRedirect(reverse('404'))
    
    # Check if the form creator is the current user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    
    # Check if the form is a quiz
    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        return render(request, "index/score.html", {"form": form_info})

# def edit_score(request, code):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("user_login"))
    
#     form_info = Form.objects.filter(code=code).first()
    
#     # Check if the form exists
#     if not form_info:
#         return HttpResponseRedirect(reverse('404'))
    
#     # Check if the form creator is the current user
#     if form_info.creator != request.user:
#         return HttpResponseRedirect(reverse("403"))
    
#     # Check if the form is a quiz
#     if not form_info.is_quiz:
#         return HttpResponseRedirect(reverse("edit_form", args=[code]))
#     else:
#         if request.method == "POST":
#             data = json.loads(request.body)
#             question_id = data["question_id"]
#             question = form_info.questions.filter(id=question_id).first()
#             if not question:
#                 return HttpResponseRedirect(reverse("edit_form", args=[code]))
#             else:
#                 score = data["score"]
#                 if score == "":
#                     score = 0
#                 question.score = score
#                 question.save()
#                 return JsonResponse({"message": "Success"})
#         else:
#             return JsonResponse({"error": "Invalid request method."}, status=405)

def edit_score(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    
    form_info = Form.objects.filter(code=code).first()
    
    # Check if the form exists
    if not form_info:
        return HttpResponseRedirect(reverse('404'))
    
    # Check if the form creator is the current user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    
    # Check if the form is a quiz
    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            score = data.get("score")
            if score == "":
                score = 0
            # Update scores for all questions in the form
            form_info.questions.update(score=score)
            return JsonResponse({"message": "Success"})
        else:
            return JsonResponse({"error": "Invalid request method."}, status=405)


def view_score(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    
    form_info = Form.objects.filter(code=code).first()
    
    # Check if the form exists
    if not form_info:
        return HttpResponseRedirect(reverse('404'))
    
    # Check if the form creator is the current user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    
    # Check if the form is a quiz
    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        return render(request, "index/score.html", {"form": form_info})


def update_score(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    
    form_info = Form.objects.filter(code=code).first()
    
    # Check if the form exists
    if not form_info:
        return HttpResponseRedirect(reverse('404'))
    
    # Check if the form creator is the current user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    
    # Check if the form is a quiz
    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                score = data.get("score")
                if score == "":
                    score = 0
                else:
                    score = int(score)  # Ensure score is an integer
                # Update scores for all questions in the form
                form_info.questions.update(score=score)
                return JsonResponse({"message": "Success"})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)  # Return error message
        else:
            return JsonResponse({"error": "Invalid request method."}, status=405)

def answer_key(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if not formInfo.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args = [code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question = Questions.objects.filter(id = data["question_id"])
            if question.count() == 0: return HttpResponseRedirect(reverse("edit_form", args = [code]))
            else: question = question[0]
            if question.question_type == "short" or question.question_type == "paragraph" or question.question_type == "date" or question.question_type == "time":
                question.answer_key = data["answer_key"]
                question.save()
            else:
                for i in question.choices.all():
                    i.is_answer = False
                    i.save()
                if question.question_type == "multiple choice" or question.question_type == "dropdown":
                    choice = question.choices.get(pk = data["answer_key"])
                    choice.is_answer = True
                    choice.save()
                else:
                    for i in data["answer_key"]:
                        choice = question.choices.get(id = i)
                        choice.is_answer = True
                        choice.save()
                question.save()
            return JsonResponse({'message': "Success"})

def feedback(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if not formInfo.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args = [code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question = formInfo.questions.get(id = data["question_id"])
            question.feedback = data["feedback"]
            question.save()
            return JsonResponse({'message': "Success"})

def preview_form(request, code):
    formInfo = Form.objects.filter(code = code)
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    if formInfo.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("user_login"))
    return render(request, "teacher/quiz/preview.html", {
        "form": formInfo
    })

def view_form(request, code):
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    if formInfo.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("user_login"))
    try:
        responseInfo = Responses.objects.filter(response_to=formInfo,responder=request.user)
        total_score = 0
        score = 0
        
        if responseInfo.count() == 0:
            return HttpResponseRedirect(reverse('404'))
        else: responseInfo = responseInfo[0]
        if formInfo.is_quiz:
            for i in formInfo.questions.all():
                total_score += i.score
            for i in responseInfo.response.all():
                if i.answer_to.question_type == "short" or i.answer_to.question_type == "paragraph" or i.answer_to.question_type == "date" or i.answer_to.question_type == "time":
                    if i.answer == i.answer_to.answer_key: score += i.answer_to.score
                elif i.answer_to.question_type == "multiple choice" or i.answer_to.question_type == "dropdown":
                    answerKey = None
                    for j in i.answer_to.choices.all():
                        if j.is_answer: answerKey = j.id
                    if answerKey is not None and int(answerKey) == int(i.answer):
                        score += i.answer_to.score
            _temp = []
            for i in responseInfo.response.all():
                if i.answer_to.question_type == "checkbox" and i.answer_to.pk not in _temp:
                    answers = []
                    answer_keys = []
                    for j in responseInfo.response.filter(answer_to__pk = i.answer_to.pk):
                        answers.append(int(j.answer))
                        for k in j.answer_to.choices.all():
                            if k.is_answer and k.pk not in answer_keys: answer_keys.append(k.pk)
                        _temp.append(i.answer_to.pk)
                    if answers == answer_keys: score += i.answer_to.score
        else:
            pass
        
        return render(request, "index/form_response.html", {
            "form": formInfo,
            "response": responseInfo,
            "score": score,
            "total_score": total_score
        })
    except:
        return render(request, "teacher/quiz/quiz_submit_form.html", {"form": formInfo})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def submit_form(request, code):
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    if formInfo.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("user_login"))
    if request.method == "POST":
        rcode = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(20))
        response = Responses(response_code = rcode, response_to = formInfo, responder_ip = get_client_ip(request),responder = request.user, responder_email=request.user.email)
        response.save()
        
        for i in request.POST:
            
            if i == "csrfmiddlewaretoken" or i == "email-address":
                continue
            question = formInfo.questions.get(id = i)
            for j in request.POST.getlist(i):
                answer = Answer(answer = j, answer_to = question)
                answer.save()
                response.response.add(answer)
                response.save()
        
        for f in request.FILES:
            if f == "csrfmiddlewaretoken" or f == "email-address":
                continue
            question = formInfo.questions.get(id = f)
            for ff in request.FILES.getlist(f):
                answer = Answer(file = ff, answer_to = question)
                answer.save()
                response.response.add(answer)
                response.save()

        # topic_progress = TopicProgress.objects.get(topic=formInfo.topic,user=request.user)
        # topic_progress.progress +=25
        # topic_progress.save()
        # updateChapterProgress(cid=formInfo.topic.chapter.id,uid=request.user.id)
        return redirect('view_form', code=code)

def responses(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]

    responsesSummary = []
    choiceAnswered = {}
    filteredResponsesSummary = {}
    for question in formInfo.questions.all():
        answers = Answer.objects.filter(answer_to = question.id)
        if question.question_type == "multiple choice" or question.question_type == "checkbox":
            choiceAnswered[question.question] = choiceAnswered.get(question.question, {})
            for answer in answers:
                choice = answer.answer_to.choices.get(id = answer.answer).choice
                choiceAnswered[question.question][choice] = choiceAnswered.get(question.question, {}).get(choice, 0) + 1
        responsesSummary.append({"question": question, "answers":answers })
    for answr in choiceAnswered:
        filteredResponsesSummary[answr] = {}
        keys = choiceAnswered[answr].values()
        for choice in choiceAnswered[answr]:
            filteredResponsesSummary[answr][choice] = choiceAnswered[answr][choice]
    
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    return render(request, "index/responses.html", {
        "form": formInfo,
        "responses": Responses.objects.filter(response_to = formInfo),
        "responsesSummary": responsesSummary,
        "filteredResponsesSummary": filteredResponsesSummary
    })

def retrieve_checkbox_choices(response, question):
    checkbox_answers = []

    answers = Answer.objects.filter(answer_to=question, response=response)
    for answer in answers:
        selected_choice_ids = answer.answer.split(',')  # Split the string into individual choice IDs
        selected_choices = Choices.objects.filter(pk__in=selected_choice_ids)
        checkbox_answers.append([choice.choice for choice in selected_choices])

    return checkbox_answers

def exportcsv(request,code):
    formInfo = Form.objects.filter(code = code)
    formInfo = formInfo[0]
    responses=Responses.objects.filter(response_to = formInfo)
    questions = formInfo.questions.all()


    http_response = HttpResponse()
    http_response['Content-Disposition'] = f'attachment; filename= {formInfo.title}.csv'
    writer = csv.writer(http_response)
    header = ['Response Code', 'Responder', 'Responder Email','Responder_ip']
    
    
    for question in questions:
        header.append(question.question)
    
    writer.writerow(header)

    for response in responses:
        response_data = [
        response.response_code,
        response.responder.email if response.responder else 'Anonymous',
        response.responder_email if response.responder_email else '',
        response.responder_ip if response.responder_ip else ''
    ]
        for question in questions:
            answer = Answer.objects.filter(answer_to=question, response=response).first()
            
        
            if  question.question_type not in ['multiple choice','checkbox']:
                response_data.append(answer.answer if answer else '')
            elif question.question_type == "multiple choice":
                response_data.append(answer.answer_to.choices.get(id = answer.answer).choice if answer else '')
            elif question.question_type == "checkbox":
                if answer and question.question_type == 'checkbox':
                    checkbox_choices = retrieve_checkbox_choices(response,answer.answer_to)
                    response_data.append(checkbox_choices)
        writer.writerow(response_data)
        
    return http_response

def response(request, code, response_code):
    formInfo = Form.objects.filter(code = code)
    
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    
    if not formInfo.allow_view_score:
        if formInfo.creator != request.user:
            return HttpResponseRedirect(reverse("403"))
    total_score = 0
    score = 0
    responseInfo = Responses.objects.filter(response_code = response_code)
    if responseInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: responseInfo = responseInfo[0]
    if formInfo.is_quiz:
        for i in formInfo.questions.all():
            total_score += i.score
        for i in responseInfo.response.all():
            if i.answer_to.question_type == "short" or i.answer_to.question_type == "paragraph" or i.answer_to.question_type == "date" or i.answer_to.question_type == "time":
                if i.answer == i.answer_to.answer_key: score += i.answer_to.score
            elif i.answer_to.question_type == "multiple choice" or i.answer_to.question_type == "dropdown":
                answerKey = None
                for j in i.answer_to.choices.all():
                    if j.is_answer: answerKey = j.id
                if answerKey is not None and int(answerKey) == int(i.answer):
                    score += i.answer_to.score
        _temp = []
        for i in responseInfo.response.all():
            if i.answer_to.question_type == "checkbox" and i.answer_to.pk not in _temp:
                answers = []
                answer_keys = []
                for j in responseInfo.response.filter(answer_to__pk = i.answer_to.pk):
                    answers.append(int(j.answer))
                    for k in j.answer_to.choices.all():
                        if k.is_answer and k.pk not in answer_keys: answer_keys.append(k.pk)
                    _temp.append(i.answer_to.pk)
                if answers == answer_keys: score += i.answer_to.score
    return render(request, "index/response.html", {
        "form": formInfo,
        "response": responseInfo,
        "score": score,
        "total_score": total_score
    })

def edit_response(request, code, response_code):
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    response = Responses.objects.filter(response_code = response_code, response_to = formInfo)
    if response.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: response = response[0]
    if formInfo.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("user_login"))
        if response.responder != request.user:
            return HttpResponseRedirect(reverse('403'))
    if request.method == "POST":
        if formInfo.authenticated_responder and not response.responder:
            response.responder = request.user
            response.save()
        if formInfo.collect_email:
            response.responder_email = request.POST["email-address"]
            response.save()
        #Deleting all existing answers
        for i in response.response.all():
            i.delete()
        for i in request.POST:
            #Excluding csrf token and email address
            if i == "csrfmiddlewaretoken" or i == "email-address":
                continue
            question = formInfo.questions.get(id = i)
            for j in request.POST.getlist(i):
                answer = Answer(answer=j, answer_to = question)
                answer.save()
                response.response.add(answer)
                response.save()
        if formInfo.is_quiz:
            return HttpResponseRedirect(reverse("response", args = [formInfo.code, response.response_code]))
        else:
            return render(request, "index/form_response.html", {
                "form": formInfo,
                "code": response.response_code
            })
    return render(request, "index/edit_response.html", {
        "form": formInfo,
        "response": response
    })

def delete_responses(request, code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("user_login"))
    formInfo = Form.objects.filter(code = code)
    #Checking if form exists
    if formInfo.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else: formInfo = formInfo[0]
    #Checking if form creator is user
    if formInfo.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "DELETE":
        responses = Responses.objects.filter(response_to = formInfo)
        for response in responses:
            for i in response.response.all():
                i.delete()
            response.delete()
        return JsonResponse({"message": "Success"})
# end custom google form views



class CalendarView(generic.ListView):
    model = Event
    template_name = 'teacher/calendar.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     # use today's date for the calendar
    #     d = get_date(self.request.GET.get('month', None))

    #     # Instantiate our calendar class with today's year and date
    #     calc = Calendar(d.year, d.month)
    #     colored_day = '\033[92m' + str(d.day) + '\033[0m'

    #     # Call the formatmonth method, which returns our calendar as a table
    #     html_cal = calc.formatmonth(withyear=True)
    #     context['calendar'] = mark_safe(html_cal)
    #     d = get_date(self.request.GET.get('month', None))
    #     context['prev_month'] = prev_month(d)
    #     context['next_month'] = next_month(d)
    #     context['form'] = EventForm()
    #     return context
    

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {   "id": event.id,
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "description": event.description,
                }
            )
        
        context = {"events": event_list,"events_month": events_month}
        return render(request, self.template_name, context)

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.today()
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
        instance.title = request.POST['title']
        instance.description = request.POST['description']
        instance.start_time = request.POST['start_time']
        instance.end_time = request.POST['end_time']
        instance.save()
        return HttpResponseRedirect(reverse('calendar'))
    else:
        instance = Event()
        instance.user = request.user
        instance.title = request.POST['title']
        instance.description = request.POST['description']
        instance.start_time = request.POST['start_time']
        instance.end_time = request.POST['end_time']
        instance.save()
        # form = EventForm(request.POST or None, instance=instance)
        # if request.POST and form.is_valid():
        #     form.save()
        return HttpResponseRedirect(reverse('calendar'))
    
def deleteEvent(request, event_id=None):
    instance = get_object_or_404(Event, pk=event_id).delete()
    return HttpResponseRedirect(reverse('calendar'))



@require_POST
def approve_course(request):
    course_id = request.POST.get('course_id')
    try:
        course = Course.objects.get(id=course_id)
        course.approved = True
        course.save()
        return JsonResponse({'success': True, 'status': 'approved'})  
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found'})



@require_POST
def hide_course(request):
    course_id = request.POST.get('course_id')
    try:
        course = Course.objects.get(id=course_id)
        course.hide = True
        course.save()
        return JsonResponse({'success': True, 'status': 'hidded'})  
    except Course.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Course not found'})
    

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'admin/course_detail.html', {'course': course})

def monthly_earning_view(request):
   
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    start_of_month = datetime(current_year, current_month, 1)
    end_of_month = datetime(current_year, current_month + 1, 1) - timedelta(days=1)

    start_timestamp = int(start_of_month.timestamp())
    end_timestamp = int(end_of_month.timestamp())

    all_payments = client.payment.all(
        {"from": start_timestamp, "to": end_timestamp}
    )
    # print('total pament',all_payments)

    total_amount = sum(int(payment['amount']) for payment in all_payments['items'])

    return JsonResponse({'monthly_earning': total_amount/100})




def yearly_earning_view(request):
    
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    current_year = datetime.now().year

    start_of_year = datetime(current_year, 1, 1)
    end_of_year = datetime(current_year, 12, 31, 23, 59, 59)  

    start_timestamp = int(start_of_year.timestamp())
    end_timestamp = int(end_of_year.timestamp())

    all_payments = client.payment.all(
        {"from": start_timestamp, "to": end_timestamp}
    )
    # print('total pament',all_payments)


    total_amount = sum(int(payment['amount']) for payment in all_payments['items'])

    return JsonResponse({'yearly_earning': total_amount / 100})



def course_chapter(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
                
        chapters = Chapter.objects.filter(course=course)
        
        print(f"Course: {course.course_name}")
        for chapter in chapters:
            print(f"Chapter: {chapter.chapter_name}")
           
        return render(request, 'admin/course_chapter.html', {'course': course, 'chapters': chapters})
    
    except Course.DoesNotExist:
        return render(request, 'error.html', {'message': 'Course not found'})
    
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
    

    
def ChapterTopicList(request, id):
    try:
        chapter_obj = Chapter.objects.get(id=id)
        topic_qs = Topic.objects.filter(chapter=chapter_obj)
        print(topic_qs) 
        return render(request, 'admin/ChapterTopicList.html', context={'topic': topic_qs, 'chapter': chapter_obj})
    except Chapter.DoesNotExist:
        return render(request, 'error.html', {'message': 'Chapter not found'})
    


def chapter_quizzes(request, chapter_id, topic_id=None):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    topic = None
    quizzes = Form.objects.filter(topic__chapter=chapter, is_quiz=True)

    if topic_id:
        topic = get_object_or_404(Topic, pk=topic_id, chapter=chapter)
        quizzes = quizzes.filter(topic=topic)
    
    for quiz in quizzes:
        #print(f"Quiz: {quiz.title}")
        for question in quiz.questions.all():
            correct_answers = question.choices.filter(is_answer=True)
            if correct_answers.exists():
                for answer in correct_answers:
                     print(answer.choice)
                # print()  # Add an empty line between questions

    return render(request, 'admin/chapter_quizzes.html', {'chapter': chapter, 'topic': topic, 'quizzes': quizzes})


def chapter_assignments(request, chapter_id, topic_id=None):
    try:
        chapter = Chapter.objects.get(id=chapter_id)
        
        if topic_id is not None:
            assignments = Form.objects.filter(topic_id=topic_id, topic__chapter=chapter, is_quiz=False)
        else:
            assignments = Form.objects.filter(topic__chapter=chapter, is_quiz=False)
        
        return render(request, 'admin/chapter_assignments.html', {'chapter': chapter, 'assignments': assignments})
    
    except Chapter.DoesNotExist:
        return render(request, 'error.html', {'message': 'Chapter not found'})
    
    except Exception as e:
        return render(request, 'error.html', {'message': str(e)})
    


login_required
def super_admin_purchased_courses(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    purchased_courses = PurchasedCourse.objects.filter(user=user)
    for purchased_course in purchased_courses:
            if purchased_course.course.type == 'Pre Recorded':
                purchased_course.total_price_with_gst = purchased_course.course.discount_fee + \
                                                    (settings.GST_RATE * purchased_course.course.discount_fee) / 100
                
            else:
                purchased_course.total_price_with_gst = purchased_course.course.fees + \
                                                    (settings.GST_RATE * purchased_course.course.fees) / 100
               
        
    return render(request, 'admin/user_purchased_courses.html', {'user': user, 'purchased_courses': purchased_courses})
    





# def update_kyc_details(request):
#     if request.method == 'POST':
#         kyc_type = request.POST.get('kycType')
#         kyc_number = request.POST.get('kycNumber')
#         kyc_mobile = request.POST.get('kycMobile')
        
#         try:
#             user_kyc = UserKYC.objects.get(user=request.user, kyc_name=kyc_type)
#         except UserKYC.DoesNotExist:
#             user_kyc = UserKYC(user=request.user, kyc_name=kyc_type)

#         user_kyc.kyc_doc_number = kyc_number
#         user_kyc.linked_number = kyc_mobile

#         user_kyc.save()

#         messages.success(request, f'{kyc_type} details updated successfully!')
#         return redirect('view_profile') 

#     else:
#         messages.error(request, 'Invalid request method!')
#         return redirect('view_profile')


def update_kyc_details(request):
    if request.method == 'POST':
        kyc_type = request.POST.get('kycType')
        kyc_number = request.POST.get('kycNumber')
        kyc_mobile = request.POST.get('kycMobile')
        kyc_front_image = request.FILES.get('kycFrontImage')
        kyc_back_image = request.FILES.get('kycBackImage')
        
        # Get the existing KYC record if it exists
        try:
            user_kyc = UserKYC.objects.get(user=request.user, kyc_name=kyc_type)
        except UserKYC.DoesNotExist:
            user_kyc = UserKYC(user=request.user, kyc_name=kyc_type)

        # Update KYC details
        user_kyc.kyc_doc_number = kyc_number
        user_kyc.linked_number = kyc_mobile

        # Update images if provided
        if kyc_front_image:
            user_kyc.kyc_image_front = kyc_front_image
        if kyc_back_image:
            user_kyc.kyc_image_back = kyc_back_image

        user_kyc.save()

        messages.success(request, f'{kyc_type} details updated successfully!')
        return redirect('view_profile') 

    else:
        messages.error(request, 'Invalid request method!')
        return redirect('view_profile')
    

    

def update_education_details(request):
    user = request.user
    education_details = Education.objects.filter(user=user).first() 

    if request.method == 'POST':
       
        institution_name = request.POST.get('institutionName')
        institution_address = request.POST.get('institutionAddress')
        subject = request.POST.get('subject')
        grade = request.POST.get('grade')
        year = request.POST.get('year')

       
        if education_details:
            education_details.institution_name = institution_name
            education_details.institution_address = institution_address
            education_details.subject = subject
            education_details.grade = grade
            education_details.year = year
            education_details.save()
        else:
            Education.objects.create(
                user=user,
                institution_name=institution_name,
                institution_address=institution_address,
                subject=subject,
                grade=grade,
                year=year
            )

        return redirect('view_profile') 

    else:
        
        context = {
            'education_details': education_details
        }
        return redirect('view_profile')
    

def update_bank_details(request):
    user = request.user
    bank_details = Banks.objects.filter(user=user).first()  # Assuming each user has only one bank record

    if request.method == 'POST':
      
        bank_name = request.POST.get('bankName')
        account_number = request.POST.get('accountNumber')
        ifsc_code = request.POST.get('ifscCode')
        account_holder = request.POST.get('accountHolder')
        mobile_number = request.POST.get('mobileNumber')

        
        if bank_details:
            bank_details.bank_name = bank_name
            bank_details.account_number = account_number
            bank_details.ifsc_code = ifsc_code
            bank_details.account_name = account_holder
            bank_details.phone_number = mobile_number
            bank_details.save()
        else:
            Banks.objects.create(
                user=user,
                bank_name=bank_name,
                account_number=account_number,
                ifsc_code=ifsc_code,
                account_name=account_holder,
                phone_number=mobile_number
            )

        
        return redirect('view_profile') 

    else:
        
        context = {
            'bank_details': bank_details
        }
        return redirect('view_profile')
    

def calculate_total_revenue():
    # Get all the purchased courses
    purchased_courses = PurchasedCourse.objects.all()

    # Initialize total revenue
    total_revenue = 0

    # Iterate through purchased courses and sum up the prices
    for purchased_course in purchased_courses:
        total_revenue += purchased_course.course.price

    return total_revenue




