from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os

class VideoAudioMerger:
    def __init__(self, video_path, audio_path):
        self.video_path = video_path
        self.audio_path = audio_path
        self.video_clip = VideoFileClip(video_path)
        self.audio_clip = AudioFileClip(audio_path)

    def merge_video_with_audio(self, result_path):
        final_clip = self.video_clip.set_audio(self.audio_clip)
        final_clip.write_videofile(result_path)

    def remove_original_source_files(self):
        os.remove(self.video_path)
        os.remove(self.audio_path)
