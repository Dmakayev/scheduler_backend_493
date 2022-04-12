from django.db import models


class FileUpload(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, default='')
    url = models.CharField(max_length=200, blank=False, default='')
