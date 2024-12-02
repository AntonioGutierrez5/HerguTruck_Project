from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone



class TipoVehiculo(models.Model):
    TIPO_VEHICULO = [
        ('c_megacamion', 'Megacamion'),
        ('c_articulado', 'Articulado'),
        ('c_cisterna', 'Cisterna'),
        ('c_frigorifico', 'Frigorifico'),
        ('c_lona', 'Lona'),
    ]
    
    tipo = models.CharField(max_length=50, choices=TIPO_VEHICULO, unique=True)

    def __str__(self):
        return self.tipo


class Conductor(models.Model):
    nombre = models.CharField(max_length=100)
    vehiculo_permitido = models.ManyToManyField(TipoVehiculo)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre



class Vehiculo(models.Model):
    tipo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo}"


class Reserva(models.Model):
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    trayecto = models.CharField(max_length=255)
    metodo_pago = models.CharField(max_length=50)
    cliente = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = ('vehiculo', 'fecha_inicio', 'fecha_fin')

    def clean(self):
        if self.fecha_inicio >= self.fecha_fin:
            raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')
 
        
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    vehiculos = models.ManyToManyField(Vehiculo)

    def __str__(self):
        return f"Carrito de {self.usuario}"


class Comentario(models.Model):
    vehiculo = models.ForeignKey('Vehiculo', related_name='comentarios', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    mensaje = models.TextField()
    correo = models.DateTimeField(default=timezone.now)
    aprobado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.mensaje





