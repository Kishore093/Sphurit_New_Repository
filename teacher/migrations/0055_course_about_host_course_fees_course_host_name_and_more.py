# Generated by Django 4.2 on 2024-02-02 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0054_alter_coursequery_options_course_course_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='about_host',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='fees',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='host_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='profile'),
        ),
        migrations.AddField(
            model_name='course',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
