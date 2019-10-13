from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Employee(models.Model):
    name=models.TextField()
    jobtitle=models.TextField()
    def __str__(self):
        return self.jobtitle


########################################

'''
the models representation of the DB, 
UML diagram in the documentation
'''

class Module (models.Model):
    moduleName = models.CharField(max_length = 100)
    def get(self):
        return self.moduleName
    def __str__(self):
        return self.moduleName


class Enrolement(models.Model):
    student = models.ForeignKey(User,on_delete = models.CASCADE)    
    module = models.ForeignKey(Module,on_delete = models.CASCADE)
    def __str__(self):
        return self.module.get()


class Building(models.Model):
    buildingName = models.CharField(max_length = 100)
    buildingPlan = models.ImageField()

    def __str__(self):
        return self.buildingName



class Venue(models.Model):
    venueName = models.CharField(max_length = 100)
    buildingID = models.ForeignKey(Building,on_delete = models.CASCADE)

    def get(self):
        return self.venueName
    def __str__(self):
        return self.venueName


class Timetable(models.Model):
    venueID = models.ForeignKey(Venue, on_delete = models.CASCADE)
    period = models.IntegerField()
    moduleID = models.ForeignKey(Module,  on_delete = models.CASCADE)
    day = models.IntegerField()

    class Meta:
        unique_together = ('venueID', 'period', 'day')
    def __str__(self):
        return "day: " + str(self.day) + " period: " + str(self.period) + " module: " + str(self.moduleID.get()) + " " + self.venueID.get()


class ExamTimetable(models.Model):
    venueID = models.ForeignKey(Venue, on_delete = models.CASCADE)
    date = models.DateField()
    moduleID = models.ForeignKey(Module,  on_delete = models.CASCADE)
    period = models.IntegerField()

    class Meta:
        unique_together = ('venueID', 'period', 'date')
    def __str__(self):
        return "day: " + str(self.date) + " period: " + str(self.period) + " module: " + str(self.moduleID.get()) + " " + self.venueID.get()


class BookedVenue(models.Model):
    student = models.ForeignKey(User,on_delete = models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateField()
    period = models.IntegerField()
    

    