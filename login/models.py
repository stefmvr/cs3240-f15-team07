from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
# Create your models here.

class Folder(models.Model):
    owner = models.CharField(max_length = 100, default="")
    parent_folder = models.ForeignKey('self', null = True, blank = True)
    name = models.CharField(max_length = 100, default="")

class Groups(models.Model):
	group_name = models.CharField(max_length=100)
	group_creator=models.CharField(max_length=100)

class UserAttributes(models.Model):
    groups = models.ManyToManyField(Groups)
    is_site_manager = models.BooleanField(default=False)
    user_name = models.CharField(max_length=100)
    publicKey = models.CharField(max_length=10000)


    def __str__(self):
        return self.user_name


class MessageDB(models.Model):
    message_subject = models.CharField(max_length=100)
    message_body = models.TextField(max_length=5000)
    encrypted = models.BooleanField()
    sym_password = models.BinaryField()
    sent_date = models.DateTimeField()
    unread = models.BooleanField(default=True)

    @classmethod
    def createNew(cls, sub, bod, enc, symm, sd, unr):
        msg = cls(message_subject = sub, message_body = bod, encrypted = enc, sym_password = symm, sent_date = sd, unread = unr)
        # do something with the book
        return msg


#-----------Report Models
class ReportModel(models.Model):
	report_title = models.CharField(max_length=100)
	report_body = models.TextField(max_length=5000)
	report_private = models.BooleanField()
	report_owner = models.CharField(max_length=100, default="")
	parent_folder = models.ForeignKey(Folder, null=True, blank=True)
	report_sharedwith = models.ManyToManyField(User)
	report_groups = models.ManyToManyField(Groups)
	report_timestamp = models.DateTimeField(auto_now_add=True)
	#report_sharedwith = ManyToManyField(models.User)
	#report_files = models.FileField(upload_to='documents/%Y/%m/%d)]

class SingleFileModel(models.Model):
	file_report = models.ForeignKey(ReportModel, related_name='report_files')
	single_file = models.FileField(upload_to='documents/%Y/%m/%d')


