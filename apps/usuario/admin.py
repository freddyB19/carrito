from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models

# Register your models here.
class UsuarioAdmin(BaseUserAdmin):
	ordering = ['id']

	list_display = [
		'id',
		'email'
	]


admin.site.register(models.Usuario)