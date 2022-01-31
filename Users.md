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
 