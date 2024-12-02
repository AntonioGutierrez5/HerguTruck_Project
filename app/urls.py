from django.urls import path
from . import views
from .views import RegisterView, CustomLoginView, profile_view

urlpatterns = [
    path('', views.index, name='index'),
    path('vehiculos/cabezas/', views.cabezas, name='cabezas'),
    path('vehiculos/trailer/', views.trailer, name='trailer'),
    path('vehiculos/cisterna/', views.cisterna, name='cisterna'),
    path('vehiculos/frigorifico/', views.frigorifico, name='frigorifico'),
    path('vehiculos/lona/', views.lona, name='lona'),
    path('reservas/', views.ReservaListView.as_view(), name='reserva-list'),
    path('reservar-vehiculo/', views.reservar_vehiculo, name='reservar-vehiculo'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar-al-carrito'),
    path('carrito/', views.carrito, name='carrito'),
    path('realizar-pago/', views.realizar_pago, name='realizar-pago'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('accounts/profile/', profile_view, name='profile'),
    path('vehiculos/', views.vehiculo_list, name='vehiculo-list'),  # Ruta para la lista de vehículos
    path('agregar-al-carrito/<int:vehiculo_id>/', views.agregar_al_carrito, name='agregar-al-carrito'),
    path('opiniones/<int:pk>/', views.opiniones, name='opiniones'),
    path('opiniones/<int:vehiculo_id>/', views.opiniones_view, name='opiniones'),
    path('buscar/', views.buscar_vehiculo, name='buscar'),


]
