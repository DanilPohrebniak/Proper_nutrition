# Generated by Django 5.0.4 on 2024-04-29 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pn', '0003_purchases_foods_in_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pn.unit'),
        ),
    ]
