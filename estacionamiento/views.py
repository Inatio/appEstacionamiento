from django.core import paginator
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets
from .serializers import EstacionamientoSerializer, ComunaSerializer

import estacionamiento
from .forms import UserRegisterForm
from .models import Estacionamiento, Comuna
from .forms import ContactoForm, EstacionamientoForm
from django.shortcuts import render, redirect, get_object_or_404

from estacionamiento import serializers

class ComunaViewset(viewsets.ModelViewSet):
    queryset = Comuna.objects.all()
    serializer_class = ComunaSerializer

class EstacionamientoViewset(viewsets.ModelViewSet):
    queryset = Estacionamiento.objects.all()
    serializer_class = EstacionamientoSerializer

    def get_queryset(self):
        estacionamientos = Estacionamiento.objects.all()

        nombre = self.request.GET.get('nombre')

        if nombre:
            estacionamientos = estacionamientos.filter(nombre__contains=nombre)

        return estacionamientos

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('profile')
    else:
        form = UserRegisterForm()

    context = { 'form' : form}
    return render(request, 'accounts/register.html', context)

def index(request):
    print(request.user)
    return render(request, "index.html")
    
def about(request):
    return render(request, "about.html")
    
def contact(request):
    data = {
        'form': ContactoForm()
    }
    
    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "contacto guardado"
        else:
            data["form"] = formulario

    return render(request, "contact.html", data)

@login_required
def reservas(request):
    estacionamientos = Estacionamiento.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(estacionamientos, 5)
        estacionamientos = paginator.page(page)
    except:
        raise Http404


    data = {
        'estacionamientos': estacionamientos
    }

    return render(request, "reservas.html", data)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

@login_required
def agregar_estacionamiento(request):

    data = {
        'form' : EstacionamientoForm()
    }

    if request.method == 'POST':
        formulario = EstacionamientoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "guardado correctamente"
        else:
            data["form"] = formulario

    return render(request, 'reserva/agregar.html', data)

@login_required
def modificar_estacionamiento(request, id):

    estacionamiento = get_object_or_404(Estacionamiento, id=id)

    data = {
        'form': EstacionamientoForm(instance=estacionamiento)
    }

    if request.method == 'POST':
        formulario = EstacionamientoForm(data=request.POST, instance=estacionamiento, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "modificado correctamente")
            return redirect(to="reservas")
        data['form'] = formulario

    return render(request, 'reserva/modificar.html', data)

@login_required
def eliminar_estacionamiento(request, id):
    estacionamiento = get_object_or_404(Estacionamiento, id=id)
    estacionamiento.delete()
    messages.success(request, "eliminado correctamente")

    return redirect(to="reservas")