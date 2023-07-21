from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *




@api_view(['GET'])
def question(request):
    data = Question.objects.all()
    serializer = QuestionSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def answer(request):
    data = Answer.objects.all()
    serializer = AnswerSerializer(data, many=True)
    return Response(serializer.data)



# 상위 몇프로
# request시, mbti 있으면 해당 mbti에 대해서 all이면 전체 리스트(내림차순)
# 전체 유저수, 퍼센트, (?바다?) response
def mbti_distribution(request, mbti):
    if mbti == "all":
        mbti_data = MbtiCnt.objects.all()
        user_data = UserCnt.objects.all()
    else:
        mbti_data = MbtiCnt.objects.filter(mbti=mbti)
        user_data = UserCnt.objects.all()



    








# 상위 몇 프로 (프론트 or 백엔드)
# 사용자 답변 어떤 형식으로 보내줄지 (프론트 -> 백엔드)
# 답변 기반으로 추천하는 바다/카테고리/바다 설명/추천하는 이유/나와 맞지 않는 바다 response
# 결과 바탕으로 mbti_cnt, user_cnt UPDATE
# 피드백 받을 때 어떤 형식으로 줄건지 (json)
# 상위 몇프로인지 보여줄 때, 전체 유저수/퍼센트/(?바다?) 정보 ??
