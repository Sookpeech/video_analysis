'''
item: wav로 변환하고자 하는 mp4 파일
save_path: 변환된 wav 파일을 저장할 경로
save_file_id: wav 파일로 저장할 파일명
'''

# 관리자 권한으로 실행
!pip install ffmpeg

import subprocess
import ffmpeg
import os

def make_wav(item, save_path, save_file_id):
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(item, os.path.join(save_path, save_file_id))
    subprocess.call(command, shell=True)
    
    
# item = 'C:/Users/82109/music.mp4'
# save_path = 'C:/Users/82109/Project/'
# save_file_id = 'music.wav'

# make_wav(item, save_path, save_file_id)
