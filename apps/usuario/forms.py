from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from . import models


class CrearUsuario(forms.ModelForm):
	password_1 = forms.CharField(label = 'Contraseña', required = True , widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Contraseña",
				'class': 'form-control form-control-lg',
				'id': 'password-input'
			}
		))
	password_2 = forms.CharField(label = 'Confirmar Contraseña', required = True , widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Repetir Contraseña",
				'class': 'form-control form-control-lg',
				'id': 'password-conf-input'
			}
		))

	class Meta:
		model = models.Usuario
		fields = (
			'nombre',
			'apellido',
			'email'
		)

		widgets={
			'nombre': forms.TextInput( 
				attrs = {
					'class': 'form-control form-control-lg', 
					'id': 'nombre-input'
				}
			),
			'apellido': forms.TextInput( 
				attrs = {
					'class': 'form-control form-control-lg', 
					'id': 'apellido-input'
				}
			),
			'email': forms.EmailInput( 
				attrs = {
					'class': 'form-control form-control-lg', 
					'id': 'apellido-input'
				}
			),
		}

	def clean_email(self):
		email = self.cleaned_data['email']

		if models.Usuario.objects.filter(email = email):
			self.add_error('email', 'Ya existe un usuario con este email.')

		return email

	def clean(self):
		self.cleaned_data = super().clean()

		password_1 = self.cleaned_data['password_1']
		password_2 = self.cleaned_data['password_2']

		if password_1 != password_2:
			raise forms.ValidationError('Las contraseñas no coinciden.')

		return self.cleaned_data

	def save(self):
		return models.Usuario.objects.create_user(
			email = self.cleaned_data['email'],
			password = self.cleaned_data['password_1'],
			nombre = self.cleaned_data['nombre'],
			apellido = self.cleaned_data['apellido'],
		)


class LoginForm(forms.Form):
	email = forms.EmailField(label = 'Email', required = True ,widget = forms.EmailInput(
		attrs = {"class": "form-control form-control-lg", 'id': 'email-input'}
	))
	password = forms.CharField(label = 'Contraseña', required = True , widget = forms.PasswordInput(
		attrs = {
			"placeholder": "Ingrese su contraseña",
			"class": "form-control form-control-lg", 
			'id': 'password-input'
		}
	))

	def clean(self):
		self.cleaned_data = super().clean()

		if not authenticate(email = self.cleaned_data['email'], password = self.cleaned_data['password']):
			raise forms.ValidationError('Las credenciales son invalidas')

		return self.cleaned_data


class UpdateUsuarioPassword(forms.Form):
	new_password = forms.CharField(label = 'Nueva Contraseña', required = True , widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Contraseña",
				"class": "form-control form-control-lg",
				'id': 'new-password-input'
			}
		))


	email = forms.EmailField(label = 'Email', required = True, help_text = 'Introduce tus credenciales para confirmar la configuración',widget = forms.EmailInput(
		attrs = {
			"class": "form-control form-control-lg", 
			'id': 'email-input'
		}
	))
	password = forms.CharField(label = 'Contraseña', required = True , widget = forms.PasswordInput(
			attrs = {
				"placeholder": "Contraseña",
				"class": "form-control form-control-lg",
				"id": 'password-input'
			}
		))
	


	def clean_new_password(self):
		new_password = self.cleaned_data.get('new_password')

		if len(new_password) <= 4:
			self.add_error('new_password', 'La contraseña es muy corta.')

		return new_password

	def clean(self):
		self.cleaned_data = super().clean()

		if not authenticate(email = self.cleaned_data['email'], password = self.cleaned_data['password']):
			raise forms.ValidationError('Las credenciales son invalidas.')

		return self.cleaned_data

	


class UpdateUsuarioEmail(forms.Form):
	
	new_email = forms.EmailField(label = 'Nuevo Email', required = True,widget = forms.EmailInput(
		attrs = {
			"class": "form-control form-control-lg",
			"id": "new-email-input"
		}
	))
	
	email = forms.EmailField(label = 'Email', required = True, help_text = 'Introduce tus credenciales para confirmar la configuración', widget = forms.EmailInput(
		attrs = {
			"class": "form-control form-control-lg",
			"id": "email-input"
		}
	))
	password = forms.CharField(label = 'Confirmar Contraseña', required = True , widget = forms.PasswordInput(
		attrs = {
			"placeholder": "Contraseña",
			"class": "form-control form-control-lg",
			"id": "password-input"
		}
	))

	def clean_new_email(self):
		email = self.cleaned_data['new_email']

		if models.Usuario.objects.filter(email = email):
			self.add_error('email', 'Ya existe un usuario con este email.')

		return email

	def clean(self):
		self.cleaned_data = super().clean()

		if not authenticate(email = self.cleaned_data['email'], password = self.cleaned_data['password']):
			raise forms.ValidationError('Las credenciales son invalidas.')

		return self.cleaned_data




