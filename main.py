from utils import prepare_dataset, read_video
from trackers import Tracker
import cv2
from ultralytics import YOLO

def main():
    model_path = r'C:\Users\Jalil\Desktop\PROJECTS\football-data-extraction\training\runs\detect\train2\weights\best.pt'
    video_path = r'C:\Users\Jalil\Desktop\PROJECTS\football-data-extraction\training\test_model\video-test.mp4'
    
    video_frames = read_video(video_path)
    
    tracker = Tracker(model_path)
    tracks = tracker.get_objects_tracks(video_frames,
                                        read_from_stub=True,
                                        stub_path='stubs/track_stubs.pkl')
    
    print(tracks['players'][10])

    
if __name__ == '__main__':
    main()