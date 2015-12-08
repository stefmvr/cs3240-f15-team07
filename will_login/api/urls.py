from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'verify/$', views.verify_account),
    url(r'reports/$', views.get_reports),
    url(r'files/$',views.get_files),
]
