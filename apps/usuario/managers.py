from django.db import models
from django.contrib.auth.models import BaseUserManager


class UsuarioManager(BaseUserManager):
	def create_user(self, email, password = None, **extra_fields):
		if not email:
			raise ValueError("Debe ingresar un email.")
		if password is None:
			raise ValueError("Debe ingresar un email.")

		usuario = self.model(
			email = self.normalize_email(email),
			**extra_fields
		)

		usuario.set_password(password)
		usuario.save(using = self._db)

		return usuario


	def create_superuser(self, email, password = None, **extra_fields):

		usuario = self.create_user(email, password, **extra_fields)

		usuario.is_admin = True
		usuario.is_staff = True
		usuario.is_superadmin = True

		usuario.save(using = self._db)
		return usuario
