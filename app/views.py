from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Vehiculo, TipoVehiculo, Reserva, Carrito, Comentario
from django.contrib.auth.views import LoginView, redirect_to_login
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from .form import ComentarioForm
from django.views.decorators.csrf import csrf_exempt



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, '¡Cuenta creada con éxito!')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"Error en {field.label}: {error}")
        return super().form_invalid(form)

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    success_url = reverse_lazy('vehiculo-list')

def index(request):
    return render(request, 'app/index.html')


    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('opiniones')
    else:
        form = OpinionForm()

    opiniones = Opinion.objects.all().order_by('-fecha')

    for opinion in opiniones:
        opinion.estrellas = [True] * opinion.calificacion + [False] * (5 - opinion.calificacion)

    return render(request, 'app/opiniones.html', {'opiniones': opiniones, 'form': form})


@login_required
def opiniones_view(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    comentarios = Comentario.objects.filter(vehiculo=vehiculo)
    
    return render(request, 'app/opiniones.html', {
        'vehiculo': vehiculo,
        'comentarios': comentarios
    })




@login_required
def profile_view(request):
    return redirect(reverse('index'))


@login_required
def vehiculo_list(request):
    vehiculos = Vehiculo.objects.all()
    tipos_vehiculo = TipoVehiculo.objects.all()
    context = {
        'vehiculos': vehiculos,
        'tipos_vehiculo': tipos_vehiculo,
    }
    return render(request, 'app/vehiculo_list.html', context)

@login_required
def vehiculo_detalle(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    return render(request, 'app/vehiculo_detalle.html', {'vehiculo': vehiculo})

def cabezas(request):
    vehiculos = Vehiculo.objects.filter(tipo__tipo="Cabezas")
    context = {'vehiculos': vehiculos}
    return render(request, 'app/cabezas.html', context)

def trailer(request):
    vehiculos = Vehiculo.objects.filter(tipo__tipo="Trailer")
    context = {'vehiculos': vehiculos}
    return render(request, 'app/trailer.html', context)

def cisterna(request):
    vehiculos = Vehiculo.objects.filter(tipo__tipo="Cisterna")
    context = {'vehiculos': vehiculos}
    return render(request, 'app/cisterna.html', context)

def frigorifico(request):
    vehiculos = Vehiculo.objects.filter(tipo__tipo="Frigorifico")
    context = {'vehiculos': vehiculos}
    return render(request, 'app/frigorifico.html', context)

def lona(request):
    vehiculos = Vehiculo.objects.filter(tipo__tipo="Lona")
    context = {'vehiculos': vehiculos}
    return render(request, 'app/lona.html', context)


class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'app/reserva_list.html'
    context_object_name = 'reservas'
    login_url = '/login/'

    def get_queryset(self):
        user = self.request.user
        return Reserva.objects.filter(cliente=user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.login_url)
        else:
            raise PermissionDenied("No tienes permiso para ver esta página.")

@login_required
def reservar_vehiculo(request):
    if request.method == 'POST':
        vehiculo_id = request.POST['vehiculo_id']
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        metodo_pago = request.POST['metodo_pago']
        trayecto = request.POST['trayecto']

        vehiculo = Vehiculo.objects.get(id=vehiculo_id)

        Reserva.objects.create(
            cliente=request.user,
            vehiculo=vehiculo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            metodo_pago=metodo_pago,
            trayecto=trayecto
        )

        messages.success(request, 'Reserva realizada con éxito.')
        return redirect('reserva-list')

    vehiculos = Vehiculo.objects.all()
    return render(request, 'app/reservar_vehiculo.html', {'vehiculos': vehiculos})

@login_required
def agregar_al_carrito(request, vehiculo_id):
    try:
        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    except Vehiculo.DoesNotExist:
        return redirect('vehiculo-list')

    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito.vehiculos.add(vehiculo)
    messages.success(request, f'{vehiculo} añadido al carrito.')
    return redirect('carrito')


@login_required
def carrito(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        vehiculos = carrito.vehiculos.all()
    except Carrito.DoesNotExist:
        vehiculos = []
        messages.error(request, 'No tienes vehículos en tu carrito.')

    return render(request, 'app/carrito.html', {'carrito': carrito, 'vehiculos': vehiculos})


@login_required
def realizar_pago(request):
    carrito = request.session.get('carrito', [])
    if not carrito:
        messages.error(request, 'No hay vehículos en el carrito.')
        return redirect('carrito')

    vehiculos = Vehiculo.objects.filter(id__in=carrito)
    total = sum(vehiculo.precio for vehiculo in vehiculos)

    if request.method == 'POST':
        # Aquí procesarías el pago
        messages.success(request, 'Pago realizado con éxito.')
        request.session['carrito'] = []  # Limpiar el carrito después del pago
        return redirect('index')

    return render(request, 'app/realizar_pago.html', {'total': total})


@login_required
def opiniones(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    comentarios = vehiculo.comentarios.filter(aprobado=True)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)  # No guardamos aún en la base de datos
            comentario.vehiculo = vehiculo  # Asociamos el comentario al vehículo
            comentario.save()  # Guardamos el comentario
            return redirect('opiniones', pk=vehiculo.pk)
    else:
        form = ComentarioForm()  # Si es una petición GET, creamos un formulario vacío

    return render(request, 'app/opiniones.html', {'vehiculo': vehiculo, 'comentarios': comentarios, 'form': form})


@login_required
def buscar_vehiculo(request):
    query = request.GET.get('q', '')  # Captura el término de búsqueda
    resultados = Vehiculo.objects.filter(nombre__icontains=query) if query else []
    return render(request, 'buscar.html', {'query': query, 'resultados': resultados})
