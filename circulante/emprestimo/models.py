#coding: utf-8
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save

from circulante.catalogo.models import Publicacao

class Participator(models.Model):
    user = models.OneToOneField(User)
    ativo = models.BooleanField(default=True)


def create_participator_profile(sender,instance,created, **kwargs):
    if created:
        Participator.objects.create(user=instance)

post_save.connect(create_participator_profile, sender = User)

class Club(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    members = models.ManyToManyField(Participator)

STATUS_OPTIONS = [
    (u'disponivel', u'Disponível'),
    (u'emprestado', u'Emprestado'),
    (u'reservado', u'Reservado'),
    (u'privado', u'Privado'),
]

class Item(models.Model):
    acquisition_date = models.DateField()
    publication = models.ForeignKey(Publicacao)
    owner = models.ForeignKey(Participator)
    status = models.CharField(max_length = 16, choices=STATUS_OPTIONS, default=STATUS_OPTIONS[0][0])
    notes = models.TextField(blank=True)

class Emprestimo(models.Model):
    applicant = models.ForeignKey(Participator)
    publication = models.ForeignKey(Publicacao)
    item = models.ForeignKey(Item, null=True)
    borrow_hour_date = models.DateTimeField(null=True)
    devolution_hour_date = models.DateTimeField(null=True)
    burn_date = models.DateTimeField(null=True)
    notes = models.TextField(blank=True)

