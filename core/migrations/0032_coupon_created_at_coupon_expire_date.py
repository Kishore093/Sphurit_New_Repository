# Generated by Django 4.2 on 2023-12-16 12:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_cart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coupon',
            name='expire_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
