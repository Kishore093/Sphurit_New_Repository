# Generated by Django 4.2 on 2024-02-12 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0058_alter_course_hide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='hide',
            field=models.BooleanField(default=True),
        ),
    ]
