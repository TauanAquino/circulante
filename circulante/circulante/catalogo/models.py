# coding: utf-8

from django.db import models

TIPOS_PUBLICACAO = (
    (u'livro', u'Livro'),
    (u'apostila', u'Apostila'),
    (u'gibi', u'Gibi'),
    (u'outro', u'Outro'),
)

class Publicacao(models.Model):

    class Meta:
        verbose_name = u'Publication'
    tipo = models.CharField(max_length=16, choices=TIPOS_PUBLICACAO,
                            default=TIPOS_PUBLICACAO[0][0])
    id_padrao = models.CharField(max_length=32, blank=True)
    titulo = models.CharField(max_length=256)
    num_paginas = models.PositiveIntegerField(default = 0)
    
    def __unicode__(self):
        return self.titulo
    
class Credito(models.Model):
    nome = models.CharField(max_length=256)
    papel = models.CharField(max_length=32, blank = True)
    publicacao = models.ForeignKey(Publicacao)
    
    def __unicode__(self):
        return self.nome
