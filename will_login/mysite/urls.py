"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^filer/', include('filer.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^login/', include('login.urls', namespace="login")),
    url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
    #url(r'^files/'+path_end,'view'),
    url(r'^api/', include('api.urls', namespace="api")),
    url(r'^reports/', include('login.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
