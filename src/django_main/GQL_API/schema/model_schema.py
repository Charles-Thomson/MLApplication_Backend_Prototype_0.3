"""The schema used in the QGL API"""
from graphene_django import DjangoObjectType

from database.models import (
    BrainInstanceModel,
    LearningInstanceModel,
    GenerationInstanceModel,
)


class LearningInstanceSchema(DjangoObjectType):
    """
    The schema for the learning instance model
    """

    class Meta:
        model = LearningInstanceModel
        fields = ("learning_instance_id", "alpha_brain", "number_of_generations")


class GenerationInstanceSchema(DjangoObjectType):
    """
    The schema for the generation instance model
    """

    class Meta:
        model = GenerationInstanceModel
        fields = (
            "generation_instance_id",
            "generation_number",
            "learning_instance_ref",
        )


class BrainInstanceSchema(DjangoObjectType):
    """
    The schema for the generation instance model
    """

    class Meta:
        model = BrainInstanceModel
        fields = (
            "brain_id",
            "current_generation_number",
            "generation_instance_ref",
        )
