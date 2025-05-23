from music21 import converter
import subprocess
from pathlib import Path
from music21.exceptions21 import Music21Exception
import sys

class Playback:
    """
    This class will convert MusicXML files to midi files for playback, and will
    also perform playback of the MIDI files. 
    """
    def __init__(self, input_xml_path: str, output_path: str):
        self.input_xml_path = input_xml_path
        self.midi_output_path = output_path
        self.midi_file_path = ""

    def convert_mxml_to_MIDI(self):
        """
        Convert MusicXML to a MIDI file using music21
        """
        try:
            print(f"Converting MusicXML: {self.input_xml_path}")
            mxml_file = converter.parse(self.input_xml_path)
            
            input_path = Path(self.input_xml_path)
            output_directory = Path(self.midi_output_path)
            file_name = input_path.with_suffix(".mid").name 
            self.midi_file_path = output_directory / file_name

            print(f"Writing MIDI: {self.midi_file_path}")
            mxml_file.write("midi", fp=str(self.midi_file_path))
        except Music21Exception as e:
            print("music21 failed to parse or write:", e)
   
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 playback.py path/to/file.xml")
        sys.exit(1)

    path_to_xml = sys.argv[1]
    
    # run just MusicXML to MIDI converter 
    # ../score_processing/MusicXML/Espanoleta.xml
    output_path = '../score_processing/MIDI'
    xml_to_midi = Playback(path_to_xml, output_path)
    xml_to_midi.convert_mxml_to_MIDI()

    
   


    