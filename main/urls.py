from django.urls import path, include
from django.shortcuts import redirect

def login_redir(request):
    return redirect('/admin/')

urlpatterns = [
    path('', login_redir, name='root_redirect')
]