

class TTS:
    """
    This class will take the output of the MusicXML parser and use
    Text to speech to output a final audio file that talks through the score 
    """
    def __init__(self, output_path: str, input_txt_path: str):
        self.input_txt_path = input_txt_path
        self.output_path = output_path