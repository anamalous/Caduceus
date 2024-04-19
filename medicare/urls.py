"""
URL configuration for medicare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/active/",views.ongoingpage),
    path("admin/",views.adminpage,name="admin"),
    path("admin/sched/",views.schedule),
    path("admin/docdata/",views.doctordata),
    path("admin/docdata/sched/<int:id>",views.schedule),
    path("admin/newappt/addingapt/",views.addingappt),
    path("admin/billing/",views.billing),
    path("doctor/",views.docpage,name="doctor"),
    path("doctor/patrecords/",views.docpatients),
    path("doctor/drugdb/",views.drugdb),
    path("doctor/drugdb/searching/",views.searchdrug),
    path("doctor/mdss/",views.mdsspage),
    path("doctor/heartdisease/",views.heartdis),
    path("doctor/heartdisease/heartassess/",views.heartassess),
    path("doctor/dosage/",views.drugopt),
    path("doctor/dosage/evaluatedrug/",views.drugcalc),
    path("doctor/loggingout/",views.loggingout),
    path("doctor/mriscan/",views.mritool),
    path("doctor/repupload/<int:id>",views.repupload),
    path("doctor/repupload/uploading/",views.uploadingrep),
    path("doctor/viewreps/<int:id>/",views.showreports),
    path("admin/repupl/",views.repupload),
    path("admin/repupl/uploading/",views.uploadingrep),
    path("doctor/repupl/",views.repupload),
    path("doctor/repupl/uploading/",views.uploadingrep),
    path("doctor/sched/",views.schedule),
    path("admin/newpatient/",views.patientform),
    path("admin/newpatient/adding/",views.addpatient),
    path("admin/newappt/",views.addapptment),
    path("home/",views.homepage,name="home"),
    path("login/",views.loginpage,name="login"),
    path("login/loggingin/",views.loggingin),
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)