from django.db import models


class UsersRoleChoices(models.TextChoices):
    ADMIN = ('admin', 'Admin')
    CLIENT = ('client', 'Client')
    DRIVER = ('driver', 'Driver')
