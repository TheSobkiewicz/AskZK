# Generated by Django 4.2.13 on 2024-05-17 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='hash',
            field=models.CharField(blank=True, editable=False, max_length=64, unique=True),
        ),
    ]
