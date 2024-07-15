
from collections import UserDict
from itertools import chain
from .models import *
from django.db.models import Sum
from .models import WalletTransaction
import datetime
# import razorpay
# from razorpay.resources import Payment
# from django.conf import settings



def total_enroll(request):
    if request.user.is_authenticated:
        qs = Course.objects.filter(user = CustomUser.objects.get(id=request.user.id))
        
        account_info = []
        for obj in qs:
            sqs = obj.course_purchased.all()
            if sqs:
                account_info = list(chain(account_info, sqs))
        return {"total_enroll":len(account_info)}
    else:
        return {"total_course":0}
    

def recent_courses(request):
    recent_courses = Course.objects.filter(type='Pre Recorded').order_by('-created_at')[:5]
    return {'recent_courses': recent_courses}



def live_courses(request):
    live_courses = Course.objects.filter(type='Live').order_by('-created_at')[:5]
    return {'live_courses': live_courses}




def enrolled_teachers_count(request):
    enrolled_teachers_count = CustomUser.objects.filter(is_Teacher=True).count()
    return {'enrolled_teachers_count': enrolled_teachers_count}

