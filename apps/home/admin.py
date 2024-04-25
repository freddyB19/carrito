from django.contrib import admin

from . import models

class ProductoAdmin(admin.ModelAdmin):
	ordering = ['id']

	list_display = [
		'id',
		'nombre'
	]
admin.site.register(models.Producto, ProductoAdmin)

class PedidoAdmin(admin.ModelAdmin):
	ordering = ['id']
	date_hierarchy = "creado"
	list_display = [
		'id',
		'creado'
	]

admin.site.register(models.Pedido, PedidoAdmin)


admin.site.register(models.DetallePedido)







