# Generated by Django 3.2.5 on 2022-01-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_skladnik_ilosc_na_recepcie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skladnik',
            name='ilosc_na_recepcie',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='skladnik',
            name='jednostka_z_recepty',
            field=models.CharField(blank=True, default='gramy', max_length=40),
        ),
    ]
