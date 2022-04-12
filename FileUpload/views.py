from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from FileUpload.models import FileUpload
from FileUpload.serializers import FileUploadSerializer
from rest_framework.decorators import api_view

from django.core.files.storage import FileSystemStorage
import PDFParser.ParsePDF


@api_view(['GET', 'POST', 'DELETE'])
def fileupload_list(request):
    if request.method == 'GET':
        fileUpload = FileUpload.objects.all()

        title = request.GET.get('name', None)
        if title is not None:
            fileUpload = fileUpload.filter(name__icontains=title)

        fileUpload_serializer = FileUploadSerializer(fileUpload, many=True)
        return JsonResponse(fileUpload_serializer.data, safe=False)

    elif request.method == 'POST':
        fileUpload_data = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(fileUpload_data.name, fileUpload_data)
        # uploaded_url = fs.url(filename)
        # pdfParser = JSONParser().parse(filename)
        # pdf_serializer = FileUploadSerializer(data=pdfParser)
        # if pdf_serializer.is_valid():
        #     pdf_serializer.save()
        namesz = PDFParser.ParsePDF.main(fs.base_location + "/" + filename)
        return JsonResponse("File Uploaded Successfully!", status=200, safe=False)


    elif request.method == 'DELETE':
        count = FileUpload.objects.all().delete()
        return JsonResponse({'message': '{} fileUpload were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def fileupload_detail(request, pk):
    # find file by pk (id)
    try:
        fileUpload = FileUpload.objects.get(pk=pk)
    except FileUpload.DoesNotExist:
        return JsonResponse({'message': 'The File does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        fileUpload_serializer = FileUploadSerializer(fileUpload)
        return JsonResponse(fileUpload_serializer.data)

    elif request.method == 'PUT':
        fileUpload_data = JSONParser().parse(request)
        fileUpload_serializer = FileUploadSerializer(fileUpload, data=fileUpload_data)
        if fileUpload_serializer.is_valid():
            fileUpload_serializer.save()
            return JsonResponse(fileUpload_serializer.data)
        return JsonResponse(fileUpload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        fileUpload.delete()
        return JsonResponse({'message': 'fileUpload was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

        # GET / PUT / DELETE file

# @api_view(['GET'])
# def fileupload_list_published(request):
#     fileUpload = FileUpload.objects.filter(published=True)
#
#     if request.method == 'GET':
#         fileUpload_serializer = FileUploadSerializer(fileUpload, many=True)
#         return JsonResponse(fileUpload_serializer.data, safe=False)
