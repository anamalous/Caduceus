from django.db.models import *
from django.contrib.postgres.fields import ArrayField
from datetime import datetime

class Employees(Model):
    empid=AutoField(primary_key=True,serialize=True)
    type=CharField(max_length=10,choices={1:"AD",2:"DR"})
    name=CharField(max_length=100)
    password=CharField(max_length=10)
    email=EmailField(max_length=100)
    contact=CharField(max_length=10)
    speciality=CharField(max_length=20)
    surgeries=ArrayField(CharField(max_length=100),default=[])
    age=IntegerField(default=0)
    hours=IntegerField(default=0)
    address=CharField(max_length=500)

class Rooms(Model):
    rid=AutoField(primary_key=True,serialize=True)
    type=CharField(max_length=20,choices={1:"OT",2:"consultation",3:"ward"})
    floor=IntegerField(default=0)
    equipped=ArrayField(CharField(max_length=20),default=[])
    capacity=IntegerField(default=0)

class Appointments(Model):
    id=AutoField(primary_key=True,serialize=True)
    patient=IntegerField(default=0)
    date=DateField(default=datetime.now())
    doctor=CharField(default="",null=True)
    timeslot=TimeField(null=True)
    surgtype=CharField(max_length=200,default="")

class PatientData(Model):
    pid=AutoField(primary_key=True,serialize=True)
    name=CharField(max_length=100)
    email=EmailField(max_length=100)
    contact=CharField(max_length=10)
    gender=CharField(max_length=10)
    age=IntegerField(default=0)
    address=CharField(max_length=500)
    weight=IntegerField(default=0)
    bloodgrp=CharField(max_length=20,choices={1:"A+",2:"A-",3:"B+",4:"B-",5:"O+",6:"O-"})
    maritalstat= CharField(max_length=20,choices={1:"married",2:"single",3:"divorced"})
    occupation=CharField(max_length=500)

class CurrentAdmits(Model):
    id=AutoField(primary_key=True,serialize=True)
    appid=IntegerField(default=0)
    pid=IntegerField(default=0)
    docid=IntegerField(default=0)
    status=CharField(max_length=20,choices={1:"admitted",2:"discharged"})
    report=IntegerField(default=0)
    currentmedication=CharField(max_length=50,default="-")
    currentdosage=IntegerField(default=0)
    currentdiagnosis=CharField(max_length=100,default="-")

class RepScans(Model):
    id=AutoField(primary_key=True,serialize=True)
    pid=IntegerField(default=0)
    docid=IntegerField(default=0)
    report=ImageField(default="hello.jpg",upload_to="media")
    comments=CharField(max_length=200, default="")

class DBsearches(Model):
    scan=ImageField(default="hello.jpg",upload_to="media")

