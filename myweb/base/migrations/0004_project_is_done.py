# Generated by Django 5.0.6 on 2024-06-08 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_task_created_at_task_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
