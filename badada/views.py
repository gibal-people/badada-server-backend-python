from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
import json




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
# 바다, 전체 유저수, mbti 누적 수 response
@api_view(['GET'])
def mbti_distribution(request, mbti):
    if mbti == "all":
        mbti_data = MbtiCnt.objects.all()
        user_data = UserCnt.objects.all()
        mbti_serializer = MbtiCntSerializer(mbti_data, many=True)
        user_serializer = UserCntSerializer(user_data, many=True)
      
        total_user_cnt = user_serializer.data[0]['total_user_cnt']
        
        # mbti,mbti_cnt,total_user
        all_mbti_data = mbti_serializer

        for i in range(len(mbti_serializer.data)):
            all_mbti_data.data[i]["total_user_cnt"] = user_serializer.data[0]['total_user_cnt']

        return Response(all_mbti_data.data)




    else:
        mbti_data = MbtiCnt.objects.filter(mbti=mbti)
        user_data = UserCnt.objects.all()
        mbti_serializer = MbtiCntSerializer(mbti_data, many=True)
        user_serializer = UserCntSerializer(user_data, many=True)
        
        mbti_cnt = mbti_serializer.data[0]['mbti_cnt']
        total_user_cnt = user_serializer.data[0]['total_user_cnt']

        mbti_percent = round((mbti_cnt/total_user_cnt) * 100, 1)
        
        
        #mbti_distribution = {}  # 없어도 되는지 확인
        mbti_distribution["mbti"] = mbit
        mbti_distribution["mbti_percent"] = mbti_percent


        return Response(mbti_distribution)







# question_num -> id
# question_content -> content
# answer_content -> content



# api명 : qna
# qna안에 question과 answer 합쳐서 넣어주기




# 전체 결과 보기
# mbti -> 바다 이름



# 사용자 답변 어떤 형식으로 보내줄지 (프론트 -> 백엔드)
## 1번 문제의 answer


# 답변 기반으로 추천하는 바다/카테고리/바다 설명/추천하는 이유/나와 맞지 않는 바다 response

# 결과 바탕으로 mbti_cnt, user_cnt UPDATE


