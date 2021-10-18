from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.forms import widgets
from .models import Contacto, Estacionamiento
from django.forms import ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    patente = forms.CharField(label='Patente')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)

    def clean_nombre(self):
        usuario = self.cleaned_data["usuario"]
        existe = UserRegisterForm.objects.filter(usuario__iexact=usuario).exists()

        if existe:
            raise ValidationError("Este nombre de usuario ya existe")

        return usuario

    class Meta:
        model = User
        fields = ['username','email','patente','password1','password2']
        help_texts = {k:"" for k in fields}

class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = '__all__'

class EstacionamientoForm(forms.ModelForm):

    nombre = forms.CharField(min_length=3, max_length=50)
    precio = forms.IntegerField(min_value=1, max_value=1500000)

    class Meta:
        model = Estacionamiento
        fields = '__all__'

    widgets = {
        "fecha-publicacion": forms.SelectDateWidget()
    }