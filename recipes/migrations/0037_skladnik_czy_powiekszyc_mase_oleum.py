# Generated by Django 3.2.5 on 2022-05-23 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0036_alter_skladnik_obey'),
    ]

    operations = [
        migrations.AddField(
            model_name='skladnik',
            name='czy_powiekszyc_mase_oleum',
            field=models.CharField(default='off', max_length=20),
        ),
    ]
