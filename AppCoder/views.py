from datetime import date

from django.shortcuts import redirect, render

from datetime import datetime
from . import models
from .models import Curso, Marca, Avatar

from .forms import AutoFormulario, AutoBuscarFormulario, MarcaFormulario, UserAvatarFormulario

from django.contrib.auth.decorators import login_required

def inicio_view(request):
    if request.user.is_authenticated:
        usuario = request.user
        avatar = Avatar.objects.filter(user=usuario).last()
        avatar_url = avatar.imagen.url if avatar is not None else ""
    else:
        avatar_url = ""

    return render(request, "AppCoder/inicio.html", context={"avatar_url": avatar_url})


def autos_buscar_view(request):
    if request.method == "GET":
        form = AutoBuscarFormulario()
        return render(
            request,
            "AppCoder/curso_formulario_busqueda.html",
            context={"form": form}
        )
    else:
        formulario = AutoBuscarFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            cursos_filtrados = []
            for auto in auto.objects.filter(auto=informacion["auto"]):
                cursos_filtrados.append(auto)

            contexto = {"autos": cursos_filtrados}
            return render(request, "AppCoder/autos_list.html", contexto)


def autos_todos_view(request):
    todos_los_cursos = []
    for curso in Curso.objects.all():
        todos_los_cursos.append(curso)

    contexto = {"autos": todos_los_cursos}
    return render(request, "AppCoder/cursos_list.html", contexto)


def autos_view(request):
    if request.method == "GET":
        print("+" * 90) #  Imprimimos esto para ver por consola
        print("+" * 90) #  Imprimimos esto para ver por consola
        form = AutoFormulario()
        return render(
            request,
            "AppCoder/auto_formulario_avanzado.html",
            context={"form": form}
        )
    else:
        formulario = AutoFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            marca = marca(marca=informacion["marca"], modelo=informacion["modelo"])
            marca.save()

        return redirect("AppCoder:inicio")


def profesores_view(xx):
    nombre = "Mariano Manuel"
    apellido = "Barracovich"
    ahora = datetime.now()
    diccionario = {
        'nombre': nombre,
        'apellido': apellido,
        "nacionalidad": "argentino",
        "hora": ahora,
        "ciudades_preferidas": ["Buenos Aires", "Lima", "San Pablo", "Trieste"]
    }  # Para enviar al contexto
    return render(xx, "AppCoder/padre.html", diccionario)


#### CRUD #####
@login_required
def marca_view(request):
    if request.method == "GET":
        return render(
            request,
            "AppCoder/profesor_formulario_avanzado.html",
            {"form": MarcaFormulario()}
        )
    else:
        formulario = MarcaFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            modelo = Marca(
                marca=informacion["marca"],
                modelo=informacion["modelo"],
                color=informacion["color"],
                categoria=informacion["categoria"]
            )
            modelo.save()
        return render(
            request,
            "AppCoder/inicio.html",
        )

@login_required
def marcas_crud_read_view(request):
    marcas = Marca.objects.all()
    return render(request, "AppCoder/marcas_lista.html", {"marcas": marcas})

@login_required
def marcas_crud_delete_view(request, profesor_email):
    profesor_a_eliminar = Marca.objects.filter(email=profesor_email).first()
    profesor_a_eliminar.delete()
    return marcas_crud_read_view(request)

@login_required
def profesores_crud_update_view(request, profesor_email):
    marca = Marca.objects.filter(email=profesor_email).first()
    if request.method == "GET":
        formulario = MarcaFormulario(
            initial={
                "marca": marca.marca,
                "modelo": marca.modelo,
                "color": marca.color,
                "categoria": marca.categoria,
            }
        )
        return render(request, "AppCoder/marcas_formulario_edicion.html", {"form": formulario, "marca": marca})
    else:
        formulario = MarcaFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            marca.marca=informacion["marca"]
            marca.modelo=informacion["modelo"]
            marca.color=informacion["color"]
            marca.categoria=informacion["categoria"]
            marca.save()
        return marcas_crud_read_view(request)

####################  ClassBasedViews (CBV)  - Vistas basadas en Clases #########################################
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class CursoListView(LoginRequiredMixin, ListView):
    model = Curso
    context_object_name = "cursos"
    template_name = "AppCoder/cbv_curso_list.html"


class CursoDetail(LoginRequiredMixin, DetailView):
    model = Curso
    template_name = "AppCoder/cbv_curso_detail.html"


class CursoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Curso
    template_name = "AppCoder/cbv_curso_create.html"
    success_url = reverse_lazy("AppCoder:curso-list")
    fields = ["curso", "camada"]
    success_message = "Curso creado con éxito!" 

class CursoUpdateView(LoginRequiredMixin, UpdateView):
    model = Curso
    template_name = "AppCoder/cbv_curso_update.html"
    success_url = reverse_lazy("AppCoder:curso-list")
    fields = ["curso"]

class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = "AppCoder/cbv_curso_delete.html"
    success_url = reverse_lazy("AppCoder:curso-list")



#################### CLASE 23:  Login / Logout #########################################
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

def login_view(request):

    if request.user.is_authenticated:
        return render(
            request,
            "AppCoder/inicio.html",
            {"mensaje": f"Ya estás autenticado: {request.user.username}"}
        )

    if request.method == "GET":
        return render(
            request,
            "AppCoder/login.html",
            {"form": AuthenticationForm()}
        )
    else:
        formulario = AuthenticationForm(request, data=request.POST)

        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            password = informacion["password"]

            modelo = authenticate(username=usuario, password=password)
            login(request, modelo)

            return render(
                request,
                "AppCoder/inicio.html",
                {"mensaje": f"Bienvenido {modelo.username}"}
            )
        else:
            return render(
                request,
                "AppCoder/login.html",
                {"form": formulario}
            )



def logout_view(request):
    pass


from .forms import UserCreationFormulario, UserEditionFormulario
from django.contrib.auth.views import PasswordChangeView


def registro_view(request):

    if request.method == "GET":
        return render(
            request,
            "AppCoder/registro.html",
            {"form": UserCreationFormulario()}
        )
    else:
        formulario = UserCreationFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            usuario = informacion["username"]
            formulario.save()

            return render(
                request,
                "AppCoder/inicio.html",
                {"mensaje": f"Usuario creado: {usuario}"}
            )
        else:
            return render(
                request,
                "AppCoder/registro.html",
                {"form": formulario}
            )

#################### CLASE 24:  Editar perfil #########################################

@login_required
def editar_perfil_view(request):

    usuario = request.user
    avatar = Avatar.objects.filter(user=usuario).last()
    avatar_url = avatar.imagen.url if avatar is not None else ""


    if request.method == "GET":


        valores_iniciales = {
            "email": usuario.email,
            "first_name": usuario.first_name,
            "last_name": usuario.last_name
        }


        formulario = UserEditionFormulario(initial=valores_iniciales)
        return render(
            request,
            "AppCoder/editar_perfil.html",
            context={"form": formulario, "usuario": usuario, "avatar_url": avatar_url}
            )
    else:
        formulario = UserEditionFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data

            usuario.email = informacion["email"]

            usuario.set_password(informacion["password1"])

            usuario.first_name = informacion["first_name"]
            usuario.last_name = informacion["last_name"]
            usuario.save()
        return redirect("AppCoder:inicio")


@login_required
def crear_avatar_view(request):

    usuario = request.user

    if request.method == "GET":
        formulario = UserAvatarFormulario()
        return render(
            request,
            "AppCoder/crear_avatar.html",
            context={"form": formulario, "usuario": usuario}
        )
    else:
        formulario = UserAvatarFormulario(request.POST, request.FILES)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            modelo = Avatar(user=usuario, imagen=informacion["imagen"])
            modelo.save()
            return redirect("AppCoder:inicio")

#################### CLASE 25:  INSTRAGRAM #########################################

from django.contrib.auth.models import User
from .models import Post, Perfil

def mostrar_profile_view(request, user_id):
    user = User.objects.get(id=user_id)
    todos_los_posts = Post.objects.filter(autor=user).all()
    perfil = Perfil.objects.filter(usuario=user).first()
    avatar = Avatar.objects.filter(user=user).first()
    avatar_url = avatar.imagen.url if avatar is not None else ""
    contexto = {"posts": todos_los_posts, "perfil": perfil, "avatar_url": avatar_url}

    return render(request, "AppCoder/instagram_profile.html", context=contexto)