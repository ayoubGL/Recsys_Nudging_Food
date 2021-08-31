# Generated by Django 3.2.6 on 2021-08-31 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Labels_Nudges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthyrecipe',
            name='NumberRatings',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unhealthyrecipe',
            name='NumberRatings',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Recommendations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('recommended_recipes', models.CharField(max_length=500)),
                ('healthiness', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Labels_Nudges.personal_info')),
            ],
        ),
    ]