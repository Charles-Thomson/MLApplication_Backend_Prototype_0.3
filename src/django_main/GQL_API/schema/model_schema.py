"""The schema used in the QGL API"""
from graphene_django import DjangoObjectType

from database.models import (
    BrainInstanceModel,
    LearningInstanceModel,
    GenerationInstanceModel,
)


class LearningInstanceSchema(DjangoObjectType):
    """
    Base Learning instance model schema
    """

    class Meta:
        model = LearningInstanceModel
        fields = ("learning_instance_id", "alpha_brain", "number_of_generations")


class GenerationInstanceSchema(DjangoObjectType):
    """
    Base Generation instance model schema
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
    Base Brain instance model schema
    """

    class Meta:
        model = BrainInstanceModel
        fields = (
            "brain_id",
            "current_generation_number",
            "generation_instance_ref",
        )
