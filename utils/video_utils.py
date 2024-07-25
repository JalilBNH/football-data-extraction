import cv2
import os 

def read_video(video_path):
    """Given the path of a video, return a list containing all the frames of this video.

    Args:
        video_path (string): path/to/video

    Returns:
        list[list]: return all the frames of the video in a list. 
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames


def save_video(frames, output_path):
    """Given a list of frame and a path, save a video with opencv

    Args:
        frames (list[list]): list of all the frames
        output_path (string): path/to/output_dir
    """
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 24, frames[0].shape[1], frames[0].shape[0])
    for frame in frames:
        out.write(frame)
    out.release