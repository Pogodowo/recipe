# Generated by Django 3.2.5 on 2022-02-06 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20220206_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='skladnik',
            name='ilosc_etanolu',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='skladnik',
            name='ilosc_wody',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
    ]
