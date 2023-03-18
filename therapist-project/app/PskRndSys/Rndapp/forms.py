from django import forms
from django.forms import ModelForm
from .models import Danisan, Randevular, Terapist


class LoginForm(forms.Form):
    username= forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    
# Create a Danisan form
class DanisanForm(ModelForm):
    
    class Meta:
        model = Danisan
        fields = "__all__"
        
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "second_name": forms.TextInput(attrs={"class":"form-control"}),
            "phone": forms.TextInput(attrs={"class":"form-control", "value": "+90"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
            "born": forms.DateInput(attrs={"class":"form-control"}),
            "price": forms.NumberInput(attrs={"class":"form-control"}),
            "gender": forms.Select(attrs={"class":"form-control"}),
            "pskId": forms.Select(attrs={"class":"form-control"})
        }
        
        labels = {
            "name":"Isim",
            "second_name":"Soyisim",
            "phone":"No",
            "born":"Doğum Tarihi",
            "price":"Ücret",
            "gender":"Cinsiyet",
            "pskId":"Terapist"
        }

class TerapistForm(ModelForm):
    
    class Meta:
        model = Terapist
        fields = "__all__"
        
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "second_name": forms.TextInput(attrs={"class":"form-control"}),
            "phone": forms.TextInput(attrs={"class":"form-control", "value": "+90"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
            "gender": forms.Select(attrs={"class":"form-control"})
        }
        
        labels = {
            "name":"Isim",
            "second_name":"Soyisim",
            "phone":"No",
            "gender":"Cinsiyet"
        }

class RandevuForm(ModelForm):
        
    class Meta:
        model = Randevular
        fields = "__all__"       
        exclude = ["passed"]
 
        widgets = {
            "dnsId": forms.Select(attrs={"class":"form-control"}),
            "rndTime": forms.DateTimeInput(attrs={"class":"form-control"}),
            "passed": forms.NumberInput(attrs={"class":"form-control"})
        }
        
        labels = {
            "dnsId":"Danışan",
            "rndTime":"Tarih",
            "passed": "Geçme Durumu"
        }

