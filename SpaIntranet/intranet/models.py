from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=60)
    telefono = models.CharField(max_length=15)  

class FichaClinica(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60)
    fecha_cita = models.DateField()
    telefono = models.CharField(max_length=15)      
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=30, blank=True)
    motivo_consulta = models.CharField(max_length=30, blank=True)
    cardiovasculares = models.CharField(max_length=30, blank=True)
    pulmonares = models.CharField(max_length=30, blank=True)
    digestivos = models.CharField(max_length=30, blank=True)
    otros = models.CharField(max_length=30, blank=True)
    sexo = models.CharField(max_length=4, blank=True)
    estado_civil = models.CharField(max_length=10, blank=True)
    renales = models.CharField(max_length=30, blank=True)
    alergicos = models.CharField(max_length=30)
    quirurgicos = models.CharField(max_length=30)
    respiratorios = models.CharField(max_length=30, blank=True)
    alcoholismo = models.CharField(max_length=2, blank=True)
    tabaquismo = models.CharField(max_length=2, blank=True)
    drogas = models.CharField(max_length=20, blank=True)
    otro = models.CharField(max_length=20, blank=True)
    madre = models.CharField(max_length=2, blank=True)
    enfermed_madre = models.CharField(max_length=30, blank=True)
    padre = models.CharField(max_length=2, blank=True)
    enfermed_padre = models.CharField(max_length=30, blank=True)
    inicio_menstruacion = models.IntegerField(null=True, blank=True)
    ciclo_menstruacion = models.IntegerField(null=True, blank=True)
    duracion_menstruacion = models.IntegerField(null=True, blank=True)
    ultima_regla = models.DateField(null=True, blank=True)
    anticonceptivos = models.CharField(max_length=2, blank=True)
    menopausia = models.CharField(max_length=2, blank=True)
    exploracion_fisica = models.CharField(max_length=35, blank=True)
    peso = models.FloatField() 
    talla = models.FloatField()  # No se especifica precisión y escala ya que mas adelante sera retirado de SQL
    imc = models.FloatField(null=True, blank=True) 

class Personal(models.Model):
    nombre = models.CharField(max_length=60)
    horario_laboral = models.CharField(max_length=100, blank=True)
    #ESTA ES UNA LISTA DE TUPLAS PARA DEFINIR EL STATUS DEL PERSONAL 
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('no_disponible', 'No Disponible'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,#ESTE PARAMETRO LIMITARA LAS OPCIONES EN LOS FORMULARIOS
        default='disponible',
    )

class Cita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_cita = models.DateField()
    horario = models.TimeField(null=True, blank=True)
    servicio = models.CharField(max_length=25, blank=True)
    metodo_pago = models.CharField(max_length=15, blank=True)
    paquete = models.CharField(max_length=2, blank=True)
    total_sesiones = models.CharField(max_length=1, blank=True)
    sesiones_tomadas = models.CharField(max_length=1, blank=True)
    sesiones_faltantes = models.CharField(max_length=1, blank=True)
    # ForeignKey para referenciar al personal asignado a la cita
    asignado_a = models.ForeignKey(
        Personal, 
        on_delete=models.SET_DEFAULT,  # Cambiar el comportamiento de eliminación
        default=None,  # Valor predeterminado
        null=True, 
        blank=True,  # Permitir valores en blanco
        related_name='citas_asignadas'  # Nombre para la relación inversa
    )
    STATUS_CHOICES = [
        ('por_confirmar', 'Por confirmar'),
        ('asistio', 'Asistio'),
        ('cancelada', 'Cancelada'),
        ('reagendada', 'Reagendada'),110
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='por_confirmar',
    )


