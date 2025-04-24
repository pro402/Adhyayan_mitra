import os
import shutil
import soundfile as sf
from kokoro import KPipeline
from pydub import AudioSegment

class Kokoro_TTS:
    """
    A class for text-to-speech conversion using the Kokoro TTS model.
    
    Language codes:
    - 🇺🇸 'a' => American English, 🇬🇧 'b' => British English
    - 🇪🇸 'e' => Spanish es
    - 🇫🇷 'f' => French fr-fr
    - 🇮🇳 'h' => Hindi hi
    - 🇮🇹 'i' => Italian it
    - 🇯🇵 'j' => Japanese: pip install misaki[ja]
    - 🇧🇷 'p' => Brazilian Portuguese pt-br
    - 🇨🇳 'z' => Mandarin Chinese: pip install misaki[zh]
    """
    
    def __init__(self, audio_chunk_dir="./audio_chunks"):
        """
        Initialize the Kokoro_TTS class.
        
        Args:
            audio_chunk_dir (str): Directory to store audio chunks.
        """
        self.audio_chunk_dir = audio_chunk_dir
        self.pipeline = None
    
    def remove_previous_audio_chunks(self):
        """Remove previous audio chunks from the directory."""
        try:
            if os.path.exists(self.audio_chunk_dir):
                shutil.rmtree(self.audio_chunk_dir)
                os.makedirs(self.audio_chunk_dir, exist_ok=True)
                print(f"Removed previous audio chunks in {self.audio_chunk_dir}")
            else:
                os.makedirs(self.audio_chunk_dir, exist_ok=True)
                print(f"Directory {self.audio_chunk_dir} created")
        except Exception as e:
            print(f"Error removing directory {self.audio_chunk_dir}: {e}")
    
    def initialize_pipeline(self, lang_code='a', repo_id='hexgrad/Kokoro-82M'):
        """
        Initialize the Kokoro TTS pipeline.
        
        Args:
            lang_code (str): Language code for the TTS model.
            repo_id (str): Repository ID for the model.
        """
        self.pipeline = KPipeline(
            lang_code=lang_code,
            repo_id=repo_id,
            # device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
        )
    
    def create_audio_chunks(self, text, voice='am_adam', speed=1, lang_code='a', repo_id='hexgrad/Kokoro-82M'):
        """
        Create audio chunks from the given text.
        
        Args:
            text (str): Text to convert to speech.
            voice (str): Voice to use for TTS.
            speed (float): Speed of speech.
            lang_code (str): Language code for the TTS model.
            repo_id (str): Repository ID for the model.
        """
        if self.pipeline is None or self.pipeline.lang_code != lang_code:
            self.initialize_pipeline(lang_code, repo_id)
        
        # Generate, display, and save audio files in a loop
        generator = self.pipeline(
            text, 
            voice=voice,
            speed=speed,
            split_pattern=r'\n+',
        )

        for i, (_, _, audio) in enumerate(generator):
            sf.write(f'{self.audio_chunk_dir}/{i}.wav', audio, 24000)  # save each audio file
    
    def merge_wav_files(self, output_path):
        """
        Merge all WAV files in the audio chunk directory into a single file.
        
        Args:
            output_path (str): Path to save the merged audio file.
        """
        # Get all wav files in the directory
        wav_files = []
        i = 0
        while True:
            file_path = os.path.join(self.audio_chunk_dir, f"{i}.wav")
            if os.path.exists(file_path):
                wav_files.append(file_path)
                i += 1
            else:
                break
        
        if not wav_files:
            print("No wav files found.")
            return
        
        # Load the first file
        combined = AudioSegment.from_wav(wav_files[0])
        
        # Append all other files
        for file_path in wav_files[1:]:
            audio = AudioSegment.from_wav(file_path)
            combined += audio
        
        # Export the combined audio
        file_extension = os.path.splitext(output_path)[1].lower()
        format_type = file_extension[1:] if file_extension else "mp3"
        
        combined.export(output_path, format=format_type)
        # print(f"Successfully merged {len(wav_files)} files into {output_path}")
    
    def generate_audio(self, text, output_path, voice='am_adam', speed=1, lang_code='a', repo_id='hexgrad/Kokoro-82M'):
        """
        Generate audio from text and save it to the specified path.
        
        Args:
            text (str): Text to convert to speech.
            output_path (str): Path to save the merged audio file.
            voice (str): Voice to use for TTS.
            speed (float): Speed of speech.
            lang_code (str): Language code for the TTS model.
            repo_id (str): Repository ID for the model.
        """
        self.remove_previous_audio_chunks()
        self.create_audio_chunks(text, voice, speed, lang_code, repo_id)
        self.merge_wav_files(output_path)
        self.remove_previous_audio_chunks()
        
        full_path = os.path.abspath(output_path)
        return full_path

# if __name__ == "__main__":
#     # Example usage
#     tts = Kokoro_TTS(audio_chunk_dir="./audio_chunks")
#     transcript = '''
#         The sky above the port was the color of television, tuned to a dead channel.
#         [Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.
#     '''
#     audio_path = tts.generate_audio(
#         text=transcript,
#         output_path="merged_output.mp3",
#         voice="am_adam",
#         lang_code="a"
#     )
#     print(f"Audio saved to {audio_path}")