from rest_framework import serializers
from FacultyNames.models import Faculty


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'lastName', 'firstName', 'email', 'phone', 'department', 'title')
