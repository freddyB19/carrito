from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


from apps.home.carrito import Carrito
from . import forms
from . import models



# Create your views here.
@require_http_methods(['GET', 'POST'])
def crear_usuario(request):
	form = forms.CrearUsuario()

	if request.method == 'POST':
		form = forms.CrearUsuario(request.POST)

		if form.is_valid():
			usuario = form.save()

			messages.success(request, 'El usuario fue creado con existo.')

			return HttpResponseRedirect( reverse ('usuarios:login') )


	context = {'form': form}
	return render(request, 'usuario/crear_usuario.html', context)


@require_http_methods(['GET', 'POST'])
def login_usuario(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect( reverse('home:index') )
	
	form = forms.LoginForm()

	if request.method == 'POST':
		form = forms.LoginForm(request.POST)

		if form.is_valid():
			
			usuario = authenticate(
				email = form.cleaned_data.get('email'), 
				password = form.cleaned_data.get('password')
			)

			login(request, usuario)

			messages.success(request, f'Bienvenido, {usuario.nombre} al sistema.')


			return HttpResponseRedirect( reverse ('home:index') )


	context = {
		'form': form
	}
	return render(request, 'usuario/login.html', context)

@require_http_methods(['GET'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def logout_usuario(request):
	carrito = Carrito(request)

	if carrito.get_productos(request.user.id):
		return HttpResponseRedirect(reverse('usuarios:confirmar-logout'))

	logout(request)
	messages.success(request, 'Hasta pronto...')
	return HttpResponseRedirect(reverse('usuarios:login'))

@require_http_methods(['GET', 'POST'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def confirmar_logout(request):
	carrito = Carrito(request)

	if request.method == 'POST':
		carrito.clean(request.user.id)
		return HttpResponseRedirect(reverse('usuarios:logout'))
	
	context = {}
	return render(request, 'usuario/confirmar_logout.html', context)


@require_http_methods(['GET'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def settings_usuario(request, pk = None):
	try:
		usuario = get_object_or_404(models.Usuario, pk = pk)
	except Usuario.DoesNotExist:
		raise Http404('No existe un usuario con estos datos.')
	

	context = {
		'form_update_password': forms.UpdateUsuarioPassword(),
		'form_update_email': forms.UpdateUsuarioEmail(),
		'username': usuario.get_username()
	}
	return render(request, 'usuario/settings.html', context)


@require_http_methods(['GET', 'POST'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def update_usuario_password(request, pk = None):
	form = forms.UpdateUsuarioPassword()

	try:
		usuario = get_object_or_404(models.Usuario, pk = pk)
	except Usuario.DoesNotExist:
		raise Http404('No existe un usuario con estos datos.')

	if request.method == 'POST':
		
		form = forms.UpdateUsuarioPassword(request.POST)

		if form.is_valid():
			usuario.set_password(form.cleaned_data.get('new_password'))
			usuario.save()

			messages.success(request, f'Su contraseña fue actualizada correctamente.')

			return HttpResponseRedirect(
				reverse('usuarios:config-usuario', kwargs = {'pk': usuario.id})
			)


	context = {
		'form': form,
		'username': usuario.get_username()
	}

	return render(request, 'usuario/update_password.html', context)


@require_http_methods(['GET', 'POST'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def update_usuario_email(request, pk = None):
	form = forms.UpdateUsuarioEmail()

	try:
		usuario = get_object_or_404(models.Usuario, pk = pk)
	except Usuario.DoesNotExist:
		raise Http404('No existe un usuario con estos datos.')

	if request.method == "POST":
		form = forms.UpdateUsuarioEmail(request.POST)

		if form.is_valid():
			usuario.email = form.cleaned_data.get('new_email')
			usuario.save(update_fields=['email'])

			messages.success(request, f'Su email fue actualizado correctamente. {usuario.email}')

			return HttpResponseRedirect(
				reverse('usuarios:config-usuario', kwargs = {'pk': usuario.id})
			)

	context = {
		'form': form,
		'username': usuario.get_username()
	}

	return render(request, 'usuario/update_email.html', context)
