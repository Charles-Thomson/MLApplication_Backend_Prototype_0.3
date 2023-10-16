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


# TODO: Test if the functins can be passed in assigned as a function over a model field
@DatabaseModelsFactory.register("general")
class BrainInstanceModel(models.Model):
    """Model for the Brain Instances"""

    brain_type = models.CharField(max_length=100, default="trained")
    brain_id = models.CharField(max_length=350)
    current_generation_number = models.CharField(max_length=350)
    fitness = models.CharField(max_length=350)
    traversed_path = models.CharField(max_length=350, default="[]")
    fitness_by_step = models.CharField(max_length=350, default="[]")
    weights = models.JSONField(default=dict)
    functions_ref = models.JSONField(default=dict)
    functions_callable = models.JSONField(default=dict)

    # svg_path = models.CharField(max_length=350, default="")
    # svg_start = models.CharField(max_length=350, default="")
    # svg_end = models.CharField(max_length=350, default="")
