# Generated by Django 4.0.1 on 2022-01-15 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Receptura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('rodzaj', models.TextField(blank=True, choices=[('1', 'Maść'), ('2', 'czopki i globulki'), ('3', 'receptura płynna')], null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skladnik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skladnik', models.CharField(max_length=40)),
                ('receptura_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.receptura')),
            ],
        ),
    ]