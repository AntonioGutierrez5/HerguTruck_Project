from django.contrib import admin
from .models import TipoVehiculo, Conductor, Vehiculo, Reserva, Comentario

@admin.register(TipoVehiculo)
class TipoVehiculoAdmin(admin.ModelAdmin):
    list_display = ('tipo',)

@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono')
    filter_horizontal = ('vehiculo_permitido',)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'disponible')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'conductor', 'fecha_inicio', 'fecha_fin', 'metodo_pago')
    list_filter = ('vehiculo', 'conductor', 'metodo_pago')
    search_fields = ('vehiculo__tipo', 'conductor__nombre')


admin.site.register(Comentario)
