# Generated by Django 3.2.5 on 2022-01-29 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_skladnik_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='skladnik',
            name='dodaj_wode',
            field=models.CharField(default='off', max_length=20),
        ),
    ]