# Generated by Django 3.2.5 on 2022-01-16 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_skladnik_aa_skladnik_aa_ad_skladnik_aa_ad_gramy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skladnik',
            name='jednostka_z_recepty',
            field=models.CharField(blank=True, default='gramy', max_length=40, null=True),
        ),
    ]