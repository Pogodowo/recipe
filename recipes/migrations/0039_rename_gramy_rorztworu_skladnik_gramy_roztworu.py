# Generated by Django 3.2.5 on 2022-05-24 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0038_auto_20220524_0755'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skladnik',
            old_name='gramy_rorztworu',
            new_name='gramy_roztworu',
        ),
    ]
