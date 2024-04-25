from django.urls import reverse
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.core.paginator import Paginator

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Prefetch

from django.views.decorators.http import require_http_methods

from apps.usuario.models import Usuario
from . import models
from .carrito import Carrito

# Create your views here.

@require_http_methods(['GET'])
def index(request):
	carrito = Carrito(request)

	productos = models.Producto.objects.all()
	productos_carrito = carrito.get_productos(request.user.id)

	context = {
		'productos': productos,
		'carrito': productos_carrito.values(),
		'total': carrito.get_gasto_total(request.user.id)
	}
	return render(request, 'home/index.html', context)

@require_http_methods(['POST'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def add_carrito(request, producto_id=None):
	carrito = Carrito(request)

	try:
		producto = get_object_or_404(models.Producto, pk = producto_id)
	except models.Producto.DoesNotExist:
		raise e

	carrito.add(usuario = request.user.id, producto = producto)

	return HttpResponseRedirect(
		reverse('home:index')
	)


@require_http_methods(['POST'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def delete_producto_carrito(request, producto_id=None):
	carrito = Carrito(request)

	carrito.delete(usuario = request.user.id, producto_id = producto_id)

	return HttpResponseRedirect(
		reverse('home:index')
	)
	

@require_http_methods(['POST'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def limpiar_carrito(request):
	carrito = Carrito(request)

	carrito.clean(request.user.id)

	return HttpResponseRedirect(
		reverse('home:index')
	)


@require_http_methods(['GET'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def lista_pedidos_usuario(request, usuario_id = None):

	pedidos = models.Pedido.objects.filter(
			usuario_id = usuario_id
		)

	paginator = Paginator(pedidos, 3)
	lista_pedidos = paginator.get_page(request.GET.get('page'))

	context = {
		'pedidos': lista_pedidos
	}

	return render(request, 'home/lista_pedidos.html', context)

@require_http_methods(['GET'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def detalle_pedido_usuario(request, usuario_id = None,pedido_id = None):
	
	pedido = models.Pedido.objects.get(id = pedido_id, usuario_id = usuario_id)


	detalle_pedido = models.DetallePedido.objects.prefetch_related(
		Prefetch('productos')
	).filter(pedido_id = pedido.id)

	context = {
		'pedido': pedido,
		'detalle_pedido': detalle_pedido
	}

	return render(request, 'home/detalle_pedido.html', context)


@require_http_methods(['POST'])
@login_required(login_url = reverse_lazy('usuarios:login'))
def hacer_pedido(request):
	carrito = Carrito(request)

	productos = carrito.get_lista_productos()
	monto_total = carrito.get_gasto_total(request.user.id)


	if productos:
		pedido = models.Pedido(
			usuario = Usuario.objects.get(pk = request.user.id),
			total = monto_total
		)

		pedido.save()

		lista_productos = models.Producto.objects.filter(id__in = productos).order_by('id')
		productos_en_carrito = carrito.get_productos(request.user.id)
		

		lista_detalle_pedidos = []


		for pk, producto in zip(sorted(productos_en_carrito.keys()), lista_productos):
			cantidad = productos_en_carrito[pk]['total']

			detalle_pedido = models.DetallePedido(
				pedido = pedido,
				productos= producto,
				cantidad = cantidad
			)

			lista_detalle_pedidos.append(detalle_pedido)

		models.DetallePedido.objects.bulk_create(lista_detalle_pedidos)


		messages.success(request, 'El pedido fue realizado con exito.')

		carrito.clean(request.user.id)

		return HttpResponseRedirect(
			reverse(
				'home:pedido', 
				kwargs = {
					'pedido_id': pedido.id, 
					'usuario_id': request.user.id
				}
			)
			#reverse('home:pedido-lista')
		)
	
	messages.info(request, 'Usted no posee productos cargados en su carrito de compras.')

	return HttpResponseRedirect(
		reverse('home:index')
	)




