# Generated by Django 4.2 on 2023-12-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0037_remove_course_views_hitcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='progress',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='progress',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='progress',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
