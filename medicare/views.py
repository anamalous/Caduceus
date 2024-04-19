from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from django.urls import reverse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from django.contrib.messages import add_message
from django.contrib import messages
import time
from .ocr import *
from .csp import *
from .forms import *
import numpy as np
import pandas as pd
from .drugopt import *
import json
from .heartpredict import *
def doctorentry(request):
  docs=pd.read_csv(r'./static/data/docs.csv')
  print(docs)
  for i in range(len(docs)):
    d=Employees.objects.create()
    d.type=docs.iloc[i]["type"]
    d.name=docs.iloc[i]["name"]
    d.password=docs.iloc[i]["password"]
    d.email=docs.iloc[i]["email"]
    d.contact=docs.iloc[i]["contact"]
    d.speciality=docs.iloc[i]["speciality"]
    d.surgeries=docs.iloc[i]["preferences"].split(",")
    d.age=docs.iloc[i]["age"]
    d.hours=docs.iloc[i]["hours"]
    d.address=docs.iloc[i]["address"]
    d.save()
  return HttpResponse("done")

@csrf_exempt
def heartassess(request):
  hbp=int(request.POST.get("HighBP"))
  hch=int(request.POST.get("HighChol"))
  cch=int(request.POST.get("CholCheck"))
  sm=int(request.POST.get("Smoker"))
  st=int(request.POST.get("Stroke"))
  di=int(request.POST.get("Diabetes"))
  print(np.array([hbp,hch,cch,sm,st,di,0]).reshape(1,7))
  pred=heartpredict(np.array([hbp,hch,cch,sm,st,di,0]).reshape(1,7))
  template=None
  print(pred)
  if pred[0]==0:
    template = loader.get_template('yayheart.html')
  else:
    template = loader.get_template('nawrheart.html')
  return HttpResponse(template.render())


def allOTs(request):
  o=Rooms.objects.filter(type="OT")
  return HttpResponse(list(o))

def docpatients(request):
  a=Appointments.objects.filter(doctor=request.session["user"])
  patlist=[]
  for i in a:
    if i.patient not in [i[0] for i in patlist]:
      p=PatientData.objects.get(pid=i.patient)  
      appts=[]
      for j in a:
        if j.patient==p.pid:
          appts.append(j.date.strftime("%d/%m/%Y"))
      patlist.append([p.pid,p.name,appts])
    print(patlist)
  context={"patients":patlist}
  template = loader.get_template('patrecords.html')
  return HttpResponse(template.render(context,request))

def homepage(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def heartdis(request):
  template = loader.get_template('heartdisease.html')
  return HttpResponse(template.render())

def drugdb(request):
  template = loader.get_template('drugdb.html')
  return HttpResponse(template.render())

@csrf_exempt
def searchdrug(request):
  form = searchdbupload(request.POST, request.FILES)  
  if form.is_valid():  
    obj=form.save()   
  r=DBsearches.objects.get(pk=obj.pk)
  imgurl=r.scan
  data=readstrip(imgurl)
  
  try:
    context={
      "Drug":list(data["Drug"].values())[0],
      "meta":{
      "Uses":list(data["Uses"].values())[0],
      "SideEffects":list(data["SideEffects"].values())[0]
      }
    }
  except:
    context={"Drug":"not found"}
  template = loader.get_template('drugsearch.html')
  return HttpResponse(template.render(context,request))

def dosagechart(request):
  template = loader.get_template('dosage.html')
  return HttpResponse(template.render())

@csrf_exempt
def addpatient(request):
  p=PatientData.objects.create()
  p.name=request.POST.get("name")
  p.email=request.POST.get("email")
  p.contact=request.POST.get("contact")
  p.gender=request.POST.get("gender")
  p.age=request.POST.get("age")
  p.address=request.POST.get("address")
  p.weight=request.POST.get("weight")
  p.bloodgrp=request.POST.get("bloodgrp")
  p.maritalstat=request.POST.get("maritalstat")
  p.occupation=request.POST.get("occupation")
  p.save()
  return HttpResponseRedirect(reverse("admin"))

def addapptment(request):
  template = loader.get_template('newappt.html')
  pat=PatientData.objects.all()
  ps={p.pid:p.name for p in pat}
  doc=Employees.objects.filter(type="DR")
  surg=[]
  for i in doc:
    surg+=i.surgeries
  context={
    "patients":ps,
    "surgtype":surg
  }
  return HttpResponse(template.render(context,request))

@csrf_exempt
def addingappt(request):
  a=Appointments.objects.create()
  a.patient=request.POST.get("patientid")
  a.surgtype=request.POST.get("surgtype")
  t=request.POST.get("timeslot")
  if t!="":
    a.timeslot=t
  a.date=request.POST.get("date")
  c=CurrentAdmits.objects.create()
  c.appid=a.id
  c.pid=request.POST.get("patientid")
  c.status=1
  c.reports=[]
  a.save()
  c.save()
  return HttpResponseRedirect(reverse("admin"))

def createschedule():
    a=Appointments.objects.filter(date=datetime.now().date())
    surgeries=[]
    for i in a:
      if i.timeslot:
        surgeries.append(Surgery(i.id,i.surgtype,preassigned_time=i.timeslot))
      else:
        surgeries.append(Surgery(i.id,i.surgtype))
    doctors=[]
    d=Employees.objects.filter(type="DR")
    doctors=[]
    for i in d:
      doctors.append(Doctor(i.empid,i.name,i.surgeries))
    r=Rooms.objects.filter(type="OT")
    OTs=[]
    for i in r:
      OTs.append(OperationTheatre(i.rid,i.equipped))
    sched=Schedule(OTs)
    for i in surgeries:
      sched.schedule_surgery(i)
    a=assigndoc(sched,doctors)
    d,l={},[]
    for hour, slots in a.slots.items():
      l.append({hour:slots})
      for j in slots:
        if j is not None:
          print(j)
          a=Appointments.objects.get(id=list(j.keys())[0])
          a.timeslot=time(hour=hour)
          a.doctor=j[a.id][1]
          a.save()
          c=CurrentAdmits.objects.get(appid=list(j.keys())[0])
          e=Employees.objects.get(name=j[a.id][1])
          c.docid=e.empid
          c.save()
    d[datetime.now().strftime("%d/%m/%Y")]=l
    f=open("./medicare/schedule.json","w")
    json.dump(d, f)
    f.close()

def drugopt(request):
  template = loader.get_template('drugopt.html')
  p=PatientData.objects.all()
  pnames={pat.pid:pat.name for pat in p}
  context={
    "disptype":"none",
    "illness":['Pre-hypertension', 'Migraines with Aura', 'Seasonal Allergies & Eczema', 'High Blood Pressure', 'Anxiety & Insomnia', 'Osteoarthritis (mother)', 'Osteoporosis (mother)', 'Type 2 Diabetes & Glaucoma', 'Atrial Fibrillation', 'Type 2 Diabetes & Peripheral Neuropathy', 'Type 2 Diabetes', 'Sleep Apnea', 'Pre-Menstrual Syndrome (PMS)', 'Gout', 'Attention Deficit Hyperactivity Disorder (ADHD)', 'Depression (mother)', 'COPD, Heart Failure, & Edema', 'Seasonal Allergies', 'Seasonal Allergies & Hives', 'Anxiety', 'Depression', 'COPD (father)', 'Asthma (father)', 'Acne', 'High Cholesterol (father)', 'Irritable Bowel Syndrome (IBS) & Depression', 'Hypertension', 'Sleep Apnea & High Blood Pressure', 'Erectile Dysfunction', 'Arthritis', 'NSAID (Aleve)', 'Anxiety & Depression', 'Menopause symptoms', 'COPD, CKD, & Hypertension', 'Irritable Bowel Syndrome (IBS)', 'High Cholesterol', 'Depression & Anxiety', 'Osteoporosis', 'Migraine headaches', 'Osteoporosis & Chronic Pain', 'Hyperlipidemia & GERD'],
    "patients":pnames
  }
  return HttpResponse(template.render(context,request))

@csrf_exempt
def drugcalc(request):
  pid=request.POST.get("patient")
  p=PatientData.objects.get(pid=pid)
  age=request.POST.get("age")
  weight=request.POST.get("weight")
  gender=request.POST.get("gender")
  height=request.POST.get("height")
  illness=request.POST.get("illness")
  res=drugoptim(age,height,weight,gender,illness)
  template = loader.get_template('drugresults.html')
  print(res[3])
  context={
    "Drug":res[0],
    "Route":res[1],
    "Dosage":res[2],
    "imgurl":res[3],
    "patdata":{
      "Name":p.name,
      "Age":age,
      "Height":height,
      "Weight":weight,
      "Gender":gender,
      "Current Illness":illness
    }
  }
  return HttpResponse(template.render(context,request))
def schedule(request):
  template = loader.get_template('sched.html')
  f=open("./medicare/schedule.json")
  today=json.load(f)
  datenow=datetime.now().strftime("%d/%m/%Y")
  if datenow not in today:
    f.close()
    createschedule()
  f=open("./medicare/schedule.json")
  sched=today[datenow]
  schedule=[]
  for i in sched:
    slots=i[list(i.keys())[0]]
    for j in range(len(slots)):
      if slots[j] is not None:
        curr=slots[j]
        a=Appointments.objects.get(id=list(curr.keys())[0])
        p=PatientData.objects.get(pid=a.patient)
        try:
          if list(curr.values())[0][1]==request.session["user"]:
            schedule.append([list(i.keys())[0],int(j)+1,list(curr.keys())[0],list(curr.values())[0][1],list(curr.values())[0][0],p.name])
        except:
          schedule.append([list(i.keys())[0],int(j)+1,list(curr.keys())[0],list(curr.values())[0][1],list(curr.values())[0][0],p.name])
  print(schedule)
  context={
    "sched":schedule
  }
  return HttpResponse(template.render(context,request))

def patientform(request):
  template = loader.get_template('patientdata.html')
  return HttpResponse(template.render())

def billing(request):
  template = loader.get_template('billing.html')
  return HttpResponse(template.render())

def repupload(request,id=0):
  template = loader.get_template('uploadreport.html')
  c=CurrentAdmits.objects.filter(status=1)
  ps=[p.pid for p in c]
  pat=PatientData.objects.filter(pid__in=ps)
  l={p.pid:p.name for p in pat}
  if id!=0:
    a=PatientData.objects.get(pid=id)
    l={a.pid:a.name}
  print(l)
  context={
    "patients":l
  }
  return HttpResponse(template.render(context,request))

def showreports(request,id):
  p=RepScans.objects.filter(pid=id)
  a=PatientData.objects.get(pid=id)
  reps=[]
  for i in p:
    reps.append([i.report,i.comments])
    print("localhost:8000/media/"+str(i.report))
  context={
    "patients":reps,
    "name":a.name
  }
  template = loader.get_template('showreports.html')
  return HttpResponse(template.render(context,request))

@csrf_exempt
def uploadingrep(request):
  pid=request.POST.get("patientid")
  form = RepScansUpl(request.POST, request.FILES)  
  if form.is_valid():  
    obj=form.save()   
  r=RepScans.objects.get(id=obj.pk)
  r.pid=request.POST.get("pid")
  r.comments=request.POST.get("comments")
  try:
    c=CurrentAdmits.objects.get(pid=r.pid,status=1)
    c.status=2
    c.report=r.id
    c.save()
  except:
    pass
  r.save()
  return HttpResponseRedirect(reverse("admin"))

def ongoingpage(request):
  template = loader.get_template('activity.html')
  f=open("./medicare/schedule.json")
  schedule=json.load(f)
  if datetime.now().strftime("%d/%m/%Y") not in schedule:
    createschedule()
  today=schedule[datetime.now().strftime("%d/%m/%Y")]
  current=[time for time in today if list(time.keys())[0]==str(datetime.now().hour)][0][str(datetime.now().hour)]
  sched=[]
  for j in range(len(current)):
      print(current[j])
      if current[j] is None:
        sched.append(["free","free","free","free"])
      else:
        curr=current[j]
        sched.append([int(j)+1,list(curr.keys())[0],list(curr.values())[0][1],list(curr.values())[0][0]])
  context={
    "sched":sched
  }
  return HttpResponse(template.render(context,request))

def mritool(request):
  template = loader.get_template('mri.html')
  return HttpResponse(template.render())

def patrecpage(request):
  template = loader.get_template('patrecords.html')
  return HttpResponse(template.render())

def loginpage(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render())

def adminpage(request):
  template = loader.get_template('admin.html')
  return HttpResponse(template.render())

def loggingout(request):
  request.session.pop("user")
  return HttpResponseRedirect(reverse("login"))

def mdsspage(request):
  template = loader.get_template('mdss.html')
  return HttpResponse(template.render())

def docpage(request):
  template = loader.get_template('doctor.html')
  context={
    "user":request.session["user"]
  }
  return HttpResponse(template.render(context,request))

def doctordata(request):
  template = loader.get_template('doctordata.html')
  doc=Employees.objects.filter(type="DR")
  for i in doc:
    i.schedurl="sched/"+str(i.empid)
  context={
    "docs":doc
  }
  return HttpResponse(template.render(context,request))

@csrf_exempt
def loggingin(request):
    ei=request.POST.get("empid")
    print(ei)
    pw=request.POST.get("passw")
    try:
      e=Employees.objects.get(empid=int(ei[2:].lstrip("0")),type=ei[:2])
      print(e.password)
      if e.password==pw:
        if ei[:2]=="DR":
          request.session['user'] = e.name
          request.session["uid"]=e.empid
          return HttpResponseRedirect(reverse("doctor"))
      else:
        messages.success(request, "Password Incorrect!")
        return HttpResponseRedirect(reverse('login'))
    except Employees.DoesNotExist:
      print("hi")
      return HttpResponseRedirect(reverse('login'))
