from music21 import converter
import subprocess
from pathlib import Path
from music21.exceptions21 import Music21Exception


class Playback:
    """
    This class will convert MusicXML files to midi files for playback, and will
    also perform playback of the MIDI files. 
    """
    def __init__(self, input_xml_path: str, output_path: str):
        self.input_xml_path = input_xml_path
        self.output_path = output_path

    def convert_mxml_to_MIDI(self):
        """
        Convert MusicXML to a MIDI file using music21
        """
        try:
            print(f"Converting MusicXML: {self.input_xml_path}")
            mxml_file = converter.parse(self.input_xml_path)
            
            midi_output_path = Path(self.input_xml_path).with_suffix(".mid")
            print(f"Writing MIDI: {midi_output_path}")
            mxml_file.write("midi", fp=str(midi_output_path))
        except Music21Exception as e:
            print("music21 failed to parse or write:", e)

    

    