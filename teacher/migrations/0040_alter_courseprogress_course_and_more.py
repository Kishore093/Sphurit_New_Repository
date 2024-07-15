# Generated by Django 4.2 on 2023-12-18 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teacher', '0039_remove_chapter_progress_remove_course_progress_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseprogress',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course_progress', to='teacher.course'),
        ),
        migrations.AlterField(
            model_name='courseprogress',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_course_progress', to=settings.AUTH_USER_MODEL),
        ),
    ]
