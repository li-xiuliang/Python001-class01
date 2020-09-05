from django.shortcuts import render
from django.db.models import Avg, Count
from datetime import datetime

# Create your views here.
from .models import PhoneInfo, CommentsInfo

def parse_ymd(s, h):
    year_s, mon_s, day_s = s.split('-')
    hour, minute = h.split(':')
    return datetime(int(year_s), int(mon_s), int(day_s), int(hour), int(minute))

def index(request):
    phone = PhoneInfo.objects.all()
    comments = CommentsInfo.objects.all()
    sentiment = []
    counts = []
    for single in phone:
        senti = comments.filter(phone_id = single.id).aggregate(Avg('sentiment'))['sentiment__avg']
        count = comments.filter(phone_id = single.id).aggregate(Count('sentiment'))['sentiment__count']
        sentiment.append(senti)
        counts.append(count)
    show_phone_info = phone[:10]
    return render(request, 'total.html', locals()) 

def single_phone(request):
    name = request.GET.get("phone", None)
    if name:
        phone = PhoneInfo.objects.all()
        comments = CommentsInfo.objects.all()
        phone_find = phone.filter(name__contains=name)
        sentiments = {}
        if phone_find:
            for each in phone_find:
                senti = list(comments.filter(phone_id = each.id).values_list('sentiment'))
                sentiments[each.name] = senti
        sen = {}
        for key, values in sentiments.items():
            ls = []
            for c in values:
                ls.append(c[0])
            sen[key] = ls
        return render(request, 'single_phone.html', locals())
    else:
        return render(request, 'error.html', locals())

def comments_author(request):
    name = request.GET.get("author", None)
    print(name)
    if name:
        comment = CommentsInfo.objects.filter(name__contains = name).values()
        scores = {}
        for com in comment:
            n = com['name']
            if n in scores:
                scores[n].append(com['sentiment'])
            else:
                scores[n] = [com['sentiment'],]
        return render(request, 'comments_author.html', locals())

def publish_time(request):
    starttime = parse_ymd(request.GET.get("startdate", None), request.GET.get("starttime", None))
    endtime = parse_ymd(request.GET.get("enddate", None), request.GET.get("endtime", None))
    date = PhoneInfo.objects.filter(publish_time__range=[starttime, endtime])
    return render(request, 'publish.html', locals())