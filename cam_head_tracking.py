#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 13:14:57 2018

@author: eric
"""
import FaceVar
from kf_2points import kf_2points
from collections import deque
import numpy as np
import glob
from face_utils import box_iou2, draw_box_on_image, draw_marks_on_image
from scipy.optimize import linear_sum_assignment
import cv2
from FaceDetector import FaceDetector
import time
from MarkDetector import MarkDetector
from MarkStabilizer import MarkStabilizer
from PoseEstimator import PoseEstimator
from kf_FaceTracker import Tracker

def main():
    video_src = 0  # 0 means webcam; set file name if video
    cam = cv2.VideoCapture(video_src)
    _, sample_frame = cam.read()  # get 1 sample frame to setup codes
    height, width = sample_frame.shape[:2]
    face_detector = FaceDetector()
    tracker = Tracker(FaceVar.IOU_THRESHOLD, img_size=(height, width))
    
    while True:
        frame_got, frame = cam.read()
        
        if frame_got is False:
            break
        conf, boxes = face_detector.get_faceboxes(image=frame, threshold=0.9)
        matches, unmatched_dets, unmatched_tracks = tracker.assign_detections_to_trackers(boxes)
        tracker.update(frame, boxes, matches, unmatched_dets, unmatched_tracks)
        frame = tracker.annotate_BBox(frame)
        
        # if facebox is not None:(image=frame, marksFace=stabilized_marks68)            
            
           
        
        cv2.imshow("preview", frame)
        if cv2.waitKey(10) == 27:
            break
        
if __name__ == '__main__':
    main()