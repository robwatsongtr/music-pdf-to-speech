from omr import OMR
import sys 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py path/to/file.pdf")
        sys.exit(1)

    path_to_pdf = sys.argv[1]
    
    # run just OMR 
    output_path = '../score_processing/MusicXML'
    pdf_to_xml = OMR(path_to_pdf, output_path)
    pdf_to_xml.run_audiveris()
    pdf_to_xml.unzip_mxls()
    pdf_to_xml.delete_files_metafolder()
