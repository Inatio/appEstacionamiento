from django.contrib import admin
from .models import Estacionamiento, Comuna, Contacto

class EstacionamientoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "precio", "descripcion", "comuna"]
    list_editable = ["precio"]
    search_fields = ["nombre"]
    list_filter = ["comuna","precio"]
    list_per_page = 5

admin.site.register(Estacionamiento, EstacionamientoAdmin)
admin.site.register(Comuna)
admin.site.register(Contacto)