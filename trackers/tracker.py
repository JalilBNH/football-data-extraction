from ultralytics import YOLO
import supervision as sv
import pickle
import os 
import cv2
import sys
sys.path.append('../')
from utils import get_center_of_bbox, get_bbox_width
from sklearn.cluster import KMeans
from colorthief import ColorThief

class Tracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()
        
    def detect_frames(self, video_frames):
        detections = self.model.predict(video_frames)
        return detections
    
    def get_objects_tracks(self, video_frames, read_from_stub=None, stub_path=None):
        
        detections = self.detect_frames(video_frames)
        
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                tracks = pickle.load(f)
            return tracks
        
        tracks = {
            'players': [],
            'goalkeeper': [],
            'referee': [],
            'ball': []
        }
            
        for frame_num, detection in enumerate(detections):
            class_names = detection.names
            class_names_inv = {value : key for key, value in class_names.items()}
            
            detection_supervision = sv.Detections.from_ultralytics(detection)
            tracks['players'].append({})
            tracks['goalkeeper'].append({})
            tracks['referee'].append({})
            tracks['ball'].append({})
            
            detection_tracks = self.tracker.update_with_detections(detection_supervision)
            
            for frame_detection in detection_tracks:
                bbox = frame_detection[0].tolist()
                class_id = frame_detection[3]
                track_id = frame_detection[4]

                #print(f'bbox: {bbox}, class_id: {class_id}, track_id: {track_id}')
                if class_id == class_names_inv['player']:
                    tracks['players'][frame_num][track_id] = {'bbox': bbox}
                if class_id == class_names_inv['goalkeeper']:
                    tracks['goalkeeper'][frame_num][track_id] = {'bbox': bbox}
                if class_id == class_names_inv['referee']:
                    tracks['referee'][frame_num][track_id] = {'bbox': bbox}
            
            for frame_detection in detection_supervision:
                bbox = frame_detection[0].tolist()
                class_id = frame_detection[3]
                if class_id == class_names_inv['ball']:
                    
                    tracks['ball'][frame_num] = {'bbox': bbox}
        
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(tracks, f)
        
        return tracks # We have the tracks dictionnnary under this format tracks[object][frame_num][track_id]

    def draw_square(self, frame, bbox, track_id=None):
        x1, y1, x2, y2 = bbox
        cv2.rectangle(
            frame,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            color=(255, 0, 0),
            thickness=2
        )
        return frame
    
    def draw_ellipse(self, frame, bbox, color, track_id=None):
        y2 = int(bbox[3])
        x_center, _ = get_center_of_bbox(bbox)
        width = get_bbox_width(bbox)
        
        cv2.ellipse(
            frame,
            center=(x_center, y2),
            axes=(int(width), int(0.35*width)),
            angle=0.0,
            startAngle=45,
            endAngle=235,
            color=color,
            thickness=1,
            lineType=cv2.LINE_4
        )
        
        rectangle_width = 40
        rectangle_height = 20
        
        x1_rect = x_center - rectangle_width//2
        y1_rect = (y2 - rectangle_height//2) +15
        x2_rect = x_center + rectangle_width//2
        y2_rect = (y2 + rectangle_height//2) + 15
        
        if track_id is not None:
            cv2.rectangle(
                frame,
                (int(x1_rect), int(y1_rect)),
                (int(x2_rect), int(y2_rect)),
                color,
                cv2.FILLED
            )
            x1_text = x1_rect + 12
            if track_id > 99:
                x1_text -= 10
            
            cv2.putText(
                frame,
                f'{track_id}',
                (int(x1_text), int(y1_rect + 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,255)
            )
        
        return frame
        
    def draw_annotations(self, video_frames, tracks):
        color_dict = {0 : (255,0,0), 1 : (0,0,255)}
        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            
            
            player_dict = tracks['players'][frame_num]
            ball_dict = tracks['ball'][frame_num]
            goalkeeper_dict = tracks['goalkeeper'][frame_num]
            referee_dict = tracks['referee'][frame_num]
            
            for track_id, player in player_dict.items():
                bbox = player['bbox']
                colo
                
                frame = self.draw_ellipse(frame, player['bbox'], (255,0,0), track_id)
            output_video_frames.append(frame)
        
        return output_video_frames