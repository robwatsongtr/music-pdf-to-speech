from music21 import converter
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
            exit(1)

        self.spoken_letters = {
            "C": "see",
            "D": "dee",
            "E": "Eee",
            "F": "eFF",
            "G": "gee",
            "A": "ayy",
            "B": "bee"
        }

    def spoken_key(self, key: str) -> str:
        """
        Keys without sharps or flats will be len 7, else with accidental len 8
        *Input must be music21 key.name for this to be valid.*
        """
        if not key or len(key) < 7 or len(key) > 8:
            return "unknown key"

        spoken_key_name = ''
        if len(key) == 7:  
            spoken_key_name = self.spoken_letters.get(key[0], key[0]) + ' ' + key[2:]
            return spoken_key_name
        elif len(key) == 8:
            if key[1] == "#":
                spoken_key_name = self.spoken_letters.get(key[0], key[0]) + ' sharp ' + key[3:]
                return spoken_key_name
            elif key[1] == "b":
                spoken_key_name = self.spoken_letters.get(key[0], key[0]) + ' flat ' + key[3:]
                return spoken_key_name
            
    def spoken_note(self, note: str) -> str:
        """
        Notes without sharps or flats will be len 2, else with accidental len 3
        *Input must be music21 note.nameWithOctave for this to be valid*
        """
        if not note or len(note) < 2 or len(note) > 3:
            return "unknown note"

        spoken_note = ''
        if len(note) == 2:
            spoken_note = self.spoken_letters.get(note[0], note[0]) + '  ' + note[1] 
            return spoken_note
        elif len(note) == 3:
            if note[1] == "#":
                spoken_note = self.spoken_letters.get(note[0], note[0]) + '  SHARP  ' + note[2] 
                return spoken_note
            elif note[1] == "b":
                spoken_note = self.spoken_letters.get(note[0], note[0]) + '  FLAT  ' + note[2] 
                return spoken_note

    def extract_staff_attr_start_p1(self) -> None:
        """
        This method extracts the Clef, Key Signature, and Time signature
        from the beginning of the score.
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
            spoken_key_name = self.spoken_key(key_name)
            self.staff_attr.append(f"Key: {spoken_key_name}\n")
        else:
            inferred_key = part.analyze('key')
            inferred_key_name = inferred_key.name
            spoken_inferred_key_name = self.spoken_key(inferred_key_name)
            self.staff_attr.append(f"Key: {spoken_inferred_key_name} as inferred.\n")

        if initial_time:
            self.staff_attr.append(
                f"Time Signature: {initial_time.numerator}  {initial_time.denominator}\n"
            )

        print("Staff attributes extracted.")

    def extract_measure_data_single_voice_p1(self) -> None:
        """
        Extracts the notes and rests from every measure of the score.
        Basic: one voice and one part. 
        """
        part = self.score.parts[0]

        for measure in part.getElementsByClass('Measure'):
            measure_num = measure.number
            if measure_num == 0:
                measure_label = str('Pickup')
            else:
                measure_label = str(measure_num)
            self.measure_data.append(f"Measure: {measure_label}\n")

            for element in measure.notesAndRests:
                beat = element.beat
                if element.isNote:
                    note = element.nameWithOctave
                    spoken_note = self.spoken_note(note)
                    note_dur = element.duration.fullName + ' note.'
                    if element.tie:
                        tie_type = element.tie.type
                        tie_info = f",  Tie: {tie_type}."
                    else:
                        tie_info = ""
                    self.measure_data.append(
                        f"Beat {beat}, {spoken_note}, {note_dur}{tie_info}\n"
                    )
                elif element.isRest:
                    rest_dur = element.duration.fullName
                    self.measure_data.append(f"  Rest:  {rest_dur}\n")

            self.measure_data.append('\n')
        
        print("Measure, note and rest data extracted")

    def write_to_txt(self) -> None:
        """
        Writes the staff attribe and measure contents into a text file. 
        """
        base_name = Path(self.input_xml_path).stem
        output_file_path = Path(self.output_path) / f"{base_name}.txt"

        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.writelines(self.staff_attr)
                file.write('\n')
                file.writelines(self.measure_data)

            print(f'Text File written to {output_file_path}')
        except Exception as e:
            print(f'Error writing file: {e}')
    
    def get_txt_file(self) -> str:
        """
        Returns full path to written text file.
        """
        xml_file = Path(self.input_xml_path)
        base_name = xml_file.stem
        txt_file = Path(self.output_path) / f"{base_name}.txt"

        return txt_file 