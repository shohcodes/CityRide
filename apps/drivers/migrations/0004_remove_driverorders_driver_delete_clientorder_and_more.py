# Generated by Django 4.2.6 on 2023-10-31 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0003_driverorders_clientorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driverorders',
            name='driver',
        ),
        migrations.DeleteModel(
            name='ClientOrder',
        ),
        migrations.DeleteModel(
            name='DriverOrders',
        ),
    ]
