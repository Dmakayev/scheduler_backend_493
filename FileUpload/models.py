from django.db import models


class FileUpload(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    url = models.CharField(max_length=200, blank=False, default='')
    uploadedFile = models.FileField()
