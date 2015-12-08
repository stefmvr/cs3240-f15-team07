from django.db import models
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from login.models import ReportModel

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class api(models.Model):
    username = models.CharField(max_length=100, blank=True, default='')
    password = models.TextField()

    class Meta:
        ordering = ('username',)


class report_api(models.Model):
    report_title = models.TextField()
    report_body = models.TextField()
    id_num = models.TextField()

    class Meta:
        ordering = ('report_title',)

class report2_api(models.Model):
    file_name = models.FileField()

    class Meta:
        ordering = ('file_name',)
