from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *



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

@api_view(['POST'])
def result(request):
    
    answer = request.data["answer"]
    #1. 불러온 데이터 바탕으로 어떤 mbti인지 파악 (answer_mbti_score)
    mbti = cal_mbti(answer)
    
    #2. mbti에 매칭되는 바다 정보 찾기 (mbti)
    beach = find_beach(mbti)
    
    #3. 바다 정보 return (beach)
    result = beach_info(beach)
    
    #4. mbti와 전체 사용자 수 update (mbti_cnt, user_cnt)
    update_cnt(mbti)

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
    mbti_data = Mbti.objects.filter(beach=beach)
    mbti_serializer = MbtiSerializer(mbti_data, many=True)
    usercnt_data = UserCnt.objects.get(id=1)
    usercnt_serializer = UserCntSerializer(usercnt_data, many=False)
    mbticnt_data = MbtiCnt.objects.get(mbti=mbti_serializer.data[0]["mbti"])
    mbticnt_serializer = MbtiCntSerializer(mbticnt_data, many=False)


    beach_info = {}
    beach_attr = []
    beach_rec = []
    beach_cat = []
    bad_beach = ""
    user = {}     # mbti 누적 수와 전체 사용자 저장하는 변수

    beach_info["beach"] = beach_serializer.data[0]["beach"]
    beach_info["location"] = beach_serializer.data[0]["location"]

    beach_attr = [beach_serializer.data[0][f"attr_{i}"] for i in range(1, 4)]
    beach_rec = [beach_serializer.data[0][f"rec_{i}"] for i in range(1, 4)]
    beach_cat = [beach_serializer.data[0][f"cat_{i}"] for i in range(1, 4)]


    bad_mbti = mbti_serializer.data[0]["bad_mbti"]
    bad_beach_data = Mbti.objects.filter(mbti=bad_mbti)
    bad_beach_serializer = MbtiSerializer(bad_beach_data, many=True)
    bad_beach = bad_beach_serializer.data[0]["beach"]
    user["mbit_cnt"] = mbticnt_serializer.data["mbti_cnt"]
    user["total_user_cnt"] = usercnt_serializer.data["total_user_cnt"]

    beach_info["beach_attr"] = beach_attr
    beach_info["beach_rec"] = beach_rec
    beach_info["beach_cat"] = beach_cat
    beach_info["bad_beach"] = bad_beach
    beach_info["user_cnt"] = user
    

    return(beach_info)


# mbti 누적 수 + 1 / 전체 이용자 수 + 1
def update_cnt(mbti):
    mbticnt_data = MbtiCnt.objects.get(mbti=mbti)
    usercnt_data = UserCnt.objects.get(id=1)


    # mbti 누적 수 + 1
    mbticnt_data.mbti_cnt += 1
    mbticnt_data.save()

    # 전체 이용자 수 + 1
    usercnt_data.total_user_cnt += 1
    usercnt_data.save()

    return()



@api_view(['POST'])
def feedback(request):
    # Good Feedback 
    if request.data["feedback"] == "good":
        feedback_data = Feedback.objects.create(
            good = 1,
            good_1 = request.data["choice"][0],
            good_2 = request.data["choice"][1],
            good_3 = request.data["choice"][2],
            good_4 = request.data["choice"][3],
            good_5 = request.data["choice"][4],
            good_text = request.data["choice"][5],

            bad = 0,
            bad_1 =0,
            bad_2 =0,
            bad_3 =0,
            bad_4 =0,
            bad_5 =0,
            bad_text=""
        )
    # Bad Feedback 
    else:
        feedback_data = Feedback.objects.create(
            bad = 1,
            bad_1 = request.data["choice"][0],
            bad_2 = request.data["choice"][1],
            bad_3 = request.data["choice"][2],
            bad_4 = request.data["choice"][3],
            bad_5 = request.data["choice"][4],
            bad_text = request.data["choice"][5],

            good = 0,
            good_1 =0,
            good_2 =0,
            good_3 =0,
            good_4 =0,
            good_5 =0,
            good_text=""
        )

    return Response("Success")



@api_view(['GET'])
def rank(requst):
    mbticnt_data = MbtiCnt.objects.all()
    user_data = UserCnt.objects.all()
    mbticnt_serializer = MbtiCntSerializer(mbticnt_data, many=True)
    user_serializer = UserCntSerializer(user_data, many=True)
    


    all_mbti_data = mbticnt_serializer                              # beach, mbti_cnt,total_user 정보를 포함하는 변수
    total_user_cnt = user_serializer.data[0]['total_user_cnt'] 

    for i in range(len(mbticnt_serializer.data)):
        all_mbti_data.data[i]["total_user_cnt"] = total_user_cnt

        mbti_data = Mbti.objects.filter(mbti=all_mbti_data.data[i]["mbti"])
        mbti_serializer = MbtiSerializer(mbti_data, many=True)
        all_mbti_data.data[i]["beach"] = mbti_serializer.data[0]["beach"]

        beach_data = Beach.objects.filter(beach=mbti_serializer.data[0]["beach"])
        beach_serializer = BeachSerializer(beach_data, many=True)

        beach_cat = [
            beach_serializer.data[0]["cat_1"],
            beach_serializer.data[0]["cat_2"],
            beach_serializer.data[0]["cat_3"],
        ]

        all_mbti_data.data[i]["beach_cat"] = beach_cat

        del all_mbti_data.data[i]["mbti"]

    return Response(all_mbti_data.data)






# 상위 몇프로
# request시, mbti 있으면 해당 mbti에 대해서 all이면 전체 리스트(내림차순)
# 바다, 전체 유저수, mbti 누적 수 response
@api_view(['GET'])
def beach(request,mbti):
    print("****************")
    print(mbti)
    mbti_data = Mbti.objects.filter(mbti=mbti)
    mbti_serializer = MbtiSerializer(mbti_data, many=False)
    print("****************")

    bad_mbti = mbti_serializer.data[0]["bad_mbti"]
    return Response(bad_mbti)








