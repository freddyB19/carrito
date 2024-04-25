from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from . import managers
# Create your models here.


class Usuario(AbstractBaseUser):
	nombre = models.CharField(max_length = 50, blank=True, null=True)
	apellido = models.CharField(max_length = 50, blank=True, null=True)
	email = models.EmailField(unique=True)

	is_active = models.BooleanField(default = True )
	is_admin = models.BooleanField(default = False)
	is_staff = models.BooleanField(default = False)
	is_superadmin = models.BooleanField(default = False)


	objects = managers.UsuarioManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['nombre', 'apellido']

	class Meta:
		verbose_name = 'Usuario'
		verbose_name_plural = 'Usuarios'

	def has_perm(self, perm, obj = None):
		return self.is_admin

	def has_module_perms(self, add_label):
		return True

	def nombre_completo(self):
		return f"{self.nombre} {self.apellido}"

	def get_username(self):
		return f"{self.email[ :  self.email.find('@') + 1]}"


	def __str__(self):
		return f"{self.email}"



