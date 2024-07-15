
from django.db.models import Count
from teacher.models import *

def topCategories(request):
    course = PurchasedCourse.objects.values("course")
    course_counts = course.annotate(count=Count("course"))
    sorted_courses = sorted(course_counts, key=lambda x: x['count'],reverse=True)
    qs = []
    for c in sorted_courses:
        co = Course.objects.get(id=c['course'])
        cc = CourseCategory.objects.get(id=co.category.id)
        qs.append(cc)
    return {"topCategories":list(set(qs))}

def availableOffers(request):
    return {"global_coupons":Coupon.objects.all()}

def notification_count(request):
    unread_count = Notification.objects.filter(user=request.user.id,viewed=False).order_by("-timestamp")
    return {"unread_count":unread_count}

def cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        cart_count = cart_items.count()
    else:
        cart_count = 0  
    return {'cart_count': cart_count}


