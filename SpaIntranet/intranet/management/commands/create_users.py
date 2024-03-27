# Importamos las clases BaseCommand y CommandError para la creación de comandos personalizados.
# También importamos los modelos User y Group que Django proporciona por defecto para la gestión de usuarios y grupos.
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group

# Definimos una nueva clase Command que hereda de BaseCommand.
# Esta clase será utilizada por Django para ejecutar nuestro comando personalizado.
class Command(BaseCommand):
    # Una breve descripción del comando. Django la muestra cuando ejecutas 'python manage.py help'
    help = 'Crea usuarios y grupos iniciales y los marca para cambiar su contraseña'
    default_users= ''
    # El método 'handle' es el punto de entrada principal de nuestro comando.
    # Django llama a este método cuando ejecutamos 'python manage.py create_initial_users'.
    def handle(self, *args, **options):
        # Definimos los nombres de los grupos que queremos crear.
        group_names = ['Usuario básico', 'Administrador', 'Soporte']
        groups = {}

        # Creamos los grupos si no existen y los almacenamos en un diccionario para su uso posterior.
        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            groups[group_name] = group
            if created:
                # Si el grupo se creó, se muestra un mensaje de éxito en la consola.
                self.stdout.write(self.style.SUCCESS(f'Grupo creado: {group_name}'))
            else:
                # Si el grupo ya existe, se muestra un mensaje informativo.
                self.stdout.write(f'Grupo ya existente: {group_name}')

        default_users = [
            {
                'username': 'Usuario',
                'password': 'ZensorialSpa2024*',  
                'group': 'Usuario básico'
            },
            {
                'username': 'Admin',
                'password': 'ZensorialSpa2024*',  
                'group': 'Administrador'
            },
            {
                'username': 'Master',
                'password': 'ZensorialSpa2024*',  
                'group': 'Soporte'
            },
        ]


        # Creamos cada usuario y los asignamos a sus respectivos grupos.
        for user_data in default_users:
            user, created = User.objects.get_or_create(username=user_data['username'])
            if created:
                # Si se creó el usuario, establecemos la contraseña y lo guardamos
                # Establecemos la contraseña. Esto la encriptará automáticamente antes de guardarla.
                user.set_password(user_data['password'])
                # Añadimos el usuario al grupo correspondiente.
                user.groups.add(groups[user_data['group']])
                # Guardamos el usuario con la nueva contraseña y grupo.
                user.is_active = True
                user.save()
                # Informamos al usuario que el usuario se ha creado correctamente.
                self.stdout.write(self.style.SUCCESS(f'Usuario creado: {user.username}'))
            else:
                # Si el usuario ya existe, se muestra un mensaje informativo.
                # No se modifica la contraseña para no sobrescribir contraseñas de usuarios existentes.
                self.stdout.write(f'Usuario ya existente: {user.username}')

