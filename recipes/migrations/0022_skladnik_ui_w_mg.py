# Generated by Django 3.2.5 on 2022-03-02 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0021_skladnik_solutio'),
    ]

    operations = [
        migrations.AddField(
            model_name='skladnik',
            name='UI_w_mg',
            field=models.CharField(default='0', max_length=40),
        ),
    ]
