# Generated by Django 4.2 on 2024-01-23 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0052_alter_course_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='topic',
            name='topic_video_thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='topic_thumbnails'),
        ),
    ]
