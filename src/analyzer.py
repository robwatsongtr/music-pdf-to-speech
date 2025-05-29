from music21 import note, chord, converter, stream
from pathlib import Path

class Analyzer:
    """
    This class takes a MusicXML file and extracts human readable information
    Outputs a text file 
    """
    def __init__(self, output_path: str, input_xml_path: str):
        self.input_xml_path = input_xml_path
        self.output_path = output_path
        self.staff_attr = []
        self.measure_data = []
        try:
            self.score = converter.parse(self.input_xml_path)
        except Exception as e:
            print(f"Failed to parse '{input_xml_path}' with error: {e}")

    def extract_staff_attr_start_p1(self) -> None:
        """
        This method uses Music 21 to extract the Clef, Key Signature, and 
        Time signature from the beginning of the score.
        """
        part = self.score.parts[0]

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

    def extract_measure_data_single_voice_p1(self) -> None:
        """
        Extracts the notes and rests from every measure of the score.
        Basic: one voice and one part. 
        """
        part = self.score.parts[0]

        for measure in part.getElementsByClass('Measure'):
            self.measure_data.append(f"Measure: {measure.number}\n")
            for element in measure.notesAndRests:
                beat = element.beat
                if element.isNote:
                    note = element.nameWithOctave
                    note_duration = element.duration.fullName
                    if element.tie:
                        tie_type = element.tie.type
                        tie_info = f", Tie: {tie_type}"
                    else:
                        tie_info = ""
                    self.measure_data.append(
                    f"  Beat: {beat}, Note: {note}, Duration: {note_duration}{tie_info}\n"
                    )
                elif element.isRest:
                    rest_duration = element.duration.fullName
                    self.measure_data.append(f"  Rest: Duration: {rest_duration}\n\n")
        
        print("Measure, note and rest data extracted")

    def write_to_txt(self) -> None:
        """
        Writes the staff attribe and measure contents into a text file. 
        """
        base_name = Path(self.input_xml_path).stem
        output_file_path = Path(self.output_path) / f"{base_name}.txt"

        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(base_name + '\n\n')
                file.writelines(self.staff_attr)
                file.write('\n')
                file.writelines(self.measure_data)
        except Exception as e:
            print(f'Error writing file: {e}')
    
        print(f'Text File written to {output_file_path}')