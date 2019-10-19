from rest_framework import serializers
from .models import Employee, Module, Enrolement, Building, Venue, Timetable, ExamTimetable

class ModuleSerializer(serializers.ModelSerializer):
	class Meta:
		model=Module
		fields='__all__'


class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model=Employee
		fields='__all__'

class EnrolementSerializer(serializers.ModelSerializer):
	class Meta:
		model=Enrolement
		fields='__all__'

class BuildingSerializer(serializers.ModelSerializer):
	class Meta:
		model=Building
		fields='__all__'

class VenueSerializer(serializers.ModelSerializer):
	class Meta:
		model=Venue
		fields='__all__'

class TimetableSerializer(serializers.ModelSerializer):
	venue = serializers.StringRelatedField(source='venueID', read_only=False)
	module = serializers.StringRelatedField(source='moduleID', read_only=False)

	class Meta:
		model=Timetable
		fields= ('id', 'period', 'day', 'module', 'venue')

class ExamTimetableSerializer(serializers.ModelSerializer):
	class Meta:
		model=ExamTimetable
		fields='__all__'