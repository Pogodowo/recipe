# Generated by Django 3.2.5 on 2022-03-19 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0030_alter_receptura_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receptura',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
