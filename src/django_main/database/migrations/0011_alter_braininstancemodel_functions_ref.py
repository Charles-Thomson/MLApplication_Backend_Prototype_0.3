# Generated by Django 4.1.7 on 2023-10-16 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("database", "0010_remove_braininstancemodel_hidden_weights_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="braininstancemodel",
            name="functions_ref",
            field=models.CharField(default=dict, max_length=350),
        ),
    ]
