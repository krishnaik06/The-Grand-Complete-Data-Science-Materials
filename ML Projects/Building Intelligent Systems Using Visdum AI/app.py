import os
from flask import Flask, render_template, request, send_from_directory
from video_summarizer.components.video_to_subtitle import SubtitleGenerator, Video2SubConfig
from video_summarizer.components.summarize import Summarizer
from video_summarizer.pipeline import run_training_pipeline
import threading

from gtts import gTTS

from video_summarizer.components.video_downloader import VideoDownloader

app = Flask(__name__)
app.config['upload_dir'] = os.path.join('uploads/')
os.makedirs(app.config['upload_dir'], exist_ok=True)

print("Loading Summarizer model")
summarizer = Summarizer()
summarizer.load_model()


@app.route('/', methods=['GET'])
def index():
    """
    It renders the index.html file in the templates folder

    Returns:
      The index.html file is being returned.
    """
    return render_template('index.html')


@app.route('/transcribe', methods=['POST'])
def upload_file():
    """
    The function upload_file() takes in a video file or a video link, transcribes the video, and
    summarizes the transcript

    Returns:
      the transcript and summary text.
    """
    if request.method == 'POST':
        video_file = request.files["video_file"]
        subtitle_generator = SubtitleGenerator(config=Video2SubConfig)
        if video_file:
            filename = video_file.filename
            video_path = os.path.join(os.path.join(
                app.config['upload_dir'], filename))
            print(video_path)
            video_file.save(video_path)
            task = 'transcribe'
            if len(request.form.getlist('translate-btn')) > 0:
                task = 'translate'
                print("translate task is selected:", task)
            subtitle = subtitle_generator.get_subtitles(video_paths=video_path,
                                                       model_path='tiny', task=task, verbose=False)
        else:
            video_link = request.form["link-input"]
            downloader = VideoDownloader(
                url=video_link, save_path=app.config['upload_dir'])
            video_path = downloader.download()
            task = 'transcribe'
            option = request.form.get('options')
            if option == 'translate':
                task = 'translate'
                print("translate task is selected:", task)
            print("task selected:", task)
            subtitle = subtitle_generator.get_subtitles(video_paths=[video_path],
                                                       model_path='tiny', task=task, verbose=False)
        transcript_text = subtitle[1]['text']
        summary_text = summarizer.summarize_text(transcript_text)
        tts = gTTS(summary_text, tld="co.uk")
        audio_path = os.path.join(app.config['upload_dir'], 'summary.mp3')
        tts.save(audio_path)

        return render_template('index.html', transcript=transcript_text, summary=summary_text, audio_path=audio_path)
    
    
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(app.config['upload_dir'], filename, mimetype='audio/mpeg')


@app.route('/train', methods=['GET', 'POST'])
def start_train():
    def run_training():
        run_training_pipeline()
    train_thread = threading.Thread(target=run_training)
    train_thread.start()
    return "Training has started"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    