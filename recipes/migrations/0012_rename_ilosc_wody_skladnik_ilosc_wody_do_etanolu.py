# Generated by Django 3.2.5 on 2022-02-07 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20220206_1535'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skladnik',
            old_name='ilosc_wody',
            new_name='ilosc_wody_do_etanolu',
        ),
    ]
