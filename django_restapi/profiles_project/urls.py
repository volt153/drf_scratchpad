"""profiles_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

when we go to /api in the web server, it will pass in the request to the django app which will then lookup 
the urlpatterns for  matches to the url we have entered. it will pass in all the urls that match the /api and it 
will load up the sub urls in the urls.py file in the api subdir    
"""
from django.contrib import admin
from django.urls import path, include # include includes other urls into the root urls of the project 

urlpatterns = [
    path('admin/', admin.site.urls), #admin app included in django by default
    path('api/', include('profiles_api.urls')) #.urls refers to the urls.py in the api subdir which contains the urls
]
