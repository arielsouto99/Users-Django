from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    #! Proceso para crear el super usuario (privado)
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = is_active,
            **extra_fields # CAMPOS EXTRAS A AGREGAR CUANDO QUERAMOS
        )
        # Encriptando password
        user.set_password(password)
        user.save(using=self.db)
        return user

    #! Creando users normales
    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, False, **extra_fields)
    

    #! Creando superuser
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, True, **extra_fields)


    #! Validacion de codigo
    def cod_validation(self, id_user, cod_registro):
        
        if self.filter(id=id_user, codregistro=cod_registro).exists():
            return True
        else:
            return False