from pathlib import Path
from src.omr import OMR
from src.analyzer import Analyzer
from src.tts import TextToSpeech

BASE_DIR = Path(__file__).resolve().parent    
ROOT_DIR = BASE_DIR.parent                   

UPLOAD_DIR = ROOT_DIR / "score_processing" / "pdf"
XML_DIR = ROOT_DIR / "score_processing" / "MusicXML"
TXT_DIR = ROOT_DIR / "score_processing" / "txt_output"
PROCESSED_DIR = ROOT_DIR / "score_processing" / "tts_audio"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
XML_DIR.mkdir(parents=True, exist_ok=True)
TXT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

midi_sound = 'Piano' # hardcode this for now 

def save_upload(file_data: bytes, file_name: str) -> Path:
    path = UPLOAD_DIR / file_name
    path.write_bytes(file_data) 

    return path

def run_pipeline(input_path: Path) -> Path:
    pdf_to_xml = OMR(XML_DIR, input_path, midi_sound)
    pdf_to_xml.run_audiveris()
    pdf_to_xml.unzip_mxls()
    pdf_to_xml.delete_files_metafolder()
    pdf_to_xml.strip_chords()
    pdf_to_xml.change_part_1_sound()
    pdf_to_xml_file = pdf_to_xml.get_xml_file()
    print(f"OMR to pdf file path: {pdf_to_xml_file}")

    xml_to_txt = Analyzer(TXT_DIR, pdf_to_xml_file)
    xml_to_txt.extract_staff_attr_start_p1()
    xml_to_txt.extract_measure_data_1v_p1()
    xml_to_txt.write_to_txt()
    xml_to_txt_file = xml_to_txt.get_txt_file()
    print(f"XML to text analysis file path: {xml_to_txt_file}")

    txt_to_tts = TextToSpeech(PROCESSED_DIR, xml_to_txt_file)
    txt_to_tts.output_tts()
    mp3_path = txt_to_tts.convert_wav_to_mp3_delete_wav()

    return mp3_path