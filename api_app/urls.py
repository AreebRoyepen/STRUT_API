"""api_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index_api_response,name="index_api_response"),
    url(r'^login',views.login,name="login"),
    url(r'^viewTimetable',views.viewTimetable,name="viewTimetable"),
    url(r'^navigate',views.navigate,name="navigate"),
    url(r'^moduleName',views.moduleName,name="moduleName"),
    url(r'^venueName',views.venueName,name="venueName"),
    url(r'^bookVenue',views.bookVenue,name="bookVenue"),
    url(r'^checkVenue',views.checkVenue,name="checkVenue"),
    url(r'^isVenue',views.isVenue,name="isVenue"),
    url(r'^studentDetails',views.studentDetails,name="studentDetails"),
    url(r'^viewExamTimetable',views.viewExamTimetable,name="viewExamTimetable")
]


