# Generated by Django 3.2.5 on 2022-01-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_skladnik_jednostka_z_recepty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skladnik',
            name='ilosc_na_recepcie',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
    ]
