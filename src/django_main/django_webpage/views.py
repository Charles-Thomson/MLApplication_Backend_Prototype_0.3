from django.shortcuts import render

from database.models import BrainInstanceModel, GenerationInstanceModel

from django_webpage.svg_handling.svg_generation import build_svg_data

# Create your views here.


# Create your views here.
def index(request):
    """Get and render all saved brain instances"""
    # rework to get by generation ref
    all_generations = GenerationInstanceModel.objects.all()

    # This is how to return the page
    return render(
        request,
        "flex_base.html",
        {
            "All_Geneerations_list": all_generations,
            # "Fit_BrainInstance_list": all_fit_brain_instances_with_svg_built,
        },
    )
