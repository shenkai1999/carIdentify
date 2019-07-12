#沈楷
from imageai.Detection import VideoObjectDetection
import os
import time
import cv2
def videoIdentify(input_dir,output_dir):
    execution_path = os.getcwd()
    detector = VideoObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()

    video_path = detector.detectObjectsFromVideo(input_file_path=input_dir, output_file_path=output_dir, frames_per_second=20, log_progress=True)
    print(video_path)


# img = cv2.VideoCapture('okvideo.avi')
# fourcc = cv2.VideoWriter_fourcc(*'XVID')#视频编码格式
# out = cv2.VideoWriter('save.mp4',fourcc,20,(640,480))




