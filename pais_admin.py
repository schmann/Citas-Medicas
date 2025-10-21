from django.contrib import admin
from .models import Pais

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('Pais', 'Codigo', 'iso3166a1', 'iso3166a2')
    search_fields = ('Pais', 'iso3166a1', 'iso3166a2')
    ordering = ('Pais',)
