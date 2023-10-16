from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


from django.http import HttpResponse

from application.lib.agent_brain.static_state_brain import BrainInstance

from database.model_data_formatting import (
    brain_instance_to_model,
    model_to_brain_instance,
    gernation_to_model,
)
from database.models import BrainInstanceModel


# for testing
from application.lib.instance_generation.instance_generation_main import (
    format_ann_config,
)

from application.lib.agent_brain.brain_factory import BrainFactory


def index(request):
    return HttpResponse("Hello, world. You're at the database index.")


# python manage.py makemigrations
# python manage.py makesuperuser
# run tests from top level folder

# test_ann_config: dict = {
#     "weight_init_huristic": "he_weight",
#     "hidden_activation_func": "linear_activation_function",
#     "output_activation_func": "argmax_activation",
#     "new_generation_func": "crossover_weights_average",
#     "input_to_hidden_connections": "[24,9]",
#     "hidden_to_output_connections": "[9,9]",
# }
# foramtted_test_config = format_ann_config(ann_config=test_ann_config)


# Currently using test brains ect
# @require_http_methods(["POST"])
def add_all(request):
    """Add a new Brain Instance"""

    brain_instance_as_model = brain_instance_to_model(
        brain_instance=test_brain, model_type="general"
    )

    brain_instance_as_model.save()
    return HttpResponse("Item should be added to the DB")


def add_generation(reauest):
    """
    Add a new generation model to the DB
    """

    new_generation_model = gernation_to_model()


def get_instance(request) -> None:
    """Get a brain Instance back from the model"""

    brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(id=1)

    rtn_brain_instance = model_to_brain_instance(brain_model)

    # print(rtn_brain_instance)

    return HttpResponse(f"Returned: {rtn_brain_instance} from the database")
