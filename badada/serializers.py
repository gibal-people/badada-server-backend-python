from rest_framework.serializers import ModelSerializer
from .models import *



class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class MbtiCntSerializer(ModelSerializer):
    class Meta:
        model = MbtiCnt
        fields = '__all__'

class UserCntSerializer(ModelSerializer):
    class Meta:
        model = UserCnt
        fields = '__all__'


class MbtiSerializer(ModelSerializer):
    class Meta:
        model = Mbti
        fields = '__all__'


class AnswerMbtiScoreSerializer(ModelSerializer):
    class Meta:
        model = AnswerMbtiScore
        fields = '__all__'


class BeachSerializer(ModelSerializer):
    class Meta:
        model = Beach
        fields = '__all__'


class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

