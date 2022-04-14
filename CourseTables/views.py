from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from CourseTables.models import Classes
from CourseTables.models import Professors
from CourseTables.models import Meetings
from CourseTables.models import Rooms
from CourseTables.models import Departments
from CourseTables.serializers import CourseSerializer
from CourseTables.models import TempCourse

from django.core.files.storage import default_storage


@csrf_exempt
def courseApi(request, fid=0):
    if request.method == 'GET':
        course = TempCourse.objects.all()
        course_serializer = CourseSerializer(course, many=True)
        return JsonResponse(course_serializer.data, safe=False)
    elif request.method == 'POST':
        course_data = JSONParser().parse(request)
        course_serializer = CourseSerializer(data=course_data)
        if course_serializer.is_valid():
            course_serializer.save()
            return JsonResponse("Added Succesfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        course_data = JSONParser().parse(request)
        course = TempCourse.objects.get(id=fid)
        course_serializer = CourseSerializer(course, data=course_data)
        if course_serializer.is_valid():
            course_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        course = TempCourse.objects.get(id=fid)
        course.delete()
        return JsonResponse("Deleted Succesfully", safe=False)


@csrf_exempt
def SaveFile(requests):
    file = requests.FILES['file']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)
