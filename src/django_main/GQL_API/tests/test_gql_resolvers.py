from django.test import TestCase
from GQL_API.resolvers.schema_resolvers import Query
import pytest
import graphene
from graphene.test import Client
from database.internal_use_db_functions.learning_instance_functions import (
    new_learning_instance_model,
)

# Create your tests here.


# Need to add the instance to the model first !
@pytest.mark.django_db
def test_gql_get_learning_instance_by_id():
    """
    Test the GraphQL input_json resolver
    """

    schema = graphene.Schema(query=Query)
    client = Client(schema)

    new_learning_instance_model(learning_instance_id="test_1")

    executed = client.execute(
        """
        {learningInstanceById(instanceId: "test_1")}
        """,
    )

    print(executed)


# test = "{\\"env_type\\": \\"Static_State\\",\\"agent_type\\": \\"\\",\\"instance_id\\": \\"this_instance_id\\", \\"map_config\\": {\\"env_map\\": \\"1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1\\",\\"map_dimensions\\": 4,\\"start_location\\": (1, 1),\\"max_step_count\\": 20,},\\"hyper_perameters\\": {\\"max_number_of_genrations\\": 2,\\"max_generation_size\\": 2,\\"fitness_threshold\\": 2.0,\\"new_generation_threshold\\": 2.0,\\"generation_failure_threshold\\": 10,},\\"brain_config\\": {\\"weight_init_huristic\\": \\"he_weight\\",\\"hidden_activation_func\\": \\"linear_activation_function\\",\\"output_activation_func\\": \\"argmax_activation\\",\\"new_generation_func\\": \\"crossover_weights_average\\",\\"input_to_hidden_connections\\": (24, 9),\\"hidden_to_output_connections\\": (9, 9),},}"


@pytest.mark.django_db
def test_hey():
    schema = graphene.Schema(query=Query)
    client = Client(schema=schema)
    executed = client.execute("""{ hey}""", context={"name": "Peter"})
    print(executed)


# (inputJson: "{\\"name\\": \\"Jane\\"}")
