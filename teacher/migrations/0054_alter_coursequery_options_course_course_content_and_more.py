# Generated by Django 4.2 on 2024-01-31 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0053_alter_topic_options_topic_topic_video_thumbnail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursequery',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='course',
            name='course_content',
            field=models.FileField(blank=True, null=True, upload_to='course_content'),
        ),
        migrations.AddField(
            model_name='course',
            name='setup_file',
            field=models.FileField(blank=True, null=True, upload_to='course_setup'),
        ),
    ]
