**CARPETA SETTINGS**
- En base.py a lo que se llama INSTALLED_APPS lo vamos a cambiar por DJANGO_APPS
- Creamos LOCAL_APPS = () aplicaciones locales
- Creamos THIRS_PARTY_APPS = () aplicaciones de terceros
- Creamos INSTALLED APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
- Esto nos permite tener un mayor control y organizacion de las carpetas
- El secret key copiar el de la app nueva

**ARCHIVO SECRET, PARA ESCONDER INFORMACION SENSIBLE DEL PROYECTO**
- A la altura del manage.py crear secret.json
- Este secret.json va a contener tanto el nombre de la db, el usuario, contrasena, secret_key, etc
- Nunca hacer publico este archivo
- Para esconder el secret_key nos vamos a base.py e importamos lo siguiente:
    - from django.core.exceptions import ImproperlyConfigured
    - import json
- Copiar este codigo para todos los proyectos, en este caso escondemos el secret_key (base.py):

with open("secret.json") as f:
secret = json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "La variable %s no existe." % secret_name
        raise ImproperlyConfigured(msg)

SECRET_KEY = get_secret('SECRET_KEY') 

- Copiar este codigo para todos los proyectos, en este caso escondemos los valores de la db:
    - En el local.py donde esta el NAME, al igual que el SECRET_KEY lo reemplazamos con el nombre de la funcion, esto se debe
    a que importamos todo desde el base.py
    - Asi deberia quedar en el local.py:
        - 'NAME': get_secret('DB_NAME'),
        - 'USER': get_secret('USER'),
        - 'PASSWORD': get_secret('PASSWORD'),
- Una vez hecho esto podemos borrar el settings.py (archivo que trae el proyecto)
- Creamos archivo .gitignore y dentro ponemos la ruta de nuestro secret.json ---> users/secret.json
 
**ABTRACT BASE USER**
- Importarlo ---> from django.contrib.auth.models import AbstractBaseUser
- Una vez generado el model hay que agregarlo en local apps y crear en base.py un AUTH_USER_MODEL que va a permitir trabajar con otro
modelo de usuario cuando se trate de usuarios y especificamos donde esta el modelo
- AUTH_USER_MODEL = 'users.User'  #App y modelo
- Recordar en apps.py cambiar el name a applications.users
- En models.py agregar debajo USERNAME_FIELD = 'username' esto nos permite elegir con que atributo vamos a hacer el login desde el administrador
- Nos faltan los managers.py para poder crear el superusuario
- Dentro del manager importar los models y from django.contrib.auth.models import BaseUserManager
- Mirar models.py y managers.py

**PASSWORD**
- Jamas guardarla como un dato plano
- Para eso en nuestro forms.py hay que agregar un campo extra que indique que tienen que agregar una contrasena
- Recoger datos y registrarlos
- Validar passwords:
    - def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no coinciden.')

**Authenticate (Login)** 
- Permite verificar si esta el usuario y contrasena o lo que queramos recuperar autenticado
- from django.contrib.auth import authenticate
-  user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )

**Login (trabaja con usuario autenticado nomas)**
- from django.contrib.auth import login
- Una vez autenticado hay que logearse 
- login(self.request, user)
- Tan simple como eso, el user es la variable que autenticamos
# Validacion de login
- En forms.py importar el authenticate:  from django.contrib.auth import authenticate
-  def clean(self): # Django detecta que debe ser una de las primeras validaciones que debe aplicar
        cleaned_data = super(LoginForm, self). clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos.')

        return self.cleaned_data

**Logout**
- from django.urls import reverse
- from django.contrib.auth import logout
- from django.http import HttpResponseRedirect
- from django.views.generic import View
- class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('users_app:user-login'))
    

**Mixins**
- Reutilizar codigo, similar a la herencia.
- Los construimos nosotros y algunos los trae Django
- Por orden jerarquico siempre van arriba de las views
# Login required mixin
- from django.contrib.auth.mixins import LoginRequiredMixin
- Necesita de una propiedad o atributo que permita solucionar que va a suceder cuando intenten entrar a la vista que esta bloqueada por no estar logueado --> login_url = reverse_lazy('users_app:user-login')


**Current user**
- Se crea una variable:
    - usuario = self.request.user
- Cuando queramos mostrar, simplemente invocamos a la variable usuario


**Envio de mails (Verificacion)**
- En models agregar un campo para el codigo y un is_active que tiene que ser booleano y default=False
- Creamos un functions.py donde vamos a almacenar todas las funciones extras de la app
- import random
- import string
- Una vez importados los paquetes creamos la funcion
- def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
- size = Es el tamanio que quiero que tenga mi codigo
- chars = string plano(ascii) y en letras mayusculas(upercase) y que contenga tambien digitos(numeros)
- Traemos la funcion a las vistas
- Incluimos el codigo dentro del form_valid 'codigo = code_generator()'
- Y lo agregamos dentro del create_user 'codregistro = codigo'
- Enviamos mail:
    - Importamos --> from django.core.mail import send_mail
    - Creamos variables para que se entienda correctamente la forma de envio
    - asunto = 'Confirmación de email'
    - mensaje = 'Código de verificación: ' + codigo
    - email_remitente = 'devsoutoariel0@gmail.com' #Quien envia el mail (mails corporativos)
    - send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],]) #Siempre poner una lista para enviar a multiples correos
- Las autorizaciones se hacen en el archivo local.py:
    - EMAIL_USE_TLS = True --> Activar el envio de email
    - EMAIL_HOST = 'smtp.gmail.com' --> Tipo de correo
    - EMAIL_HOST_USER = get_secret('EMAIL'), --> Usuario gmail
    - EMAIL_HOST_PASSWORD = get_secret('PASS_EMAIL'),--> contrasena de usuario gmail
    - EMAIL_PORT = 587 --> Temas de deploy

**Codigo de verificacion**
- Mediante url pasarle el parametro pk que va a ser el id del usuario
