# video_analysis


## make_wav.py
음성 분석을 위해 mp4 파일을 wav 파일로 변환

입력 파라미터: item, save_path, save_file_id

item: wav로 변환하고자 하는 mp4 파일(ex. 'C:/Users/82109/music.mp4')

save_path: 변환된 wav 파일을 저장할 경로(ex. 'C:/Users/82109/Project/')

save_file_id: wav 파일로 저장할 파일명(ex. 'music.wav')



## GazeTracking/video_analysis.py
자세 분석/제스처 분석/시선 분석 포함

입력 파라미터: sensitivity(정수), video_path(ex. 'C:/Users/82109/Videos/sample.mp4')

pose_time, f_time, s_time, t_time, script_time, face_time, movement_time 반환
\n
pose_time: 자세가 기울어진 시간

f_time: 1번 제스처(손이 얼굴 위로 올라갔을 때)

s_time: 2번 제스처(팔짱 끼거나 한 쪽 팔을 잡았을 때, 손 맞잡을 때)

t_time: 3번 제스처(허리에 손을 올렸을 때)

script_time: 시선이 대본으로 향한 시간

face_time: 시선이 주변으로 분산된 시간

movement_time: 얼굴을 움직인 시간


\n
※ GazeTracking 버전

numpy == 1.16.1

opencv_python == 4.2.0.32

dlib == 19.16.0



<s>1. 어깨의 x좌표
- x좌표는 인물이 카메라의 중심에 위치했는지를 알아내는 기준으로 사용하였음.
- 왼쪽 어깨의 좌표와 오른쪽 어깨의 좌표를 더해서 2로 나눈 결과를 몸의 중심 좌표라고 생각하고 그 좌표가 화면의 중심으로부터 0.1 벗어났으면 경고 문구를 출력함.
- 벗어난 정도는 변경 가능함.

2. 어깨의 y좌표
- y좌표는 인물의 자세가 바른지를 알아내는 것으로 사용하였음.
- 두 어깨의 y좌표가 심하게 차이날 경우 바른 자세가 아닌 것으로 판단함.
- 두 어깨의 y좌표 차이도 변경 가능함.

3. count 변수
- count 변수를 통해 잘못된 자세의 횟수를 세어 피드백 시 출력할 수 있음.

● 보완해야 할 점
- x좌표와 y좌표의 각각의 기준을 세부적으로 정해야함. 컴퓨터와 스마트폰의 화면 비율의 차이때문에 직접 해보면서 조정해야 함.
- 발표할 때 약간의 자세 변경이 있을 수 있으므로 극단적으로 보이는 경우가 어디서부터인지 정해야 함.
- 현재는 두 어깨의 좌표만으로 설정했지만 다른 좌표로도 할 필요성이 있는지 확인해야 함.</s>
