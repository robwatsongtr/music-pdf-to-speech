from music21 import converter, note, chord, converter
from pathlib import Path

class Analyzer:
    """
    This class takes a MusicXML file and extracts / parses out human readable information
    And will output a text file 
    """
    def __init__(self, output_path: str, input_xml_path: str):
        self.input_xml_path = input_xml_path
        self.output_path = output_path
        self.staff_attr = []
        self.measure_data = []

    def extract_staff_attr_start(self) -> None:
        score = converter.parse(self.input_xml_path)
        part = score.parts[0]

        clef = part.recurse().getElementsByClass('Clef')
        initial_clef = clef[0] if clef else None

        initial_key_sig = part.recurse().getElementsByClass('KeySignature')

        time = part.recurse().getElementsByClass('TimeSignature')
        initial_time = time[0] if time else None 

        if initial_clef:
            self.staff_attr.append(f"Clef: {initial_clef.name}\n")
        
        if initial_key_sig:
            key_sig = initial_key_sig[0]
            key_name = key_sig.asKey().name
            self.staff_attr.append(f"Key: {key_name}\n")
        else:
            inferred_key = part.analyze('key')
            self.staff_attr.append(f"Key: {inferred_key.name} as inferred.\n")

        if initial_time:
            self.staff_attr.append(f"Time Signature: {initial_time.ratioString}\n")

        print("Staff attributes extracted.")

    def write_to_txt(self) -> None:
        base_name = Path(self.input_xml_path).stem
        output_file_path = Path(self.output_path) / f"{base_name}.txt"

        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(base_name + '\n\n')
                file.writelines(self.staff_attr)
        except Exception as e:
            print(f'Error writing file: {e}')
    
        print(f'Text File written to {output_file_path}')