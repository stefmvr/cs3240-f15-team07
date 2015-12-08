from django.contrib import admin

from .models import UserAttributes, Groups, Folder

admin.site.register(UserAttributes)
admin.site.register(Groups)
admin.site.register(Folder)
# Register your models here.
