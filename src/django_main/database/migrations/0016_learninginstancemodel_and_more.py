# Generated by Django 4.1.7 on 2023-10-19 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0015_generationinstancemodel_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LearningInstanceModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("instance_id", models.CharField(max_length=350)),
                ("alpha_brain", models.JSONField(default=dict)),
                ("number_of_generations", models.CharField(max_length=350)),
            ],
        ),
        migrations.RenameField(
            model_name="generationinstancemodel",
            old_name="generation_brain_instances",
            new_name="parents_of_generation",
        ),
        migrations.AddField(
            model_name="braininstancemodel",
            name="generation_instance_ref",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="database.generationinstancemodel",
            ),
        ),
        migrations.AlterField(
            model_name="braininstancemodel",
            name="fitness_by_step",
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name="braininstancemodel",
            name="traversed_path",
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name="generationinstancemodel",
            name="learning_instance_ref",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="database.learninginstancemodel",
            ),
        ),
    ]
