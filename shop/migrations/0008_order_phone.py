# Generated by Django 3.2.7 on 2021-12-22 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_order_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.IntegerField(default=91, max_length=12),
            preserve_default=False,
        ),
    ]
