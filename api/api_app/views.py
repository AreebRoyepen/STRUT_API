from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
#########################
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
########################
from django.contrib.auth.models import User
from .models import Employee, Module, Enrolement, Building, Venue, Timetable, ExamTimetable
from .serializers import EmployeeSerializer, ModuleSerializer, EnrolementSerializer, BuildingSerializer, VenueSerializer, TimetableSerializer, ExamTimetableSerializer


def index_api_response(request):
	responseData = {
    	'Error':'Endpoint not found:Append Endpoint' ,
	}
	return HttpResponse(json.dumps(responseData), content_type="application/json")


class EmployeeListView(APIView):

	def get(self,request):
		employees=Employee.objects.all()
		serializer=EmployeeSerializer(employees,many=True)
		return Response(serializer.data)
	def post(self,request):
		pass

##########################################################################

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    return Response({'response: true '},
                    status=HTTP_200_OK)


@api_view(["POST"])
def viewTimetable(request):
	num = request.data.get("studentNumber")
	stud = User.objects.get(username = num)
	enrolement = Enrolement.objects.filter(student = stud.pk)
	lst = enrolement.values_list("moduleID", flat = True) 
	t = Timetable.objects.filter(moduleID__in = lst)
	serializer = TimetableSerializer(t, many = True)
	return Response(serializer.data)


@api_view(["POST"])
def navigate(request):
	to = request.data.get("to")
	frm = request.data.get("from")

	v1 = Venue.objects.filter(venueName = frm).values_list()
	b1 = Building.objects.get(pk = v1[0][2])

	v2 = Venue.objects.filter(venueName = to).values_list()
	b2 = Building.objects.get(pk = v2[0][2])

	if (v1 is None or v2 is None or b1 is None or b2 is None):
		return Response({'error': 'Invalid building or venue'},
                        status=HTTP_404_NOT_FOUND)

	return Response({'from:' + b1.buildingName + ', to :' + b2.buildingName},
                    status=HTTP_200_OK)



@api_view(["POST"])
def bookVenue(request):

	return


@api_view(["POST"])
def moduleName(request):
	id = request.data.get("id")
	m = Module.objects.filter(pk = id)

	if (m is None):
		return Response({'error': 'Invalid module'},
                        status=HTTP_404_NOT_FOUND)
	return Response(ModuleSerializer(m,many = True).data)


@api_view(["POST"])
def venueName(request):
	id = request.data.get("id")
	v = Venue.objects.filter(pk = id)

	if (v is None):
		return Response({'error': 'Invalid venue'},
                        status=HTTP_404_NOT_FOUND)
	return Response(VenueSerializer(v, many = True).data)

