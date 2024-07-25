from ultralytics import YOLO
import supervision as sv
import pickle
import os 

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

    def draw_square():
        pass
    def draw_annotations():
        pass