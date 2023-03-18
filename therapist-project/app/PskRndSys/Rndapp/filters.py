from pyexpat import model
import django_filters as filters
from django import forms
from .models import *

class RandevuFilter(filters.FilterSet):
  
  dnsId__pskId = filters.ModelChoiceFilter(
    queryset = Terapist.objects.all(), label = "Terapist", widget = forms.Select(attrs={"class":"form-control"})
    )
  
  class Meta:
    model = Randevular
    fields = ['dnsId__pskId']
    


  
  

  
    
  
  

    

