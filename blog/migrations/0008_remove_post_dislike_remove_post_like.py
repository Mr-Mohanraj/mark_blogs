# Generated by Django 4.1.4 on 2023-02-03 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_follower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dislike',
        ),
        migrations.RemoveField(
            model_name='post',
            name='like',
        ),
    ]