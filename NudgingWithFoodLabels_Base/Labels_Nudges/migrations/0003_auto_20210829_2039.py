# Generated by Django 3.2.6 on 2021-08-29 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Labels_Nudges', '0002_auto_20210829_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthyrecipe',
            name='NumberRatings',
            field=models.IntegerField(max_length=200),
        ),
        migrations.AlterField(
            model_name='unhealthyrecipe',
            name='NumberRatings',
            field=models.IntegerField(max_length=200),
        ),
    ]
