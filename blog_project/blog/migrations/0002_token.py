# Generated by Django 4.1.4 on 2023-01-30 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_token', models.CharField(max_length=64)),
                ('reset_token', models.CharField(max_length=64)),
            ],
        ),
    ]
