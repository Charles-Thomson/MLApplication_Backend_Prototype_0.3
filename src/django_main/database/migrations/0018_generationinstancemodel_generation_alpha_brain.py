# Generated by Django 4.1.7 on 2023-10-19 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "database",
            "0017_rename_instance_id_learninginstancemodel_learning_instance_id",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="generationinstancemodel",
            name="generation_alpha_brain",
            field=models.JSONField(default=dict),
        ),
    ]
