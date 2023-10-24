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


@DatabaseModelsFactory.register("learning_instance_model")
class LearningInstanceModel(models.Model):
    """
    A model to store the data from a learning instace
    """

    learning_instance_id = models.CharField(max_length=350)
    alpha_brain = models.JSONField(default=dict)
    number_of_generations = models.CharField(max_length=350)

    def __str__(self):
        return f"Instance ID: {self.learning_instance_id} - Number of Generations: {self.number_of_generations}"


@DatabaseModelsFactory.register("generation_instance_model")
class GenerationInstanceModel(models.Model):
    """
    A model to store a full generation of BrainInstances
    In the current version this strones a set of parents - i.e the "fit" instances
    from a previous generation
    """

    generation_instance_id = models.CharField(max_length=350)
    generation_number = models.CharField(max_length=350)
    average_fitness = models.CharField(max_length=350)
    fitness_threshold = models.CharField(max_length=350)
    parents_of_generation = models.JSONField(default=dict)
    generation_alpha_brain = models.JSONField(default=dict)
    generation_size = models.CharField(max_length=350, default=0)
    learning_instance_ref = models.ForeignKey(
        LearningInstanceModel,
        on_delete=models.CASCADE,
        default="",
        related_name="fk_ref",
    )

    def __str__(self):
        return f"Generation ID: {self.generation_instance_id} - Generation Number: {self.generation_number}"


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

    generation_instance_ref = models.ForeignKey(
        GenerationInstanceModel,
        on_delete=models.CASCADE,
        default="",
        related_name="fk_ref",
    )

    def __str__(self):
        return f"Brain ID: {self.brain_id} - Generation Number: {self.current_generation_number}"

    # svg_path = models.CharField(max_length=350, default="")
    # svg_start = models.CharField(max_length=350, default="")
    # svg_end = models.CharField(max_length=350, default="")
