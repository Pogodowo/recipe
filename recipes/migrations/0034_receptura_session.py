# Generated by Django 3.2.5 on 2022-04-18 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('recipes', '0033_alter_receptura_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='receptura',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sessions.session'),
        ),
    ]