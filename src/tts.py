from TTS.api import TTS
from pathlib import Path

class TextToSpeech:
    """
    This class will take the text analysis of the MusicXML file,
    Then using Coqui TTS output a wav file. 
    """
    def __init__(self, output_path: str, input_txt_path: str):
        self.input_txt_path = input_txt_path
        self.output_path = output_path

    def output_tts(self) -> None:
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        input_file = Path(self.input_txt_path)

        try:
            with open(input_file, "r") as file:
                text = file.read()
            
            if not text:
                print(f'File {input_file} is empty')
                
        except Exception as e:
            print(f"Error reading file {input_file}: {e}")
            exit(1)

        base_name = Path(self.input_txt_path).stem
        output_file_path = Path(self.output_path) / f"{base_name}.wav"

        try:
            tts.tts_to_file(text=text, file_path=output_file_path)

            print(f'Text-to-speech WAV file saved at {output_file_path}')
        except Exception as e:
            print(f'Unexpected error in tts: {e}')
            exit(1)


