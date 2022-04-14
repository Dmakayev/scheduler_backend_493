from django.db import models

import FacultyNames.models


class Professors(models.Model):
    id = models.AutoField(primary_key=True)
    lastName = models.TextField()
    firstName = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    department = models.TextField()


class Rooms(models.Model):
    rID = models.TextField()
    bName = models.AutoField(primary_key=True)
    capacity = models.IntegerField()


class Departments(models.Model):
    depID = models.TextField(primary_key=True)


class Classes(models.Model):
    models.ForeignKey.null = True
    secID = models.AutoField(primary_key=True)
    courseName = models.TextField()
    Department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    Professor = models.ForeignKey(Professors, on_delete=models.SET_NULL)
    Professor.null = True
    courseNumber = models.IntegerField()
    credits = models.TextField()
    days = models.TextField()
    time = models.TextField()
    waitSize = models.TextField()
    enrollment = models.TextField()
    room = models.ForeignKey(Rooms, on_delete=models.SET_NULL)
    room.null = True


class Meetings(models.Model):
    mID = models.AutoField(primary_key=True)
    mName = models.TextField()
    room = models.ForeignKey(Rooms, on_delete=models.SET_NULL)
    room.null = True
    host = models.ForeignKey(Professors, on_delete=models.CASCADE)
    faculty = models.ForeignKey(FacultyNames.models.Faculty, on_delete=models.SET_NULL)
    faculty.null = True
