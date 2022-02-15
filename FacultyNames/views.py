from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from FacultyNames.models import Faculty
from FacultyNames.serializers import FacultySerializer

from django.core.files.storage import default_storage

@csrf_exempt
def facultyApi(request, fid=0):
    if request.method == 'GET':
        faculty = Faculty.objects.all()
        faculty_serializer = FacultySerializer(faculty, many=True)
        return JsonResponse(faculty_serializer.data, safe=False)
    elif request.method == 'POST':
        faculty_data = JSONParser().parse(request)
        faculty_serializer = FacultySerializer(data=faculty_data)
        if faculty_serializer.is_valid():
            faculty_serializer.save()
            return JsonResponse("Added Succesfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        faculty_data = JSONParser.parse(request)
        faculty = Faculty.objects.get(id=faculty_data['id'])
        faculty_serializer = FacultySerializer(faculty, data=faculty_data)
        if faculty_serializer.is_valid():
            faculty_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        faculty = Faculty.objects.get(id=fid)
        faculty.delete()
        return JsonResponse("Deleted Succesfully", safe=False)


@csrf_exempt
def SaveFile(requests):
    file = requests.FILES['file']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)