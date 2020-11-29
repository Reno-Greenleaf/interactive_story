# Generated by Django 3.1.3 on 2020-11-29 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0002_place_game'),
        ('game', '0002_game_starting_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='starting_place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games', to='place.place'),
        ),
    ]
