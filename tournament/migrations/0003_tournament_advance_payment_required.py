# Generated by Django 5.0.6 on 2024-05-26 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_tournament_passport_required_alter_tournament_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='advance_payment_required',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]