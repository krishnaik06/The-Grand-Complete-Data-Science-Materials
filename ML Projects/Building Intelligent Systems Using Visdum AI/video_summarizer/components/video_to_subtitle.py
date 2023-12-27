import os
import tempfile
import warnings
from typing import List, Dict
from dataclasses import dataclass
import ffmpeg

import whisper
from video_summarizer.logger import logger
from video_summarizer.utils.util import write_srt


@dataclass
class Video2SubConfig:
    output_dir: str = 'srt'
    audio_codec: str = 'pcm_s16le'
    audio_sample_rate: str = '16k'
    audio_channels: int = 1


class SubtitleGenerator:
    def __init__(self, config: Video2SubConfig):
        self.output_dir = config.output_dir
        self.audio_sample_rate = config.audio_sample_rate
        self.audio_codec = config.audio_codec
        self.audio_channels = config.audio_channels

# extract_audio_from_video
# generate_subtitles
# get_subtitles -> Output

    def extract_audio_from_video(self, video_paths: List[str]) -> Dict[str, str]:
        temp_dir = tempfile.gettempdir() # tempfile Return the name of the directory used for temporary files
        audio_paths = {}

# https://youtube.com/bfibufpvui

        for video_path in video_paths:
            filename = os.path.basename(video_path).split(".")[0] # dot seperator
            output_path = os.path.join(temp_dir, f"{filename}.wav")

            # ffmpeg library to perform video to audio conversion
            try:
                ffmpeg.input(video_path).output(
                    output_path,
                    acodec="pcm_s16le",
                    ac=self.audio_channels,
                    ar=self.audio_sample_rate,
                ).run(quiet=False, overwrite_output=True, capture_stdout=True, capture_stderr=True)
                
            except ffmpeg.Error as e:
                print('stdout:', e.stdout.decode('utf8'))
                print('stderr:', e.stderr.decode('utf8'))
                raise e
            
            audio_paths[video_path] = output_path

        return audio_paths
    
    def generate_subtitles(
        self, audio_paths: Dict[str, str], transcribe_fn: callable
    ) -> Dict[str, str]:
        subtitles_paths = {}

        for video_path, audio_path in audio_paths.items():
            try:
                filename = os.path.basename(video_path).split(".")[0]
                subtitle_path = os.path.join(self.output_dir, f"{filename}.srt") # abc.srt

                logger.info(
                    f"Generating subtitles for {os.path.basename(audio_path)}... This might take a while."
                )

                warnings.filterwarnings("ignore")
                result = transcribe_fn(audio_path)
                warnings.filterwarnings("default")

                with open(subtitle_path, "w", encoding="utf-8") as srt_file:
                    write_srt(result["segments"], file=srt_file)

                subtitles_paths[video_path] = subtitle_path

            except ffmpeg._run.Error as e:
                logger.error(f"Error generating subtitles for {os.path.basename(audio_path)}: {str(e)}")

        return subtitles_paths, result

    def get_subtitles(
        self, video_paths: List[str], model_path: str, task: str, verbose=False
    ) -> Dict[str, str]:
        os.makedirs(self.output_dir, exist_ok=True)

        if model_path.endswith(".en"):
            print(f"{model_path} is an English model")

        model = whisper.load_model(model_path)
        audio_paths = self.extract_audio_from_video(video_paths)
        subtitles_paths = self.generate_subtitles(
            audio_paths,
            lambda audio_path: model.transcribe(audio_path, verbose=verbose, task=task),
        )

        return subtitles_paths