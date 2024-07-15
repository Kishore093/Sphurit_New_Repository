
from django import template
register = template.Library()
from teacher.models import*

@register.filter
def count(array):
    return len(array)

@register.filter
def topicCount(cid):
    c = Course.objects.get(id=cid.id)
    ch = Chapter.objects.filter(course=c)
    qs = []
    for i in ch:
        ts = Topic.objects.filter(chapter=i)
        qs.extend(ts)
    return len(qs)

@register.filter
def form_count(cid):
    c = Course.objects.get(id=cid.id)
    ch = Chapter.objects.filter(course=c)
    qs = []
    for i in ch:
        ts = Topic.objects.filter(chapter=i)
        for j in ts:
            fs = Form.objects.filter(topic=j)
            qs.extend(fs)
    return len(qs)

@register.filter(name='vduration')
def vduration(videourl):
    video_time = "8min"
    return video_time