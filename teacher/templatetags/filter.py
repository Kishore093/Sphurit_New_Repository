from django import template
register = template.Library()
from teacher.models import*
from core.models import*
from chats.models import*

@register.filter
def is_quiz(qs, value):
    return qs.filter(is_quiz=value)

@register.filter
def course_filter(qs): 
    return qs.filter(hide=False,approved=True, type='Pre Recorded')

@register.filter
def get_course_progress(value,user):
    cobj = Course.objects.get(id=value)
    try:
        uobj = CustomUser.objects.get(id=user.id)
        try:
            obj = CourseProgress.objects.get(course=cobj,user=uobj)
            return int(obj.progress)
        except:
            return 0
    except:
        return 0

@register.filter
def get_chapter_progress(value,user):
    cobj = Chapter.objects.get(id=value)
    try:
        uobj = CustomUser.objects.get(id=user.id)
        try:
            obj = ChapterProgress.objects.get(chapter=cobj,user=uobj)
            return int(obj.progress)
        except:
            return 0
    except:
        return 0

@register.filter
def get_topic_progress(value,user):
    tobj = Topic.objects.get(id=value)
    try:
        uobj = CustomUser.objects.get(id=user.id)
        try:
            obj = TopicProgress.objects.get(topic=tobj,user=uobj)
            return int(obj.progress)
        except:
            return 0
    except:
        return 0

@register.filter
def is_reviewed(value,user):
    cobj = Course.objects.get(id=value)
    try:
        uobj = CustomUser.objects.get(id=user.id)
        try:
            Feedback.objects.get(course=cobj,user=uobj)
            return True
        except:
            return False
    except:
        return False

@register.filter
def is_purchased(value,user):
    cobj = Course.objects.get(id=value)
    try:
        uobj = CustomUser.objects.get(id=user.id)
        try:
            PurchasedCourse.objects.get(course=cobj,user=uobj)
            return True
        except:
            return False
    except:
        return False
    
@register.filter
def is_course_coupon_applied(value,user):
    cobj = Course.objects.get(id=value)
    try:
        uobj = CustomUser.objects.get(id=user.id)
        if cobj.coupon_applied_by.contains(uobj):
            return True
        else:
            return False
    except:
        return False

@register.filter
def has_course(value):
    cat = CourseCategory.objects.get(id=value)
    cobj = Course.objects.filter(category=cat,hide=False,approved=True)
    if cobj:
        return True
    else:
        return False
    
@register.filter
def is_cart(value,user):
    cobj = Course.objects.get(id=value)
    try:
        uobj = CustomUser.objects.get(id=user.id)
        c = Cart.objects.get(user=uobj)
        ci = CartItem.objects.filter(cart=c,course=cobj)
        if len(ci)>0:
            return True
        else:
            return False
    except:
        return False

@register.filter
def workstrim_status(value):
    wobj = ChatThread.objects.get(id=value)
    if wobj.block:
        return True
    else:
        return False