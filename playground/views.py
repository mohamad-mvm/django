from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

var1 = {'firstname':'mohamad','lastname':'Vahabian'}

def sayHello(request):
    return HttpResponse('hello world')

def htmltemp(request):
    x=1
    return render(request,'hello.html',var1)
