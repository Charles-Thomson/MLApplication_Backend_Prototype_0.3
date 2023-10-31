from django.contrib import admin
from database.models import (
    BrainInstanceModel,
    GenerationInstanceModel,
    LearningInstanceModel,
)

# Register your models here.

admin.site.register(BrainInstanceModel)
admin.site.register(GenerationInstanceModel)
admin.site.register(LearningInstanceModel)
