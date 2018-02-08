from django.db import models


class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=64)
    token = models.CharField(max_length=64,null=True,blank=True)

    group = models.ForeignKey(to="Group")
    roles = models.ManyToManyField(to="Roles")

class Menu(models.Model):
    name = models.CharField(max_length=32)

class Group(models.Model):
    title = models.CharField(max_length=32)
    menu = models.ForeignKey(to="Menu")

class Roles(models.Model):
    name = models.CharField(max_length=32)
