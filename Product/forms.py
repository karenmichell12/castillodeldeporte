from concurrent.futures import process
from dataclasses import fields
from unicodedata import category
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):

    class Meta:
     model = User
     fields = ["username","first_name","last_name","email","password1","password2"]

class CalificationForm(forms.ModelForm):

    class Meta:
        model = Califications
        fields = ["Producto","Calification","Comentary"]

class Direccionform(forms.ModelForm):
    class Meta:
     model = Direccion
     fields = ["line1","line2","city","state","postal_code"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['line1'].widget.attrs.update({
            'class':'form-control'
        })
        self.fields['line2'].widget.attrs.update({
            'class':'form-control'
        })

        self.fields['city'].widget.attrs.update({
            'class':'form-control'
        })

        self.fields['state'].widget.attrs.update({
            'class':'form-control'
        })

        self.fields['postal_code'].widget.attrs.update({
            'class':'form-control'
        })

    