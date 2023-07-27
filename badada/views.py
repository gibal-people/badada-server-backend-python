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
# 답변 보내줄때 int로
## 형식
# {
#     "answer" : [1,5,9,12,15,17,19,23,26,28,32,34]
# }

@api_view(['GET', 'POST'])
def result(request):
    if request.method == 'GET':
        answer = request.data["answer"]
        #1. 불러온 데이터 바탕으로 어떤 mbti인지 파악 (answer_mbti_score)
        mbti = cal_mbti(answer)
        
        #2. mbti에 매칭되는 바다 정보 찾기 (mbti)
        beach = find_beach(mbti)
        
        #3. 바다 정보 return (beach)
        result = beach_info(beach)
        
        #4. mbti와 전체 사용자 수 update (mbti_cnt, user_cnt)
        user = update_cnt(mbti)
        
        result["user_cnt"] = user

        return Response(result)





# 답변을 바탕으로 점수 계산하여 mbti 도출
def cal_mbti(answer):
    mbtiscore_data = AnswerMbtiScore.objects.all()
    mbtiscore_serializer = AnswerMbtiScoreSerializer(mbtiscore_data, many=True)

    e=0;s=0;t=0;p=0
    for i in answer:
        e += mbtiscore_serializer.data[i-1]["e"]
        s += mbtiscore_serializer.data[i-1]["s"]
        t += mbtiscore_serializer.data[i-1]["t"]
        p += mbtiscore_serializer.data[i-1]["p"]

    mbti = ""
    # 각 타입의 유형(ei/ns/tf/jp)합은 1200
    if e > 600 :
        mbti = "E"
    else :
        mbti += "I"

    if s > 600 :
        mbti += "S" 
    else :
        mbti += "N"

    if t > 600 :
        mbti += "T" 
    else :
        mbti += "F"

    if p > 600 :
        mbti += "P" 
    else :
        mbti += "J"

    return(mbti)
    

# mbti에 매칭되는 바다 찾기
def find_beach(mbti):
    mbti_data = Mbti.objects.all()
    mbti_serializer = MbtiSerializer(mbti_data, many=True)

    beach = [item["beach"] for item in mbti_serializer.data if item["mbti"] == mbti]

    return(beach[0])


# 바다 정보
def beach_info(beach):
    beach_data = Beach.objects.filter(beach=beach)
    beach_serializer = BeachSerializer(beach_data, many=True)

    beach_info = {}
    beach_attr = []
    beach_rec = []
    beach_cat = []

    beach_info["beach"] = beach_serializer.data[0]["beach"]
    beach_info["location"] = beach_serializer.data[0]["location"]

    beach_attr = [beach_serializer.data[0][f"attr_{i}"] for i in range(1, 4)]
    beach_rec = [beach_serializer.data[0][f"rec_{i}"] for i in range(1, 4)]
    beach_cat = [beach_serializer.data[0][f"cat_{i}"] for i in range(1, 4)]

    beach_info["beach_attr"] = beach_attr
    beach_info["beach_rec"] = beach_rec
    beach_info["beach_cat"] = beach_cat

    return(beach_info)



# mbti 누적 수 + 1 / 전체 이용자 수 + 1
def update_cnt(mbti):
    mbticnt_data = MbtiCnt.objects.get(mbti=mbti)
    usercnt_data = UserCnt.objects.get(id=1)
    mbticnt_serializer = MbtiCntSerializer(mbticnt_data, many=False)
    usercnt_serializer = UserCntSerializer(usercnt_data, many=False)
    
    user = {} # mbti 누적 수와 전체 사용자 저장하는 변수
    user["mbit_cnt"] = mbticnt_serializer.data["mbti_cnt"]
    user["total_user_cnt"] = usercnt_serializer.data["total_user_cnt"]


    # mbti 누적 수 + 1
    mbticnt_data.mbti_cnt += 1
    mbticnt_data.save()

    # 전체 이용자 수 + 1
    usercnt_data.total_user_cnt += 1
    usercnt_data.save()


    return(user)
















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


