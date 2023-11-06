import graphene
from graphene_django import DjangoObjectType
from .models import Restaurant

from database.models import (
    BrainInstanceModel,
    LearningInstanceModel,
    GenerationInstanceModel,
)

# class BrainInstanceModelType(DjangoObjectType):
#     class Meta:
#         model = BrainInstanceModel
#         fields = ("brain_id")

# class BrainInstanceQuery(graphene.ObjectType):
#     """
#     Quieries for the brain instance model
#     """

#     brains = graphene.List(BrainInstanceModelType)

#     def resolve_restaurants(self, info, func=test, **kwargs):
#         print(info)

#         func()
#         payload = Restaurant.objects.all()
#         return payload


# schema = graphene.Schema(query=BrainInstanceQuery)
from graphene import ObjectType, String, Schema
import json


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


class Query(graphene.ObjectType):
    """
    Query for the learning instance model
    """

    learning_instance = graphene.List(LearningInstanceSchema)
    generation_instance = graphene.List(GenerationInstanceSchema)
    brain_instance = graphene.List(BrainInstanceSchema)

    learning_instance_by_id = String(instance_id=String(default_value="default"))
    generaiton_instance_by_fk = String(instance_id_ref=String(default_value="default"))
    brain_instance_by_fk = String(
        generation_instance_ref=String(default_value="default")
    )

    # leraning instance ref "learning_ID_test"
    # generation ref "generation_ID_test"
    def resolve_learning_instance_by_id(self, info, instance_id: str):
        """
        Resolver for the learning_instance path
        """
        payload = LearningInstanceModel.objects.get(learning_instance_id=instance_id)

        return payload

    def resolve_generaiton_instance_by_fk(self, info, instance_id_ref: str):
        """
        Resolver for getting generation instances based on the learnin instance ref - fk
        """
        learning_instance_model = LearningInstanceModel.objects.get(
            learning_instance_id=instance_id_ref
        )
        generation_objects = learning_instance_model.fk_ref.all()

        return generation_objects

    def resolve_brain_instance_by_fk(self, info, generation_instance_ref: str):
        """
        Resolver for getting brain instance by the generaiton instance referance - fk
        """
        generation_instance_model = GenerationInstanceModel.objects.get(
            generation_instance_id=generation_instance_ref
        )
        brain_objects = generation_instance_model.fk_ref.all()

        return brain_objects

    # to start test getting all the leanring insaces
    # Teh move into getting by ID
    def resolve_learning_instance(self, info):
        """
        Resolver for the learning_instance path
        """
        payload = LearningInstanceModel.objects.all()
        return payload

    def resolve_generation_instance(self, info):
        """
        Resolver for the generation_instance path
        """
        payload = GenerationInstanceModel.objects.all()
        return payload

    def resolve_brain_instance(self, info):
        """
        Resolver for the brain_instance path
        """
        payload = BrainInstanceModel.objects.all()
        return payload


# class RestaurantType(DjangoObjectType):
#     class Meta:
#         model = Restaurant
#         fields = ("id", "name", "address")
#         print("test")


# class Query(graphene.ObjectType):
#     """
#     Queries for the Restaurant model
#     """

#     restaurants = graphene.List(RestaurantType)
#     hello = String(first_name=String(default_value="default"))
#     json_test = graphene.JSONString(
#         name=String(default_value="default"),
#         second_name=String(default_value="default"),
#     )

#     def resolve_hello(self, info, first_name: str):
#         return first_name

#     def resolve_json_test(self, info, name: str, second_name):
#         return str(name), second_name

#     def resolve_restaurants(self, info, **kwargs):
#         payload = Restaurant.objects.all()
#         return payload


schema = graphene.Schema(query=Query)
