#coding:utf-8

from django.contrib import admin
from .models import Publicacao, Credito

class CreditoInline(admin.TabularInline):
    model = Credito
    extra = 1

class PublicacaoAdmin(admin.ModelAdmin):
    inlines = [CreditoInline]

admin.site.register(Publicacao, PublicacaoAdmin)

