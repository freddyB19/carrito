class Carrito:
	def __init__(self, request):
		self.request = request
		self.session = self.request.session

		if  'carrito' not in self.session:
			self.session['carrito'] = {}

		self.carrito = self.session['carrito']

	def get_productos(self, usuario):
		if str(usuario) in self.carrito.keys():
			return self.carrito[str(usuario)]
		return {}


	def get_gasto_total(self, usuario):
		if 'gasto' in self.carrito:
			return self.carrito['gasto']
		return 0



	def save(self):
		self.session['carrito'] = self.carrito
		self.session.modified = True


	def add_lista_productos(self, producto):
		if 'productos' in self.carrito.keys():
			self.carrito['productos'] += [producto]
		else:
			self.carrito['productos'] = [producto]

		self.save()

	def push_lista_productos(self, producto):
		if 'productos' in self.carrito.keys():
			if producto in self.carrito['productos']:
				self.carrito['productos'].remove(producto)

				self.save()
	def get_lista_productos(self):
		if 'productos' in self.carrito.keys():
			return self.carrito['productos']
		return []

	def add(self, usuario, producto):
		if str(usuario) in self.carrito.keys():
			if str(producto.id) in self.carrito[str(usuario)].keys():
				self.carrito[str(usuario)][str(producto.id)]['total'] += 1
			else:
				self.carrito[str(usuario)][str(producto.id)] = {
					'id': producto.id,
					'nombre': producto.nombre,
					'precio': producto.precio,
					'total': 1
				}
		else:
			self.carrito[str(usuario)] = {
				str(producto.id): {
					'id': producto.id,
					'nombre': producto.nombre,
					'precio': producto.precio,
					'total': 1
				}
			}
		
		self.save()

		self.set_total(monto = producto.precio)
		self.add_lista_productos(producto.id)

		

	def delete(self, usuario, producto_id):
		if str(usuario) in self.carrito.keys():
			if str(producto_id) in self.carrito[str(usuario)].keys():
				self.carrito[str(usuario)][str(producto_id)]['total'] -= 1

				precio = self.carrito[str(usuario)][str(producto_id)]['precio']

				if self.carrito[str(usuario)][str(producto_id)]['total'] == 0:
					producto = self.carrito[str(usuario)].pop(str(producto_id))

					precio = producto['precio']
				
				self.save()

				self.set_total(
					monto =  precio, #self.carrito[str(usuario)][str(producto_id)]['precio'], 
					opc = False
				)
				
				self.push_lista_productos(producto_id)
				


	def clean(self, usuario):
		if str(usuario) in self.carrito.keys():
			if self.carrito[str(usuario)]:
				self.carrito[str(usuario)] = {}

				if 'gasto' in self.carrito:
					self.carrito['gasto'] = 0
				if 'productos' in self.carrito:
					self.carrito['productos'] = []

				self.save()


	def set_total(self, monto, opc = True):
		if opc:
			if 'gasto' in self.carrito.keys():
				self.carrito['gasto'] += monto
			else:
				self.carrito['gasto'] = monto
		else:
			if 'gasto' in self.carrito.keys():
				self.carrito['gasto'] -= monto

				if self.carrito['gasto'] < 0:
					self.carrito['gasto'] = 0
		self.save()




