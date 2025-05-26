from omr import OMR
from playback import Playback

import sys 

if __name__ == "__main__":

    valid_sounds = ['Piano', 'Guitar', 'Marimba']
    output_path_hardcode = '../score_processing/MusicXML'

    if len(sys.argv) < 3:
        print("Usage: python3 main.py path/to/file.pdf sound")
        print(f"Sound options: {', '.join(valid_sounds)}")
        sys.exit(1)

    path_to_pdf = sys.argv[1]
    midi_sound = sys.argv[2]

    if midi_sound not in valid_sounds:
        print(f'Error: {midi_sound} not a valid sound.')
        print(f'Valid sounds are: {', '.join(valid_sounds)}')
        sys.exit(1)

    # run just OMR 
    pdf_to_xml = OMR(output_path_hardcode, path_to_pdf, midi_sound)
    pdf_to_xml.run_audiveris()
    pdf_to_xml.unzip_mxls()
    pdf_to_xml.delete_files_metafolder()
    pdf_to_xml.strip_chords()
    pdf_to_xml.change_part_1_sound()
