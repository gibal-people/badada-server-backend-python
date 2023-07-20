from rest_framework.serializers import ModelSerializer
from .models import Answer


class TestDataSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'