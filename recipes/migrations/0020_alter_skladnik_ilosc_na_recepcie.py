# Generated by Django 3.2.5 on 2022-02-27 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0019_auto_20220227_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skladnik',
            name='ilosc_na_recepcie',
            field=models.CharField(blank=True, default='0', max_length=40, null=True),
        ),
    ]
