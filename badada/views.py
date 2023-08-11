from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *



# 질문 & 답변
@api_view(['GET'])
def qna(request):
    question_data = Question.objects.all()
    question_serializer = QuestionSerializer(question_data, many=True)
    
    qna_serializer = question_serializer

    for i in range(len(qna_serializer.data)):
        answer_data = Answer.objects.filter(question_num=i+1)
        answer_serializer = AnswerSerializer(answer_data, many=True)
        qna_serializer.data[i]["answer"] = []
        
        for j in range(len(answer_serializer.data)):
            answer_data_tmp = answer_serializer.data[j]
            del answer_data_tmp["question_num"]
            qna_serializer.data[i]["answer"].append(answer_data_tmp)

    return Response(qna_serializer.data)





# 질문에 대한 답변을 req body로 받으면 해당 내용을 바탕으로 결과 response

## body 형식
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
    rank_data = MbtiCnt.objects.all().order_by("-mbti_cnt")
    rank_data_serializer = MbtiCntSerializer(rank_data, many=True)

    beach_info = {} # 바다 정보 저장
    beach_attr = [] # 바다 특징
    beach_rec = []  # 바다 추천 이유
    beach_cat = []  # 바다 카테고리
    user = {}     # mbti 누적 수와 전체 사용자 저장하는 변수

    beach_info["beach"] = beach_serializer.data[0]["beach"]
    beach_info["location"] = beach_serializer.data[0]["location"]

    beach_attr = [beach_serializer.data[0][f"attr_{i}"] for i in range(1, 4)]
    beach_rec = [beach_serializer.data[0][f"rec_{i}"] for i in range(1, 4)]
    beach_cat = [beach_serializer.data[0][f"cat_{i}"] for i in range(1, 4)]

    bad_mbti = mbti_serializer.data[0]["bad_mbti"]
    bad_beach_data = Mbti.objects.filter(mbti=bad_mbti)
    bad_beach_serializer = MbtiSerializer(bad_beach_data, many=True)
    
    bad_beach_eng_data = Beach.objects.filter(mbti=bad_mbti)
    bad_beach_eng_serializer = BeachSerializer(bad_beach_eng_data, many=True)
    
    bad_beach = [
        bad_beach_serializer.data[0]["beach"],
        bad_beach_eng_serializer.data[0]["beach_eng"],
    ]
    user["mbti_cnt"] = mbticnt_serializer.data["mbti_cnt"]
    user["total_user_cnt"] = usercnt_serializer.data["total_user_cnt"]


    # 내림차순으로 정렬한 후, 바다가 몇 번째 순위인지 구하기
    mbti_rank = 0
    for i in range(len(rank_data_serializer.data)):
        mbti_rank += 1
        if rank_data_serializer.data[i]["mbti"] == mbti_serializer.data[0]["mbti"]:
            break
        
    
    beach_info["beach_eng"] = beach_serializer.data[0]["beach_eng"]
    beach_info["beach_attr"] = beach_attr
    beach_info["beach_rec"] = beach_rec
    beach_info["beach_cat"] = beach_cat
    beach_info["bad_beach"] = bad_beach
    beach_info["user_cnt"] = user
    beach_info["rank"] = mbti_rank

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


# 피드백 정보 디비에 저장
## body 형식
# {
#     "feedback" : "bad",
#     "choice" : [1,1,1,1,1,"bad"]
# }

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


# 전체 바다 순위
@api_view(['GET'])
def rank(requst):
    mbticnt_data = MbtiCnt.objects.all().order_by("-mbti_cnt")
    user_data = UserCnt.objects.all()
    mbticnt_serializer = MbtiCntSerializer(mbticnt_data, many=True)
    user_serializer = UserCntSerializer(user_data, many=True)

    all_mbti_data = mbticnt_serializer      
    
    # beach, mbti_cnt,total_user 정보를 포함하는 변수
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
        
        beach_eng = beach_serializer.data[0]["beach_eng"]

        all_mbti_data.data[i]["beach_cat"] = beach_cat
        all_mbti_data.data[i]["beach_eng"] = beach_eng
        
        # mbti 내용 필요 x
        del all_mbti_data.data[i]["mbti"]

    return Response(all_mbti_data.data)




# 특정 바다 정보
# 결과 화면에서 보여주는 내용과 동일
@api_view(['GET'])
def beach(request,beach):
    beach_data = Beach.objects.filter(beach_eng=beach)
    beach_serializer = BeachSerializer(beach_data, many=True)

    result = beach_info(beach_serializer.data[0]["beach"])
    return Response(result)








