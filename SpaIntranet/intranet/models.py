from django.db import models

class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=30)
    telefono_cliente = models.CharField(max_length=15, unique=True) 

class FichaClinica(models.Model):
    nombre_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_ficha = models.DateTimeField(null=True, blank=True)  
    edad = models.IntegerField(null=False, blank=False)
    ocupacion = models.CharField(max_length=30, blank=True, null=True)
    motivo_consulta = models.CharField(max_length=30, null=False, blank=False)
    cardiovasculares = models.CharField(max_length=20, null=False, blank=False)
    pulmonares = models.CharField(max_length=20, null=False, blank=False)
    digestivos = models.CharField(max_length=20, null=False, blank=False)
    otros = models.CharField(max_length=20, null=False, blank=False)
    sexo = models.CharField(max_length=2, null=True, blank=True)
    estado_civil = models.CharField(max_length=10, null=True, blank=True)
    renales = models.CharField(max_length=20, null=False, blank=False)
    alergicos = models.CharField(max_length=30, null=False, blank=False)
    quirurgicos = models.CharField(max_length=20, null=False, blank=False)
    respiratorios = models.CharField(max_length=20, null=False, blank=False)
    alcoholismo = models.CharField(max_length=10, null=True, blank=True)
    tabaquismo = models.CharField(max_length=10, null=True, blank=True)
    drogas = models.CharField(max_length=2, null=True, blank=True)
    otro = models.CharField(max_length=10, null=True, blank=True)
    madre = models.CharField(max_length=2, null=True, blank=True)
    enfermed_madre = models.CharField(max_length=30, null=False, blank=False)
    padre = models.CharField(max_length=2, null=True, blank=True)
    enfermed_padre = models.CharField(max_length=30,null=False, blank=False)
    inicio_menstruacion = models.IntegerField(null=True, blank=True)
    ciclo_menstruacion = models.IntegerField(null=True, blank=True)
    duracion_menstruacion = models.IntegerField(null=True, blank=True)
    ultima_regla = models.DateTimeField(null=True, blank=True)
    anticonceptivos = models.CharField(max_length=15, null=True, blank=True)
    menopausia = models.CharField(max_length=2, null=True, blank=True)
    peso = models.FloatField(null=False, blank=False) 
    talla = models.FloatField(null=False, blank=False)  # No se especifica precisión y escala ya que mas adelante sera retirado de SQL
    imc = models.FloatField(null=False, blank=False) 

class Personal(models.Model):
    nombre_empleado = models.CharField(max_length=35, null=False, blank=False)
    horario_laboral_inicio = models.TimeField(null=False, blank=False, default='00:00')#Formato aceptado 09:00 ya que es 24hrs
    horario_laboral_fin = models.TimeField(null=False, blank=False, default='00:00')
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
    nombre_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_cita = models.DateTimeField(null=False, blank=False)
    horario_cita_inicio = models.TimeField(null=False, blank=False, default='00:00') #Formato aceptado 09:00 ya que es 24hrs
    horario_cita_fin = models.TimeField(null=False, blank=False, default='00:00')
    servicio = models.CharField(max_length=25, null=False, blank=False)
    metodo_pago = models.CharField(max_length=15, null=False, blank=False)
    paquete = models.CharField(max_length=2, null=False, blank=False)
    total_sesiones = models.CharField(max_length=2, null=True, blank=True)
    sesiones_tomadas = models.CharField(max_length=2, null=True, blank=True)
    sesiones_faltantes = models.CharField(max_length=2, null=True, blank=True)
    observaciones = models.CharField(max_length=255, null=True, blank=True)
    # ForeignKey para referenciar al personal asignado a la cita
    asignado_a = models.ForeignKey(
        Personal, 
        on_delete=models.SET_DEFAULT,  # Cambiar el comportamiento de eliminación
        default=None,
        null=True, 
        blank=True,  # Permitir valores en blanco
        related_name='citas_asignadas',  # Nombre para la relación inversa
        
    )
    STATUS_CHOICES = [
        ('por_confirmar', 'Por confirmar'),
        ('asistio', 'Asistio'),
        ('cancelada', 'Cancelada'),
        ('reagendada', 'Reagendada')
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='por_confirmar',
    )


