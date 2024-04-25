from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
	path("", views.index, name = 'index'),

	path("add/<int:producto_id>/carrito/", views.add_carrito, name = 'add-carrito'),
	path("delete/<int:producto_id>/carrito/", views.delete_producto_carrito, name = 'delete-carrito'),
	path("vaciar/carrito/", views.limpiar_carrito, name = 'vaciar-carrito'),

	path('crear/pedido/', views.hacer_pedido, name = 'hacer-pedido'),

	path(
		'usuario/<int:usuario_id>/lista/pedidos/', 
		views.lista_pedidos_usuario, 
		name = 'pedido-lista'
	),
	path(
		'usuario/<int:usuario_id>/detalle/<int:pedido_id>/pedido/', 
		views.detalle_pedido_usuario, 
		name = 'pedido'
	),

]
