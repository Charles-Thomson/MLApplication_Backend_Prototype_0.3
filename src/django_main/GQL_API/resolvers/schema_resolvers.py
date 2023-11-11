"""Resolvers for the GQL API requests"""
import json
import graphene
from graphene import String
from graphene.types.generic import GenericScalar

from application.lib.config_generation.config_file_structure import (
    generate_test_input_config_as_json,
    generate_full_run_test_input_config_as_json,
)
from application.lib.instance_generation.instance_generation_main import new_instance

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


class Query(graphene.ObjectType):
    """
    GQL Base Query
    """

    # for testing
    dummy_run = String(dummy_id=String())

    # New instance
    new_instance = GenericScalar(input_config=String(default_value="no_config_given"))

    # Get model by referance
    get_learning_instance_by_id = String(
        learning_instance_id=String(default_value="no_id_given")
    )
    get_generation_instance_by_learning_ref = String(
        learning_instance_ref=String(default_value="no_ref_given")
    )
    get_brain_instances_by_generaition_ref = String(
        generation_instance_ref=String(default_value="no_ref_given")
    )

    # Get all model data by model
    get_all_learning_instances = graphene.List(LearningInstanceSchema)
    get_all_generation_instances = graphene.List(GenerationInstanceSchema)
    get_all_brain_instances = graphene.List(BrainInstanceSchema)

    # For testing
    def resolve_dummy_run(self, info, dummy_id: str):
        """
        Run the system with dummy json
        """
        print("in dummy run resolver")
        dummy_json_input = generate_full_run_test_input_config_as_json(
            test_instance_id=dummy_id
        )

        instance = new_instance(input_config=dummy_json_input)

        print(instance.instance_id)

        instance.run_instance()

        return instance.instance_id

    def resolve_new_instance(self, info, input_config: json):
        """
        Resolver - Generate and run a new leaning instance based on the input_config configuration
        var: input_config - Configuration for the new insatnce
        """

        instance = new_instance(input_config=input_config)

        instance.run_instance()

        return instance.instance_id + "complete"

    def resolver_get_learning_instance_by_id(self, info, learning_instance_id: str):
        """
        Resolver - Get the learning instance with the given learning_instance_id
        var: learning_instance_id - ID of a learning insatnce
        """

        return LearningInstanceModel.objects.get(
            learning_instance_id=learning_instance_id
        )

    def resolve_get_generation_instance_by_learning_ref(
        self, info, learning_instance_ref: str
    ):
        """
        Resolver - get all generatio instances related to a given learning instance
        var: learning_instance_ref - A learning instance referance
        """

        learning_instance_model = LearningInstanceModel.objects.get(
            learning_instance_id=learning_instance_ref
        )
        return learning_instance_model.fk_ref.all()

    def resolve_get_brain_instances_by_generaition_ref(
        self, info, generation_instance_ref: str
    ):
        """
        Resolver - get all brain instances related to a given generation
        var: generation_instance_ref - A generation instance referance
        """

        generation_instance_model = GenerationInstanceModel.objects.get(
            generation_instance_id=generation_instance_ref
        )

        return generation_instance_model.fk_ref.all()

    def resolve_get_all_learning_instance(self, info):
        """
        Resolver - get all learning instances
        """
        return LearningInstanceModel.objects.all()

    def resolve_get_all_generation_instance(self, info):
        """
        Resolver - get all generation instances
        """
        return GenerationInstanceModel.objects.all()

    def resolve_get_all_brain_instance(self, info):
        """
        Resolver - get all brain instances
        """
        return BrainInstanceModel.objects.all()


schema = graphene.Schema(query=Query)
