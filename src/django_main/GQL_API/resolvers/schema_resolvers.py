"""Resolvers for the GQL API requests"""
import json
import graphene
from graphene_django import DjangoObjectType

from database.models import (
    BrainInstanceModel,
    LearningInstanceModel,
    GenerationInstanceModel,
)

from GQL_API.schema.model_schema import (
    LearningInstanceSchema,
    GenerationInstanceSchema,
    BrainInstanceSchema,
)

from graphene import JSONString, String
from graphene.types.generic import GenericScalar


class Query(graphene.ObjectType):
    """
    Query for the resolvers
    """

    learning_instance = graphene.List(LearningInstanceSchema)
    generation_instance = graphene.List(GenerationInstanceSchema)
    brain_instance = graphene.List(BrainInstanceSchema)

    learning_instance_by_id = String(instance_id=String(default_value="default"))
    generaiton_instance_by_fk = String(instance_id_ref=String(default_value="default"))
    brain_instance_by_fk = String(
        generation_instance_ref=String(default_value="default")
    )

    input_config_json = String(input_config=String(default_value="no_data"))

    input_json_test = GenericScalar(input_json=String(default_value="no_data"))

    # inputJsonTest(jsonInput: "{\"name\": \"Jane\"}") working format
    def resolve_input_json_test(self, info, input_json):
        """
        Testing the usage of json
        """
        print(input_json)
        print(type(input_json))
        as_dict = json.loads(input_json)
        print(as_dict)
        print(type(as_dict))

        return input_json

    def resolve_input_config_json(self, info, input_config: str):
        """
        Resolver for th input config
        var: input_config - the input config in json format
        """
        print(input_config)
        print(type(input_config))
        return input_config

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


schema = graphene.Schema(query=Query)
