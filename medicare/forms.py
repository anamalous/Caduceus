from django.db import models  
from django.forms import fields  
from .models import *  
from django import forms  


class RepScansUpl(forms.ModelForm):  
    class Meta:  
        model = RepScans  
        fields = ["report"]

class searchdbupload(forms.ModelForm):  
    class Meta:  
        model = DBsearches  
        fields = ["scan"]
