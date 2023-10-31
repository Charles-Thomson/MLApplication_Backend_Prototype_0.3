# from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from database.models import BrainInstanceModel
from database.data_modeling.brain_instance_modeling import (
    brain_instance_to_model,
    brain_model_to_instance,
)

from application.lib.agent_brain.brain_factory import BrainFactory

from database.internal_use_db_functions.learning_instance_functions import (
    new_learning_instance_model,
)

from database.internal_use_db_functions.generation_instance_functions import (
    new_generation_instance_model,
)

from application.lib.instance_generation.config_formatting import format_brain_config
from application.lib.agent_brain.brain_factory import new_random_weighted_brain


def index(request):
    """
    Basic landing page for index
    """
    return HttpResponse("Hello, world. You're at the database index.")


test_brain_config: dict = {
    "weight_init_huristic": "he_weight",
    "hidden_activation_func": "linear_activation_function",
    "output_activation_func": "argmax_activation",
    "new_generation_func": "crossover_weights_average",
    "input_to_hidden_connections": "[24,9]",
    "hidden_to_output_connections": "[9,9]",
}
foramtted_test_config = format_brain_config(brain_config=test_brain_config)


# Currently being used as a test func
# @require_http_methods(["POST"])
def save_brain_instance(request):
    """Add a new Brain Instance"""

    instance_id = "test_instance"
    learning_instance_db_referance = new_learning_instance_model(instance_id)

    current_generation_number_1 = 1
    generation_instance_id_1 = f"L:{instance_id}-G:{current_generation_number_1}"

    test_generation_model_ref: json = new_generation_instance_model(
        generation_instance_id=generation_instance_id_1,
        generation_number=current_generation_number_1,
        learning_instance_referance=learning_instance_db_referance,
        parents_of_generation=[],
    )

    brain_instance = new_random_weighted_brain(
        brain_config=foramtted_test_config, brain_id="test_brain", parents=[]
    )

    est_brain = BrainFactory.make_brain(
        brain_id="test_brain_id",
        brain_type="random_weighted_brain",
        brain_config=foramtted_test_config,
    )

    brain_instance_as_model = brain_instance_to_model(
        brain_instance, test_generation_model_ref
    )

    brain_instance_as_model.save()
    return HttpResponse("Item should be added to the DB")


def add_generation(reauest):
    """
    Add a new generation model to the DB
    """

    new_generation_model = gernation_to_model()


# @require_http_methods(["GET"])
# def get_brain_instance(request, brain_id) -> None:
#     """Get a brain Instance back from the model"""

#     brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(id=brain_id)

#     rtn_brain_instance = brain_model_to_instance(brain_model)

#     # print(rtn_brain_instance)

#     return HttpResponse(f"Returned: {rtn_brain_instance} from the database")
