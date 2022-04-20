from rest_framework import serializers
from CourseTables.models import TempCourse, TempMeeting


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempCourse
        fields = ('classNumber', 'className', 'credits', 'sectionNumber', 'capacity', 'room', 'waitSize', 'enrollment',
                  'days', 'uniqueCourseID', 'time', 'instructor')


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempMeeting
        fields = ('mID', 'firstName', 'lastName', 'classNumber', 'sectionNumber', 'className', 'room', 'eventType',
                  'startTime', 'endTime')
