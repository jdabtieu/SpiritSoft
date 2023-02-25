from django.urls import path, include
from django.shortcuts import redirect, render

def login_redir(request):
    return redirect('/admin/')

def iframed(request):
    return render(request, 'iframed.html')

urlpatterns = [
    path('', login_redir, name='root_redirect'),
    path('iframe/', iframed, name='iframed_container'),
]