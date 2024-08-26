# Generated by Django 5.1 on 2024-08-26 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.basket'),
        ),
        migrations.AddField(
            model_name='basket',
            name='basket_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop_item'),
        ),
    ]
