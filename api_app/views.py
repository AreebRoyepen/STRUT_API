from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from datetime import datetime
#########################
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.db.models.query import EmptyQuerySet
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
from .models import Employee, Module, Enrolement, Building, Venue, Timetable, ExamTimetable, BookedVenue
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
    return Response({'response': ' true '},
                    status=HTTP_200_OK)


@api_view(["POST"])
def viewTimetable(request):
	num = request.data.get("studentNumber")
	stud = User.objects.get(username = num)
	enrolement = Enrolement.objects.filter(student = stud.pk)
	lst = enrolement.values_list("module", flat = True) 
	t = Timetable.objects.filter(moduleID__in = lst)
	serializer = TimetableSerializer(t, many = True)
	return Response(serializer.data)


@api_view(["POST"])
def navigate(request):
	to = request.data.get("to")
	frm = request.data.get("from")

	v1 = Venue.objects.filter(venueName = frm).values_list()
	if (len(v1) == 0):
		b1 = Building.objects.get(buildingName = frm)
	else:
		b1 = Building.objects.get(pk = v1[0][2])
		#b1 = b1.buildingName

	v2 = Venue.objects.filter(venueName = to).values_list()

	if (len(v2) == 0):
		b2 = Building.objects.get(buildingName = to)
	else:
		b2 = Building.objects.get(pk = v2[0][2])
		#b2 = b2.buildingName

	if (b1 is None or b2 is None):
		return Response({'error': 'Invalid building or venue'},
                        status=HTTP_404_NOT_FOUND)

	serializer1 = BuildingSerializer(b1, many = False)
	serializer2 = BuildingSerializer(b2, many = False)

	return Response({'from':serializer1.data, 'to' : serializer2.data},
                        status=HTTP_200_OK)



@api_view(["POST"])
def bookVenue(request):
	period = request.data.get("period")
	d = request.data.get("date")
	d = str(d)
	print(int(d[6:10]),int(d[3:5]),int(d[0:2]))
	d = datetime(int(d[6:10]),int(d[3:5]),int(d[0:2]))
	studentID = request.data.get("id")
	venue = request.data.get("venue")
	p = request.data.get("period")

	v = Venue.objects.filter(venueName = venue)
	v = v[0].pk
	stud = User.objects.get(username = studentID)

	bv = BookedVenue.objects.filter(period = period, date = d, venue  = v)
	bv1 = Timetable.objects.filter(period = period, day= d.weekday()+ 1, venueID = v)

	if(len(bv) == 0 and len(bv1) == 0):
		venue = BookedVenue(student = studentID, venueID = v,    date = d , period = p )
		venue.save()
		return Response({'message': 'success'},
                        status=HTTP_200_OK)
	else:
		return Response({'message': 'already booked'},
                        status=HTTP_400_BAD_REQUEST)
	


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


@api_view(["POST"])
def isVenue(request):
	id = request.data.get("name")
	v = Venue.objects.filter(venueName = id)

	if (len(v) == 0):
		return Response({'response': 'false'},
                        status=HTTP_404_NOT_FOUND)
	return Response({'response': 'true'},
                        status=HTTP_200_OK)


@api_view(["POST"])
def viewModules(request):
	num = request.data.get("studentNumber")
	stud = User.objects.get(username = num)
	enrolement = Enrolement.objects.filter(student = stud.pk)
	serializer = EnrolementSerializer(enrolement, many = True)
	return Response(serializer.data)