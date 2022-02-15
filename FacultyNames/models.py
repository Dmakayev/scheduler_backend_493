from django.db import models


class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    lastName = models.TextField()
    firstName = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    department = models.TextField()
    title = models.TextField()

