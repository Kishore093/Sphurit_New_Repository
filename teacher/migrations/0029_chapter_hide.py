# Generated by Django 4.2 on 2023-11-20 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0028_course_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='hide',
            field=models.BooleanField(default=True),
        ),
    ]
