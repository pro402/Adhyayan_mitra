import sys
import os
from pathlib import Path
from time import time

def transcribe_audio(project_components_dir=None):
    """Main function to handle audio recording and transcription"""
    try:
        # Get the directory where transcripter.py is located
        script_dir = Path(__file__).parent.absolute()
        
        # Determine the components directory path
        if project_components_dir is None:
            # Default: assume components directory is one level up from script_dir
            components_dir = script_dir.parent
        else:
            # Use provided path
            components_dir = Path(project_components_dir)
        
        # Add both the components directory and its parent to sys.path
        if str(components_dir) not in sys.path:
            sys.path.append(str(components_dir))
        
        # Also add the parent directory of components
        components_parent = components_dir.parent
        if str(components_parent) not in sys.path:
            sys.path.append(str(components_parent))
        
        # Import components - try both relative and absolute imports
        try:
            # Try direct import first (if components are in sys.path)
            from audio_recorder.recorder import AudioRecorder
            from components.sTT_model.whisper_tiny import AudioTranscriptor
        except ImportError:
            # If that fails, try with components prefix
            from components.audio_recorder.recorder import AudioRecorder
            from components.sTT_model.whisper_tiny import AudioTranscriptor
        
        # User input handling
        recording = input("""Enter Yes -> If you need to record the audio and then transcribe it.
Enter No -> If you want to transcribe the pre-recorded audio.
""").lower().strip()
        
        # Audio capture logic
        audio_path = None
        
        if recording == "yes":
            recorder = AudioRecorder()
            print("Starting recording...")
            recorder.start_recording()
            input("Recording Has Started. Press Enter when you want to stop!!")
            print("Recording Stopped...")
            
            # Save recording in the same directory as this script
            recording_path = script_dir / "recording.mp3"
            audio_path = recorder.stop_recording(str(recording_path))
            
        elif recording == "no":
            # Look for recording.mp3 in the same directory as this script
            recording_path = script_dir / "recording.mp3"
            if recording_path.exists():
                audio_path = str(recording_path)
            else:
                print("No pre-recorded file found at", recording_path)
                return None
        
        # Transcription logic
        if audio_path and os.path.exists(audio_path):
            transcriptor = AudioTranscriptor()
            print(f"Processing: {audio_path}")
            
            start_time = time()
            transcript = transcriptor.whisper_transcribe(audio_path)
            duration = time() - start_time
            
            time_str = f"{duration:.1f}s" if duration < 60 else f"{duration//60:.0f}m {duration%60:.0f}s"
            print(f"Transcription completed in {time_str}")
            
            # Save transcript in the same directory as this script
            transcript_path = script_dir / "transcript.txt"
            with open(transcript_path, "w") as f:
                f.write(transcript)
            print(f"Transcript saved to {transcript_path}")
            
            return transcript
        else:
            print("Audio file not found")
            return None
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# # Example usage
# if __name__ == "__main__":
#     transcribe_audio()
