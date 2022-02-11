from django import forms
from django.contrib.auth import authenticate

from .models import User

class UserRegisterForm(forms.ModelForm): # Dependiendo de un modelo
    
    password1 = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder':'Password'
            }
        )
    )

    password2 = forms.CharField(
        label = 'Repeat Password',
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder':'Repeat Password'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'nombres', 'apellidos', 'genero',)

    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no coinciden.')


class LoginForm(forms.Form): # Sin depender de un modelo
    username = forms.CharField(
        label = 'Username',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'Username'
            }
        )
    )

    password = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder':'Password'
            }
        )
    )

    def clean(self): # Django detecta que debe ser una de las primeras validaciones que debe aplicar
        cleaned_data = super(LoginForm, self). clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos.')

        return self.cleaned_data


class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder':'Current Password'
            }
        )
    )

    password2 = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput(
            attrs = {
                'placeholder':'New Password'
            }
        )
    )


class VerificationForm(forms.Form):
    codregistro = forms.CharField(max_length=50, required=True)

    # Recuperando el pk
    def __init__(self, pk, *args, **kwargs):
        # id_user = pk de la vista y a su vez la vista lo recibe de las urls
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            #Verificamos si el codigo y el id usuario son validos
            activo = User.objects.cod_validation(
               # self.kwargs['pk'], Asi no se puede recuperar el pk en los forms\
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('El codigo es incorrecto.')
        else:
            raise forms.ValidationError('El codigo es incorrecto.')