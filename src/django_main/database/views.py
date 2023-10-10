from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from database.model_data_formatting import 

from django.http import HttpResponse

# from src.application.lib.agent_brain.brain_factory import BrainInstance

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
    brain_id = "test id 1"
    generation_num = "test number 0"
    hidden_weights = "[5,6,7,8]"
    output_weights = "[5,6,7,8]"

    new_brain_instance = BrainInstanceModel(
        brain_type=brain_type,
        brain_id=brain_id,
        generation_num=generation_num,
        hidden_weights=hidden_weights,
        output_weights=output_weights,
    )

    new_brain_instance = brain_instance_handling.brain_instance_to_model(
        brain_instance=test_brain, model_type="general"
    )

    new_brain_instance.save()
    return HttpResponse("Item should be added to the DB")
