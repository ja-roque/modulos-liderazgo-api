"""liderazgo_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import include, url
from django.urls import path

from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from .views import RestrictedView, getDoc, getPresentation, getUserModules, getExam, getVideo, postExamScore, getUserReport, getAllReports, getAllUsers, getBibliografia, getTest, getDinamica

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^', include('rest_auth.urls')),
    url(r'^registration/', include('rest_auth.registration.urls')),
    
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    
    url(r'^refresh-token/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    url(r'^restricted/$', RestrictedView.as_view()),

    # GETS
    url(r'^getdoc/$', getDoc.as_view()),
    url(r'^getpresentation/$', getPresentation.as_view()),
    url(r'^getexam/$', getExam.as_view()),
    url(r'^getvideo/$', getVideo.as_view()),
    url(r'^getdinamica/$', getDinamica.as_view()),
    url(r'^gettest/$', getTest.as_view()),
    url(r'^getbibliografia/$', getBibliografia.as_view()),
    url(r'^getusermodules/$', getUserModules.as_view()),
    url(r'^getuserreport/$', getUserReport.as_view()),

    url(r'^getallusers/$', getAllUsers.as_view()),
    url(r'^getallreports/$', getAllReports.as_view()),

    # POSTS
    url(r'^postexamscore/$', postExamScore.as_view()),    
]
