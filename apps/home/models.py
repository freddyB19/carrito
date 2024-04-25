from django.db import models
from django.urls import reverse

from apps.usuario.models import Usuario

# Create your models here.
class Producto(models.Model):
	nombre = models.CharField(max_length = 30)
	precio = models.FloatField(default = 2.10)
	descripcion = models.TextField(max_length= 150)
	imagen = models.CharField(max_length = 30, blank=True, null=True)


	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
		ordering = ['nombre']


	def __str__(self):
		return f"{self.nombre}"

class Pedido(models.Model):
	usuario = models.ForeignKey(
		Usuario,
		on_delete = models.SET_NULL,
		blank=True,
		null=True,
		related_name='pedidos'
	)
	total = models.FloatField(default = 0.0)
	creado = models.DateTimeField(auto_now_add=True)
	activo = models.BooleanField(default = True)


	class Meta:
		verbose_name = 'Pedido'
		verbose_name_plural = 'Pedidos'
		ordering = ['-creado']

	def get_absolute_url(self):
		return reverse('home:pedido', kwargs = {'pedido_id': self.pk, 'usuario_id': self.usuario.id})

	def __str__(self):
		return f"{self.creado}"


class DetallePedido(models.Model):
	pedido = models.ForeignKey(
		Pedido,
		related_name='detalle_pedido',
		on_delete = models.CASCADE,
		null = True,
		blank=True
	)
	productos = models.ForeignKey(
		Producto,
		related_name='detalle_pedido_productos',
		on_delete = models.CASCADE,
		null = True,
		blank=True
	)
	cantidad = models.PositiveSmallIntegerField(default = 1)


	class Meta:
		verbose_name = 'DetallePedido'
		verbose_name_plural = 'DetallePedidos'

	def __str__(self):
		return f"Nª: {self.id} - Pedido: {self.pedido}"
