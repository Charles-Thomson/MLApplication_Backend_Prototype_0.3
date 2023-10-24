# from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from database.models import BrainInstanceModel

# from database.data_modeling.brain_instance_modeling import (
#     brain_instance_to_model,
#     brain_model_to_instance,
# )
# from database.data_modeling.generation_instance_modeling import (
#     generation_instance_to_model,
#     generation_model_to_instance,
# )


def index(request):
    """
    Basic landing page for index
    """
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
def add_brain_instance(request):
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


@require_http_methods(["GET"])
def get_brain_instance(request, brain_id) -> None:
    """Get a brain Instance back from the model"""

    brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(id=brain_id)

    rtn_brain_instance = brain_model_to_instance(brain_model)

    # print(rtn_brain_instance)

    return HttpResponse(f"Returned: {rtn_brain_instance} from the database")
