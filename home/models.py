from django.db import models
from django import forms
# Create your models here.
# models.py
class Hotel(models.Model):
	Image = models.ImageField(upload_to='img/')
	
class HotelForm(forms.ModelForm):

    class Meta:
        model = Hotel
        fields = ['Image']
