from omr import OMR
from analyzer import Analyzer
from tts import TextToSpeech
# from playback import Playback

import sys 

if __name__ == "__main__":

    valid_sounds = ['Piano', 'Guitar', 'Marimba']
    
    if len(sys.argv) < 3:
        print("Usage: python3 main.py path/to/file.pdf sound")
        print(f"Sound options: {', '.join(valid_sounds)}")
        sys.exit(1)

    path_to_pdf = sys.argv[1]
    midi_sound = sys.argv[2]

    if midi_sound not in valid_sounds:
        print(f'Error: {midi_sound} not a valid sound.')
        print(f"Valid sounds are: {', '.join(valid_sounds)}")
        sys.exit(1)

    # 1) OMR (Optical Music Recognition)
    output_path_xml = '../score_processing/MusicXML'
    pdf_to_xml = OMR(output_path_xml, path_to_pdf, midi_sound)
    pdf_to_xml.run_audiveris()
    pdf_to_xml.unzip_mxls()
    pdf_to_xml.delete_files_metafolder()
    pdf_to_xml.strip_chords()
    pdf_to_xml.change_part_1_sound()
    pdf_to_xml_file = pdf_to_xml.get_xml_file()
    print(f"OMR to pdf file path: {pdf_to_xml_file}")

    # 2) Analyze Music XML file and output a text file 
    output_path_txt = '../score_processing/txt_output'
    xml_to_txt = Analyzer(output_path_txt, pdf_to_xml_file)
    xml_to_txt.extract_staff_attr_start_p1()
    xml_to_txt.extract_measure_data_1v_p1()
    xml_to_txt.write_to_txt()
    xml_to_txt_file = xml_to_txt.get_txt_file()
    print(f"XML to text analysis file path: {xml_to_txt_file}")

    # 3) TTS on text file and output to audio 
    output_path_audio = "../score_processing/tts_audio"
    txt_to_tts = TextToSpeech(output_path_audio, xml_to_txt_file)
    txt_to_tts.output_tts()
    

