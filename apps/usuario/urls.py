from django.urls import path

from . import views

app_name = 'usuarios'
urlpatterns = [
	path('crear/', views.crear_usuario , name = 'crear-usuario'),
	path('login/', views.login_usuario , name = 'login'),
	path('logout/', views.logout_usuario , name = 'logout'),
	path('confirmar-logout/', views.confirmar_logout , name = 'confirmar-logout'),
	path('config/<int:pk>/usuario/', views.settings_usuario , name = 'config-usuario'),
	path('update/password/<int:pk>/usuario/', views.update_usuario_password , name = 'update-password'),
	path('update/email/<int:pk>/usuario/', views.update_usuario_email , name = 'update-email'),

]