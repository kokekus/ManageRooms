# Generated by Django 2.2.6 on 2022-04-17 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roominfo',
            old_name='room_capacity',
            new_name='capacity',
        ),
        migrations.RenameField(
            model_name='roominfo',
            old_name='room_name',
            new_name='name',
        ),
    ]