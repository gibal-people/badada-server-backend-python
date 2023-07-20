from rest_framework.serializers import ModelSerializer
from .models import Answer
from .models import Question


class TestDataSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class TestDataSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'