from rest_framework import serializers
from CourseTables.models import TempCourse


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempCourse
        fields = ('classNumber', 'className', 'credits', 'sectionNumber', 'capacity', 'room', 'waitSize', 'enrollment',
                  'days', 'uniqueCourseID', 'time', 'instructor')
