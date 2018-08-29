from django.contrib import admin
from .models import Probeg, Loko, Filial

# Register your models here.
@admin.register(Probeg)
class ProbegAdmin(admin.ModelAdmin):
    list_display = ['filial', 'loko', 'year', 'km_count']


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Loko)
class LokoAdmin(admin.ModelAdmin):
    list_display = ['seria', 'stavka_za_km']
