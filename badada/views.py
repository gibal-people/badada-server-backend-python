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


@api_view(['GET'])
def qna(request):
    question_data = Question.objects.all()
    answer_data = Answer.objects.all()
    question_serializer = QuestionSerializer(question_data, many=True)
    answer_serializer = AnswerSerializer(answer_data, many=True)

    qna_serializer = question_serializer

    for i in range(len(qna_serializer.data)):
        qna_serializer.data[i]["answer"]= answer_serializer.data[i]
        del qna_serializer.data[i]["answer"]["question_num"]


    return Response(qna_serializer.data)





# 답변 기반으로 추천하는 바다/카테고리/바다 설명/추천하는 이유/나와 맞지 않는 바다 response
@api_view(['GET', 'POST'])
def result(request):
    if request.method == 'GET':
        data = request.data
        print(type(data["answer"][0]))
        
        return Response({'success': True})











# 상위 몇프로
# request시, mbti 있으면 해당 mbti에 대해서 all이면 전체 리스트(내림차순)
# 바다, 전체 유저수, mbti 누적 수 response
@api_view(['GET'])
def mbti_distribution(request,mbti):
    if mbti == "all":
        mbticnt_data = MbtiCnt.objects.all()
        user_data = UserCnt.objects.all()
        mbticnt_serializer = MbtiCntSerializer(mbticnt_data, many=True)
        user_serializer = UserCntSerializer(user_data, many=True)
      
        
        all_mbti_data = mbticnt_serializer                              # beach, mbti_cnt,total_user 정보를 포함하는 변수
        total_user_cnt = user_serializer.data[0]['total_user_cnt'] 
        

        for i in range(len(mbticnt_serializer.data)):
            all_mbti_data.data[i]["total_user_cnt"] = user_serializer.data[0]['total_user_cnt']

            mbti_data = Mbti.objects.filter(mbti=all_mbti_data.data[i]["mbti"])
            mbti_serializer = MbtiSerializer(mbti_data, many=True)
            all_mbti_data.data[i]["beach"] = mbti_serializer.data[0]["beach"]

            del all_mbti_data.data[i]["mbti"]

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
        mbti_distribution["mbti"] = mbti
        mbti_distribution["mbti_percent"] = mbti_percent


        return Response(mbti_distribution)

















# 결과 바탕으로 mbti_cnt, user_cnt UPDATE


