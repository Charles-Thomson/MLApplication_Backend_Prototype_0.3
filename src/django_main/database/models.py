"""The Model for the DB"""
from django.db import models


class DatabaseModelsFactory:
    """Factory for DB models"""

    available_models: dict = {}

    @classmethod
    def get_model(cls, model_type: str):
        """Get the desired model"""
        try:
            retrival = cls.available_models[model_type]
        except KeyError as err:
            raise NotImplementedError(
                f"MODEL FACTORY - {model_type} is not implemented"
            ) from err
        return retrival

    @classmethod
    def register(cls, model_name):
        """Deco to register each model"""

        def deco(deco_cls):
            cls.available_models[model_name] = deco_cls
            return deco_cls

        return deco


@DatabaseModelsFactory.register("brain_instance_model")
class BrainInstanceModel(models.Model):
    """Model for the Brain Instances"""

    brain_type = models.CharField(max_length=100, default="trained")
    brain_id = models.CharField(max_length=350)
    current_generation_number = models.CharField(max_length=350)
    fitness = models.CharField(max_length=350)
    traversed_path = models.JSONField(default=dict)
    fitness_by_step = models.JSONField(default=dict)
    weights = models.JSONField(default=dict)
    functions_callable = models.JSONField(default=dict)

    # svg_path = models.CharField(max_length=350, default="")
    # svg_start = models.CharField(max_length=350, default="")
    # svg_end = models.CharField(max_length=350, default="")


@DatabaseModelsFactory.register("generation_storage_model")
class GenerationInstanceModel(models.Model):
    """
    A model to store a full generation of BrainInstances
    In the current version this strones a set of parents - i.e the "fit" instances
    from a previous generation
    """

    generation_id = models.CharField(max_length=350)
    generation_number = models.CharField(max_length=350)
    average_fitness = models.CharField(max_length=350)
    fitness_threshold = models.CharField(max_length=350)
    generation_brain_instances = models.JSONField(default=dict)
