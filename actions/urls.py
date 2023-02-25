from django.urls import path, include
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('admin/actions/', include([
        path('importstudents/', views.ImportStudentsView.as_view(), name='import_students'),
        path('createreport/', views.CreateReportView.as_view(), name='create_report'),
    ])),
]