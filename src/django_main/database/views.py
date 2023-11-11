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


from application.lib.agent_brain.brain_factory import new_random_weighted_brain


def index(request):
    """
    Basic landing page for index
    """
    return HttpResponse("Hello, world. You're at the database index.")
