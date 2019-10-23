from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models.query import EmptyQuerySet

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
import json
from datetime import datetime

from .models import Module, Enrolement, Building, Venue, Timetable, ExamTimetable, BookedVenue
from .serializers import UserSerializer, ModuleSerializer, EnrolementSerializer, BuildingSerializer, VenueSerializer, TimetableSerializer, ExamTimetableSerializer



def index_api_response(request):
	responseData = {
    	'Error':'Endpoint not found:Append Endpoint' ,
	}
	return HttpResponse(json.dumps(responseData), content_type="application/json")


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

	v2 = Venue.objects.filter(venueName = to).values_list()

	if (len(v2) == 0):
		b2 = Building.objects.get(buildingName = to)
		flag  = False
	else:
		flag = True
		b2 = Building.objects.get(pk = v2[0][2])

	if (b1 is None or b2 is None):
		return Response({'error': 'Invalid building or venue'},
                        status=HTTP_404_NOT_FOUND)

	serializer1 = BuildingSerializer(b1, many = False)
	serializer2 = BuildingSerializer(b2, many = False)

	if not flag:
		return Response({'from':serializer1.data, 'to' : serializer2.data},
                        status=HTTP_200_OK)
	else:
		v2 = Venue.objects.get(venueName = to)
		serializer3 = VenueSerializer(v2, many = False)
		return Response({'from':serializer1.data, 'to' : serializer2.data, 'venue' : serializer3.data},
                        status=HTTP_200_OK)



@api_view(["POST"])
def checkVenue(request):
	period = request.data.get("period")
	d = request.data.get("date")
	studentID = request.data.get("id")
	venue = request.data.get("venue")
	p = request.data.get("period")

	d = str(d)
	d = datetime(int(d[6:10]),int(d[3:5]),int(d[0:2]))

	v = Venue.objects.filter(venueName = venue)
	v = v[0]
	stud = User.objects.get(username = studentID)

	bv = BookedVenue.objects.filter(period = period, date = d, venue  = v)
	bv1 = Timetable.objects.filter(period = period, day= d.weekday()+ 1, venueID = v)

	if(len(bv) == 0 and len(bv1) == 0):
		venue.save()
		return Response({'message': 'success'},
                        status=HTTP_200_OK)
	else:
		return Response({'message': 'already booked'},
                        status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def bookVenue(request):
	period = request.data.get("period")
	d = request.data.get("date")
	studentID = request.data.get("id")
	venue = request.data.get("venue")
	p = request.data.get("period")

	d = str(d)
	d = datetime(int(d[6:10]),int(d[3:5]),int(d[0:2]))

	v = Venue.objects.filter(venueName = venue)
	v = v[0]
	stud = User.objects.get(username = studentID)

	bv = BookedVenue.objects.filter(period = period, date = d, venue  = v)
	bv1 = Timetable.objects.filter(period = period, day= d.weekday()+ 1, venueID = v)

	if(len(bv) == 0 and len(bv1) == 0):
		venue = BookedVenue(student = stud, venue = v,    date = d , period = p )
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

	if (len(m) == 0):
		return Response({'error': 'Invalid module'},
                        status=HTTP_404_NOT_FOUND)
	return Response(ModuleSerializer(m,many = True).data)


@api_view(["POST"])
def venueName(request):
	id = request.data.get("id")
	v = Venue.objects.filter(pk = id)

	if (len(v)==0):
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
def studentDetails(request):
	num = request.data.get("studentNumber")
	stud = User.objects.get(username = num)

	serializer1 = UserSerializer(stud, many = False)

	enrolement = Enrolement.objects.filter(student = stud.pk)
	serializer2 = EnrolementSerializer(enrolement, many = True)
	return Response({'user':serializer1.data, 'modules' : serializer2.data},
                        status=HTTP_200_OK)


@api_view(["POST"])
def viewExamTimetable(request):
	num = request.data.get("studentNumber")
	stud = User.objects.get(username = num)
	enrolement = Enrolement.objects.filter(student = stud.pk)
	lst = enrolement.values_list("module", flat = True) 
	t = ExamTimetable.objects.filter(moduleID__in = lst)
	serializer = ExamTimetableSerializer(t, many = True)
	return Response(serializer.data)