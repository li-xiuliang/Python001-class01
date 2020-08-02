from django.shortcuts import render
from django.http import HttpResponse
from .models import DbComment


# Create your views here.
def index(request):
    return HttpResponse("Hello Django!")

def comments(request):
    n = DbComment.objects.all()
    return render(request, 'comments.html', locals())

