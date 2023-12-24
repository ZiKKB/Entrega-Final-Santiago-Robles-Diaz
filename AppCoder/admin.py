from django.contrib import admin

from . import models

# Register your models here.


admin.site.register(models.Marca)
admin.site.register(models.Auto)
admin.site.register(models.Avatar)

admin.site.register(models.Post)
admin.site.register(models.Comentario)
admin.site.register(models.Perfil)

