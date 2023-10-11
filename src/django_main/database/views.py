from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


from django.http import HttpResponse

from application.lib.agent_brain.static_state_brain import BrainInstance


from database.models import BrainInstanceModel

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the database index.")


# TODO: Work out the import for the BrainInstance
# TODO: Test the conversion from brain to model instance
# TODO: Test saving the model instance
# TODO: test converting the instance back to a brain instance
# TODO: Work out the testing of the above

# python manage.py makemigrations
# python manage.py makesuperuser
# run tests from top level folder


# @require_http_methods(["POST"])
def add_all(request):
    """Add a new Brain Instance"""

    brain_type = "general"
    brain_id = "2"
    generation_num = "test number 0"
    hidden_weights = "[5,6,7,8]"
    output_weights = "[5,6,7,8]"

    brain_type = bytes(brain_type, encoding="utf-8")
    brain_id = bytes(brain_id, encoding="utf-8")
    generation_num = bytes(generation_num, encoding="utf-8")
    hidden_weights = bytes(hidden_weights, encoding="utf-8")
    output_weights = bytes(output_weights, encoding="utf-8")

    new_brain_instance = BrainInstanceModel(
        brain_type=brain_type,
        brain_id=brain_id,
        generation_num=generation_num,
        hidden_weights=hidden_weights,
        output_weights=output_weights,
    )

    new_brain_instance.save()
    return HttpResponse("Item should be added to the DB")


def get_instance(request) -> None:
    """Get a brain Instance back from the model"""

    brain_model: BrainInstanceModel = BrainInstanceModel.objects.get(id=2)

    return HttpResponse(f"Returned: {brain_model} from the database")
