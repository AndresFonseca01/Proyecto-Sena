from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from autenticacion.models import User


def index(request):
    return render(request, 'index.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'], email=request.POST['email'], last_name=request.POST['last_name'], first_name=request.POST['first_name'], document=request.POST['document'])
                user.save()
                login(request, user)
                return redirect('traductor')
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm, "error": "Nombre de usuario o  Correo ya existen"
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
