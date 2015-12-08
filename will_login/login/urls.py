__author__ = 'wfg2af'

from django.conf.urls import url

from . import views

urlpatterns = [url(r'^$', views.home_page, name='home_page'),
               url(r'^register/$', views.register_page, name='register_page'),
               url(r'^lg/$', views.login_page, name='login_page'),
               url(r'^message/$', views.message_page, name='message_page'),
               url(r'^loggedin/$', views.logged_in_page, name='logged_in_page'),
               url(r'^messageHub/$', views.message_hub_page, name='message_hub_page'),
               url(r'^messageDisplay/$', views.message_display_page, name='message_display_page'),
               url(r'^updateInfo/$', views.update_page, name='update_page'),
               url(r'^groups/$', views.group_page, name='group_page'),
               url(r'^siteManager/$', views.site_manager_page, name='site_manager_page'),
               url(r'^myReports/$', views.my_reports_page, name='my_reports_page'),
		url(r'^uploadReport/$', views.upload_report, name='upload_report'),
		url(r'^submitReport/$', views.submit_report, name='submit_report'),
		url(r'^editReport/$', views.edit_report, name='edit_report'),
		url(r'^sharedWithMe/$', views.shared_with_me, name='shared_with_me'),
        url(r'^viewGroup/$', views.view_group, name='view_group'),
        url(r'^delete/$', views.delete_all, name='delete_all'),
			   ]
