# Generated by Django 3.2.5 on 2022-02-10 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_rename_ilosc_wody_skladnik_ilosc_wody_do_etanolu'),
    ]

    operations = [
        migrations.AddField(
            model_name='receptura',
            name='czopki_czy_globulk',
            field=models.TextField(blank=True, choices=[('1', 'czopki'), ('2', 'globulki')], null=True),
        ),
        migrations.AddField(
            model_name='receptura',
            name='czy_ilosc_oleum_pomnozyc',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='receptura',
            name='ilosc_czop_glob',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='receptura',
            name='masa_docelowa_czop_glob',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
    ]
