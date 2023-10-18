from database.models import BrainInstanceModel, GenerationInstanceModel
from rest_framework import serializers


class ModelToBrainInstanceSerializer(serializers.ModelSerializer):
    """
    Serialize the model for model to instance

    """

    class Meta:
        model = BrainInstanceModel
        fields = "__all__"


class ModelToGenerationDataSerializer(serializers.ModelSerializer):
    """
    Serialize the model for model to instance
    """

    class Meta:
        model = GenerationInstanceModel
        fields = "__all__"
