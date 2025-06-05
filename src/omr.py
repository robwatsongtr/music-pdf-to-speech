import subprocess
import os 
from pathlib import Path
import shutil
from lxml import etree
import sys

class OMR:
    """
    This class will perform Optical Music Recognition on a PDF score 
    using Audiveris, Then output to MusicXML file, while cleaning
    up extraneous files and folders. 
    """
    def __init__(self, output_path: str, input_pdf_path: str, midi_sound: str):
        self.input_pdf_path = input_pdf_path
        self.output_path = output_path
        self.midi_sound = midi_sound
        self.midi_sound_map = {
            "Piano" : "0",
            "Guitar" : "25",
            "Marimba" : "12"
        }

    def run_audiveris(self) -> None:
        """
        Run Audiveris CLI to convert a PDF score into a MusicXML file.
        """
        script_path = "../audiveris-cli.sh"
        cmd = [
            script_path, 
            "-batch", 
            "-export", 
            "-output", self.output_path,
            self.input_pdf_path
        ]
        try:
            subprocess.run(cmd, check=True)
            print("Audiveris processing completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Audiveris failed with exit code {e.returncode}")
            sys.exit(1)

    def unzip_mxls(self) -> None:
        """
        Unzip the resulting .mxl file(s)
        """
        output_path = Path(self.output_path)
        mxl_files = output_path.glob("*.mxl")

        for mxl_file in mxl_files:
            try:
                subprocess.run(
                    ["unzip", "-o", mxl_file, "-d", str(output_path)], check=True
                )
                print(f"{mxl_file} unzipped successfully")
            except subprocess.CalledProcessError as e:
                print(f"unzip failed with exit code {e.returncode}")
    
    def check_for_xml_file(self) -> bool:
        directory = Path(self.output_path)

        return any(directory.glob("*.xml"))

    def delete_files_metafolder(self) -> None:
        """
        Delete non .xml files and 'META-INF' folder, keep log file  
        (Produced by Audioveris and The unzipping of the .mxl file(s))
        """
        directory = Path(self.output_path)
        extensions = {'.mxl', '.omr'}

        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix in extensions:
                print(f"Deleting {file_path}")
                os.remove(file_path)
                
        dir_to_delete = directory / 'META-INF'
        if dir_to_delete.exists() and dir_to_delete.is_dir():
            print("Deleting META-INF directory")
            shutil.rmtree(dir_to_delete)

        if not self.check_for_xml_file():
            print("OMR FAILED: No .xml file produced. Check Logs.")
            sys.exit(1)
        else:
            print("OMR Succeeded!")

    def get_xml_file(self) -> str:
        """
        Returns full path to MusicXML file after OMR.
        """
        original_file = Path(self.input_pdf_path)
        base_name = original_file.stem
        xml_file = Path(self.output_path) / f"{base_name}.xml"

        if not xml_file.exists():
            print(f'XML file not found: {xml_file}')
            print('This is likely due to Audiveris producing multiple .mvt.xml files')
            print('Multiple xml file concatenation not currently supported.\n')
            sys.exit(1)

        return xml_file

    def strip_chords(self) -> None:
        """
        If MusicXML file has chords above staff, remove them
        ie, it strips <harmony> tags. These get played in playback. 
        """
        xml_to_process = self.get_xml_file()

        try:
            tree = etree.parse(xml_to_process)
        except etree.XMLSyntaxError as e:
            print(f"Failed to parse XML: {e}")
            return

        root = tree.getroot()
        tag_to_remove = 'harmony'
        for elem in root.xpath('.//' + tag_to_remove):
            parent = elem.getparent()
            if parent is not None:
                parent.remove(elem)

        try:
            tree.write(
                xml_to_process,
                pretty_print=True,
                xml_declaration=True,
                encoding='UTF-8'
            )

            print('Chords Stripped.')
        except Exception as e:
            print(f'Error writing xml file: {e}')

        

    def change_part_1_sound(self) -> None:
        """
        In MusicXML file: 
        Changes Part 1 part name, part abbreviation, score instrument name,
        midi instrument program to what is stored in self.midi_sound
        """
        xml_to_process = self.get_xml_file()

        try:
            tree = etree.parse(xml_to_process)
        except etree.XMLSyntaxError as e:
            print(f"Failed to parse XML: {e}")
            return
        
        root = tree.getroot()
        score_part_1 = root.xpath('.//score-part[@id="P1"]')[0]

        part_name_element = score_part_1.find('part-name')
        part_abbrev_element = score_part_1.find('part-abbreviation')
        instrument_name_element = score_part_1.find('.//instrument-name')
        midi_program_element = score_part_1.find('.//midi-program')

        if part_name_element is not None:
            part_name_element.text = self.midi_sound

        if part_abbrev_element is not None:
            part_abbrev_element.text = self.midi_sound 
            
        if instrument_name_element is not None:
            if self.midi_sound == 'Piano':
                instrument_name_element.text = "Acoustic Grand Piano"
            elif self.midi_sound == 'Guitar':
                instrument_name_element.text = "Acoustic Guitar Steel"
            elif self.midi_sound == 'Marimba':
                instrument_name_element.text = "Marimba"

        if midi_program_element is not None:
            midi_program_element.text = self.midi_sound_map.get(self.midi_sound)
    
        try:
            tree.write(
                xml_to_process,
                pretty_print=True,
                xml_declaration=True,
                encoding='UTF-8'
            )

            print(f'Part 1 Sound changed to {self.midi_sound}')
        except Exception as e:
            print(f'Error writing xml file: {e}')

        
            