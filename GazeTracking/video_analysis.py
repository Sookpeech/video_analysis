import cv2
import mediapipe as mp
from gaze_tracking import GazeTracking
import time
import numpy as np


def video_analysis(sensitivity, video_path):
    # 라이브러리 gaze 클래스 초기화
    gaze = GazeTracking()
    
    # 라이브러리 pose 클래스 초기화
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    # 비디오 객체 불러오기
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened()==False:
        print("동영상 불러오기에 실패했습니다.")
    
    
    
    # 변수 정의
    FPS = int(cap.get(cv2.CAP_PROP_FPS)) # 동영상의 fps 알아냄
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 전체 frame 수 알아냄
    duration = frame_count/FPS # fps와 전체 frame 수로 동영상 길이 알아냄

    # 자세가 바르지 않은 시간을 세는 변수
    count = 0
    
    # 각 제스처의 시간을 세는 변수
    first_count = 0 # 1번 제스처
    second_count = 0 # 2번 제스처
    third_count = 0 # 3번 제스처
    face_count = 0 # 주변
    movement_count = 0 # 얼굴
    script_count = 0 # 대본
    
    # 프레임 변수
    f_count = 0
    
    # 자세 불량 flag 변수
    p_before = 0; p_present = 0

    # 첫번째 제스처 flag 변수
    f_before = 0; f_present = 0

    # 두 번째 제스처 flag 변수
    s_before = 0; s_present = 0

    # 세 번째 제스처 flag 변수
    t_before = 0; t_present = 0
    
    # face
    face_before = 0; face_present = 0

    # script
    script_before = 0; script_present = 0

    # face movement
    movement_before = 0; movement_present = 0
    
    # 눈 깜박임 횟수 보정값
    correction = duration / 20

    # 분석 시작 시간
    start = time.time()

    
    
    while True:
        success, img = cap.read()

        # 원하는 프레임 단위로 cut
        cap.set(cv2.CAP_PROP_POS_FRAMES,f_count/2);
        f_count += FPS

        # 동영상이 끝나면 break
        if (np.shape(img) == ()): break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        

        # 각 변수에 스켈레톤 저장
        left_shoulder = results.pose_landmarks.landmark[11]
        right_shoulder = results.pose_landmarks.landmark[12]

        left_wrist = results.pose_landmarks.landmark[15]
        right_wrist = results.pose_landmarks.landmark[16]

        left_elbow = results.pose_landmarks.landmark[13]
        right_elbow = results.pose_landmarks.landmark[14]

        left_hip = results.pose_landmarks.landmark[23]
        right_hip = results.pose_landmarks.landmark[24]

        nose = results.pose_landmarks.landmark[0]
        
        
        # 조건 잡아내기
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            
            
            # 1초 동안 그 행동을 했다고 판단하면 각 count 변수에 더하기
            # FPS/2를 하는 이유는 프레임수를 FPS/2로 건너뛰었기 때문에
            if p_before == p_present and p_present == 1:
                count += FPS/2

            if f_before == f_present and f_present == 1:
                first_count += FPS/2

            if s_before == s_present and s_present == 1:
                second_count += FPS/2

            if t_before == t_present and t_present == 1:
                third_count += FPS/2
                
            # 변수 초기화하기
            p_before = p_present
            f_before = f_present
            s_before = s_present
            t_before = t_present
            
            
            # 얼굴 움직임 분석
            if (abs(nose.x - 0.5) >= (11 - sensitivity) * 0.1):
                movement_present = 1
            else:
                movement_present = 0


            # 자세 분석
            if (abs((left_shoulder.x + right_shoulder.x) / 2 - 0.5) >= 0.1):
                print("몸을 화면 가운데에 맞춰주세요.")

            if (abs(left_shoulder.y - right_shoulder.y) >= (11 - sensitivity) * 0.01):
                # print("두 어깨의 균형이 맞지 않습니다.")
                p_present = 1
            else:
                p_present = 0

            # 제스처 분석
    
            # 1번: 손이 얼굴 위로 올라갔을 때
            if ((left_wrist.x < left_shoulder.x) and (left_wrist.x > right_shoulder.x) \
               and (left_wrist.y < left_shoulder.y)):
                f_present = 1

            elif ((right_wrist.x < left_shoulder.x) and (right_wrist.x > right_shoulder.x) \
               and (right_wrist.y < right_shoulder.y)):
                f_present = 1
            else:
                f_present = 0

            # 2번: 팔짱 끼거나 한 쪽 팔을 잡았을 때, 손 맞잡을 때
            if (abs(left_wrist.x - right_shoulder.x) <= sensitivity * 0.05 or abs(left_wrist.x - right_shoulder.x) <= sensitivity * 0.05):
                s_present = 1
            else:
                s_present = 0

            # 3번: 허리에 손을 올렸을 때
            if (left_wrist.y < left_hip.y and right_wrist.y < right_hip.y):
                if (abs(left_wrist.x - left_hip.x) <= sensitivity * 0.01 and (left_hip.y - left_wrist.y) <= sensitivity * 0.005 and abs(right_wrist.x - right_hip.x) <= sensitivity * 0.01 and (right_hip.y - right_wrist.y) <= sensitivity * 0.005):
                    t_present = 1
                else:
                    t_present = 0

                    
                    
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(img)
        new_img = gaze.annotated_frame()

        if movement_before == movement_present and movement_present == 1:
            movement_count += FPS/2

        if face_before == face_present and face_present == 1:
            face_count += FPS/2

        if script_before == script_present and script_present == 1:
            script_count += FPS/2

        face_before = face_present
        script_before = script_present
        movement_before = movement_present

        if gaze.is_blinking():
            script_present = 1
        else:
            script_present = 0

        if gaze.is_right():
            face_present = 1
        elif gaze.is_left():
            face_present = 1
        else:
            face_present = 0
        
        
        cv2.namedWindow('pose', cv2.WINDOW_NORMAL)
        cv2.imshow("pose", img)
        cv2.waitKey(1)

    end = time.time()
    cap.release()
    cv2.destroyWindow("pose")

    minutes = int(duration / 60)
    seconds = duration % 60

    print("영상 길이 : " + str(minutes) + ':' + str(seconds))
    print("분석에 걸린 시간 : ", (end - start))
    print("fps : ", FPS)

    print("자세가 기울어진 시간 : ", count/FPS)
    print("1번 제스처 시간 : ", first_count/FPS)
    print("2번 제스처 시간 : ", second_count/FPS)
    print("3번 제스처 시간 : ", third_count/FPS)
    if (script_count/FPS - correction > 0):
        print("시선이 분산된 시간(대본) : ", script_count/FPS - correction)
    print("시선이 분산된 시간(주변) : ", face_count/FPS)
    print("얼굴 움직임 시간 : ", movement_count/FPS)
    
    return count/FPS, first_count/FPS, second_count/FPS, third_count/FPS, script_count/FPS - correction, face_count/FPS, movement_count/FPS
  
  
  
# 민감도는 1부터 10까지의 정수
# sensitivity = int(input("민감도를 입력해주세요.(1 ~ 10) : "))
# video_path = 'C:/Users/82109/Videos/sample.mp4'

# pose_time, f_time, s_time, t_time, script_time, face_time, movement_time = video_analysis(sensitivity, video_path)
# print(pose_time, " ", f_time, " ", s_time, " ", t_time, " ", script_time, " ", face_time, " ", movement_time)
