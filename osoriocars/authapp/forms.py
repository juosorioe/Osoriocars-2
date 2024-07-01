from django import forms
import os
from django.conf import settings
from .models import Service, CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_mechanic']

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_mechanic']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


class ServiceForm(forms.ModelForm):
    # Obtener la lista de imágenes en la carpeta static/img
    img_dir = os.path.join(settings.STATICFILES_DIRS[0], 'img')
    choices = [(f'img/{img}', img) for img in os.listdir(img_dir) if img.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    
    image = forms.ChoiceField(choices=choices, required=True)

    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'image']