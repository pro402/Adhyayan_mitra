import sounddevice as sd
import numpy as np
import queue
import threading
import os
from pydub import AudioSegment
from pydub.effects import normalize

# for fully android pydub compatibility may be difficult so can 
# we can shift to other libraries like pvrecorder or we can use streamlit-audio-recorder

class AudioRecorder:
    def __init__(self):
        self.q = queue.Queue()
        self.recording = False
        self.audio_frames = []
        self.default_filename = "recording.mp3"

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())
        self.audio_frames.append(indata.copy())

    def start_recording(self, samplerate=44100, channels=1):
        self.audio_frames = []
        self.recording = True

        def record_thread():
            try:
                with sd.InputStream(samplerate=samplerate, 
                                  channels=channels,
                                  dtype='float32',
                                  callback=self.audio_callback):
                    while self.recording:
                        sd.sleep(100)
            except Exception as e:
                print(f"Error: {e}")

        self.thread = threading.Thread(target=record_thread)
        self.thread.daemon = True
        self.thread.start()

    def stop_recording(self, filename=None):
        if not self.recording:
            return None

        self.recording = False
        sd.sleep(50)  # Allow final buffers to process

        if not self.audio_frames:
            return None

        filename = filename or self.default_filename
        recorded_data = np.concatenate(self.audio_frames)
        
        # Audio processing
        recorded_data = recorded_data / np.max(np.abs(recorded_data))
        recorded_data = (recorded_data * 32767).astype(np.int16)
        
        audio = AudioSegment(
            recorded_data.tobytes(),
            frame_rate=44100,
            sample_width=2,
            channels=1
        )
        
        # Apply effects
        audio = audio.compress_dynamic_range()
        audio = normalize(audio)
        audio = audio.high_pass_filter(80)
        audio = audio.low_pass_filter(10000)
        
        # Save with full path
        full_path = os.path.abspath(filename)
        audio.export(full_path, format="mp3", bitrate="128k")
        return full_path