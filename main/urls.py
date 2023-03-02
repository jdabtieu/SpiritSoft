from django.conf import settings
from django.urls import path, include
from django.shortcuts import redirect, render

def homepage(request):
    """Display homepage if configured"""
    if settings.HOMEPAGE:
        return render(request, 'homepage.html')
    else:
        return redirect('/admin/')


def helppage(request):
    """Display help page"""
    return render(request, 'help.html')

def iframed(request):
    """IFrame view for embedded (desktop) app"""
    return render(request, 'iframed.html')

urlpatterns = [
    path('', homepage, name='root_redirect'),
    path('help/', helppage, name='help_page'),
    path('iframe/', iframed, name='iframed_container'),
]