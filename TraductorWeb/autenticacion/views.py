from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from autenticacion.models import User
import re


def index(request):
    return render(request, 'index.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': UserCreationForm
        })
    else:
        # Validación del correo electrónico
        email = request.POST['email']
        if not re.match(r'^[\w\.-]+@(misena\.edu\.co|soy\.sena\.edu\.co)$', email):
            return render(request, 'registro.html', {
                'form': UserCreationForm, "error": "El correo debe ser de @misena.edu.co o @soy.sena.edu.co"
            })

        # Validación de la contraseña
        password1 = request.POST['password1']
        if len(password1) < 5:
            return render(request, 'registro.html', {
                'form': UserCreationForm, "error": "La contraseña debe tener al menos 5 caracteres"
            })

        # Crear el usuario si las validaciones pasan
        if password1 == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=password1, email=email, last_name=request.POST['last_name'], first_name=request.POST['first_name'], document=request.POST['document'])
                user.save()
                login(request, user)
                return redirect('traductor')
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm, "error": "Nombre de usuario o correo ya existen"
                })
        return render(request, 'registro.html', {
            'form': UserCreationForm, "error": "Las contraseñas no coinciden"
        })


@login_required
def traductor(request):
    return render(request, 'traductor.html')


@login_required
def signout(request):
    logout(request)
    return redirect('index')


def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, email=request.POST['email'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': '¡ Correo o contraseñas incorrectos !'
            })
        else:
            login(request, user)
            return redirect('traductor')
