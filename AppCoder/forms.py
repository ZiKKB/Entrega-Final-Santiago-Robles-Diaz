from django import forms


from .models import Avatar


class AutoFormulario(forms.Form):
    Marca = forms.CharField()
    Modelo = forms.CharField()


class AutoBuscarFormulario(forms.Form):
    Marca = forms.CharField()


class MarcaFormulario(forms.Form):
    Marca = forms.CharField()
    Modelo = forms.CharField()
    Color = forms.CharField()
    profesion = forms.CharField()


#### CLASE 23: registro

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UserModel


class UserCreationFormulario(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ["password1", "password2", "username", "email"]
        help_texts = {k: "" for k in fields}


class UserEditionFormulario(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")

    class Meta:
        model = UserModel
        fields = ["email", "password1", "password2", "first_name", "last_name"]
        help_texts = {k: "" for k in fields}


class UserAvatarFormulario(forms.ModelForm):

    class Meta:
        model = Avatar
        fields = ["imagen"]
