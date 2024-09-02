from utils import prepare_dataset, read_video, save_video
from matplotlib import pyplot as plt
from trackers import Tracker
import cv2
from ultralytics import YOLO
import cv2

def main():
    model_path = r'C:\Users\Jalil\Desktop\PROJECTS\football-data-extraction\training\runs\detect\train2\weights\best.pt'
    video_path = r'C:\Users\Jalil\Desktop\PROJECTS\football-data-extraction\training\test_model\video-test.mp4'
    
    video_frames = read_video(video_path)
    
    tracker = Tracker(model_path)
    tracks = tracker.get_objects_tracks(video_frames,
                                        read_from_stub=True,
                                        stub_path='stubs/track_stubs.pkl')
    
    # Crop an image to test
    for frame_num, frame in enumerate(video_frames):
        player_dict = tracks['players'][frame_num]
        
        for track_id, player in player_dict.items():
            print(f'track_id : {track_id}, player : {player}')
            
        
    
    
        
        

    #output_video_frames = tracker.draw_annotations(video_frames, tracks)
    
    #save_video(output_video_frames, output_path='./model_inferences/video_test.avi')

    
if __name__ == '__main__':
    main()