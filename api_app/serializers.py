from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Module, Enrolement, Building, Venue, Timetable, ExamTimetable

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields= ('first_name', 'last_name', 'email','username')

class ModuleSerializer(serializers.ModelSerializer):
	class Meta:
		model=Module
		fields='__all__'


class EnrolementSerializer(serializers.ModelSerializer):
	modulename = serializers.StringRelatedField(source='module', read_only=False)

	class Meta:
		model=Enrolement
		fields=('modulename' , 'year')

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
	venue = serializers.StringRelatedField(source='venueID', read_only=False)
	module = serializers.StringRelatedField(source='moduleID', read_only=False)
	class Meta:
		model=ExamTimetable
		fields='__all__'