# Generated by Django 3.1.3 on 2020-12-07 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0002_place_game'),
        ('player', '0005_session_happened'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='place',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='place.place'),
            preserve_default=False,
        ),
    ]