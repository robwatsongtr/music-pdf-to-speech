

class Playback:
    """
    This class will convert MusicXML files to midi files for playback, and will
    also perform playback of the MIDI files. 
    """
    def __init__(self, input_xml_path: str, output_dir: str):
        self.input_xml_path = input_xml_path
        self.output_dir = output_dir

    