from django.shortcuts import render
from .models import *

# Create your views here.


def hellow(request):
    queryset=Product.objects.all()
    
    return render(request,'index.html',{'products':list(queryset)})
