

class TTS:
    """
    This class will take the text analysis of the MusicXML file,
    Using text to speech to output an audio file.
    """
    def __init__(self, output_path: str, input_txt_path: str):
        self.input_txt_path = input_txt_path
        self.output_path = output_path