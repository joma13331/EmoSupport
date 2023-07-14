"""
This python file deals with audio related code.
It primari deals with following:
    1. Speech-to-text using OpenAI's whisper model
    2. Using Coqui's TTS library for Text-to-Speech
"""

# IMPORTS
import os
import whisper
from TTS.api import TTS


class AudioUtils:

    def __init__(self, stt_model:str = "small.en") -> None:
        self.model = whisper.load_model(stt_model)
        tts_model = "tts_models/en/vctk/vits"
        self.tts = TTS(tts_model)

    def speech_to_text(self, audio_path:str) -> str:
        """
        This function takes in a path to an audio file and returns the text
        present in the audio file.
        """
        text = whisper.transcribe(self.model, audio_path)
        return text["text"]
    
    def text_to_speech(self, text:str, output_path:str, speaker:str="p238") -> None:
        """
        This function takes in a text and converts it into an audio file.
        """
        self.tts.tts_to_file(text=text, speaker=speaker, file_path=output_path)
        return None
    

if __name__ == "__main__":

    audio_utils = AudioUtils()

    # Speech to text
    text = audio_utils.speech_to_text("Data/Audio/chunk_chunk_ani_3_0_mic1.flac")
    audio_utils.text_to_speech(text=text, speaker="p238",output_path="Data/Audio/output.wav") 