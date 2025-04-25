from transformers import WhisperProcessor, WhisperForConditionalGeneration, pipeline
import librosa
import torch
from typing import Optional, List, Dict

class AudioTranscriptor:
    def __init__(self, model_name: str = "openai/whisper-tiny", 
                 device: Optional[str] = None, 
                 chunk_length_s: int = 30):
        # Device configuration
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize processor and model
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name)
        self.model.config.forced_decoder_ids = None
        
        # Optimization configurations
        self.model = self.model.to(self.device)
        if torch.__version__ >= "2.0" and self.device == "cuda":
            self.model = torch.compile(self.model)
        
        # Chunk processing parameters
        self.chunk_length_s = chunk_length_s
        self.sampling_rate = 16000  # Whisper's required sampling rate

    def whisper_transcribe(self, audio_path: str, 
                  batch_size: int = 8, 
                  return_timestamps: bool = False) -> str:
        try:
            # Load and resample audio
            audio_array, _ = librosa.load(audio_path, sr=self.sampling_rate)
            
            # Calculate chunk size in samples
            chunk_size = self.chunk_length_s * self.sampling_rate
            total_samples = len(audio_array)
            
            # Split audio into chunks
            chunks = [
                audio_array[i : i + chunk_size] 
                for i in range(0, total_samples, chunk_size)
            ]
            
            # Process chunks in batches
            transcriptions = []
            for batch_idx in range(0, len(chunks), batch_size):
                batch = chunks[batch_idx : batch_idx + batch_size]
                
                # Process batch
                inputs = self.processor(
                    batch,
                    sampling_rate=self.sampling_rate,
                    return_tensors="pt",
                    padding=True,
                    truncation=True
                ).input_features.to(self.device)
                
                # Generate predictions
                with torch.inference_mode():
                    predicted_ids = self.model.generate(inputs)
                
                # Decode predictions
                batch_transcriptions = self.processor.batch_decode(
                    predicted_ids, 
                    skip_special_tokens=True
                )
                
                transcriptions.extend(batch_transcriptions)
            
            return " ".join(transcriptions)
        
        except Exception as e:
            print(f"Transcription error: {e}")
            return None

    def whisper_transcribe_with_timestamps(self, audio_path: str) -> List[Dict]:
        """Advanced method with timestamp support"""
        # Implementation would require custom timestamp alignment
        # This is a simplified version using the pipeline approach
        pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            feature_extractor=self.processor.feature_extractor,
            tokenizer=self.processor.tokenizer,
            chunk_length_s=30,
            device=self.device,
        )
        
        return pipe(audio_path, return_timestamps=True)["chunks"]