from TTS.api import TTS
from pathlib import Path
import os
import sys
from pydub import AudioSegment

class TextToSpeech:
    """
    This class will take the text analysis of the MusicXML file,
    Then using Coqui TTS output a wav file. 
    """
    def __init__(self, output_path: str, input_txt_path: str):
        self.input_txt_path = input_txt_path
        self.output_path = output_path

    def output_tts(self) -> None:
        tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")
        input_file = Path(self.input_txt_path)

        try:
            with open(input_file, "r") as file:
                text = file.read()
            
            if not text:
                print(f'File {input_file} is empty')
                
        except Exception as e:
            print(f"Error reading file {input_file}: {e}")
            sys.exit(1)

        base_name = Path(self.input_txt_path).stem
        output_file_path = Path(self.output_path) / f"{base_name}.wav"

        try:
            tts.tts_to_file(
                text=text, 
                file_path=output_file_path
            )
            print(f'Text-to-speech WAV file saved at {output_file_path}')
        except Exception as e:
            print(f'Error in text-to-speech: {e}')
            sys.exit(1)

    def get_wav_file(self) -> str:
        txt_file = Path(self.input_txt_path)
        base_name = txt_file.stem
        wav_file = Path(self.output_path) / f"{base_name}.wav"

        if not wav_file.exists():
            print(f'Wav file {wav_file} not found')
            sys.exit(1)

        return wav_file 

    def convert_wav_to_mp3_delete_wav(self) -> None:
        wav_file_path = self.get_wav_file()

        if not wav_file_path.exists():
            print(f'WAV file {wav_file_path} not found.')
            return

        output_mp3_path = wav_file_path.with_suffix(".mp3")

        try:
            sound_file = AudioSegment.from_wav(wav_file_path)
            sound_file.export(output_mp3_path, format="mp3", bitrate="128k")
            print(f'mp3 file written to {output_mp3_path}')
        except Exception as e:
            print(f'Error converting file {wav_file_path} to mp3: {e}')

        if output_mp3_path.exists():
            os.remove(wav_file_path)
            print(f'wav file {wav_file_path} deleted.')
        else:
            print(f'wav file {wav_file_path} not found')
