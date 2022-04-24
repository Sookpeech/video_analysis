import cv2
import mediapipe as mp
import time


mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
count = 0 #자세 불량 횟수

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('videos/Girl - 48019.mp4')
pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    left_shoulder = results.pose_landmarks.landmark[11]
    right_shoulder = results.pose_landmarks.landmark[12]
#     print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
        print("left_shoulder.x: ", left_shoulder.x, "left_shoulder.y: ", left_shoulder.y)
        print("right_shoulder.x: ", right_shoulder.x, "right_shoulder.y: ", right_shoulder.y)
        if (abs((left_shoulder.x + right_shoulder.x) / 2 - 0.5) >= 0.1):
            print("몸을 화면 가운데에 맞춰주세요.")
            cv2.putText(img, "Please adjust your body to the standard.", (100,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
        if (abs(left_shoulder.y - right_shoulder.y) >= 0.01):
            print("두 어깨의 균형이 맞지 않습니다.")
            cv2.putText(img, "The posture is not correct.", (100,100), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
