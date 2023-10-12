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


# TODO: Test the factory approach of Get model
class BrainInstanceModel(models.Model):
    """Model for the Brain Instances"""

    brain_type = models.CharField(max_length=100, default="trained")
    brain_id = models.CharField(max_length=350)
    current_generation_number = models.CharField(max_length=350)
    fitness = models.CharField(max_length=350)
    hidden_weights = models.BinaryField()
    output_weights = models.BinaryField()
    traversed_path = models.CharField(max_length=350, default="[]")
    fitness_by_step = models.CharField(max_length=350, default="[]")
    functions_ref = models.CharField(max_length=350, default={})

    # svg_path = models.CharField(max_length=350, default="")
    # svg_start = models.CharField(max_length=350, default="")
    # svg_end = models.CharField(max_length=350, default="")


def get_model(model_type: str) -> models.Model:
    """Return a given model -
    Available:
    "general"
    "fit"
    "trained"
    """

    model: dict[str, models.Model] = {
        "general": BrainInstanceModel,
    }
    return model[model_type]
