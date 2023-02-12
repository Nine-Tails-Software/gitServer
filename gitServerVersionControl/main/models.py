from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField



class Repository(models.Model):
    name = models.CharField(max_length=300, default='')

    description = models.CharField(max_length=1000, default='', blank=True)
    owner = models.CharField(max_length=1000, default='', blank=True)

    keepNumber = models.IntegerField(default=5)

    fullName = models.CharField(max_length=300, default='', blank=True)

    startCommand = models.CharField(max_length=300, default='', blank=True)

    #Tags eventually

    url = models.URLField(default='', blank=True)
    cTag = models.CharField(max_length=300, default='', blank=True)

    code = models.CharField(max_length=300, default='', blank=True)



    enable = models.BooleanField(default=False)
    running = models.BooleanField(default=False)



    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.code}'''


class GameServer(models.Model):
    name = models.CharField(max_length=300, default='')

    Game = models.CharField(max_length=1000, default='', blank=True)
    description = models.CharField(max_length=1000, default='', blank=True)

    fullName = models.CharField(max_length=300, default='', blank=True)

    startCommand = models.CharField(max_length=300, default='', blank=True)

    #Tags eventually

    downloadURL = models.URLField(default='', blank=True)
    connectionURL = models.CharField(max_length=1000, default='', blank=True)

    code = models.CharField(max_length=300, default='', blank=True)


    enable = models.BooleanField(default=False)
    running = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.code}'''