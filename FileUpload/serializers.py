from rest_framework import serializers
from FileUpload.models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ('id',
                  'name',
                  'url',
                  'uploadedFile')
