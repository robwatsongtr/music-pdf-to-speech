from music21 import converter, note, chord

class Analyzer:
    """
    This class takes a MuiscXML file and extracts / parses out human readable information
    And will output a text file 
    """
    def __init__(self, input_xml_path: str, output_path: str):
        self.input_xml_path = input_xml_path
        self.output_path = output_path