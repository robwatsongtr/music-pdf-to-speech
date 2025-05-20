from omr import OMR

if __name__ == "__main__":
    espanoleta_score = '../score_processing/pdf/Espanoleta.pdf'
    sor_b_min_study_score = '../score_processing/pdf/SorBminStudyOp35no22.pdf'

    output_path = '../score_processing/MusicXML'

    pdf_to_xml1 = OMR(output_path)
    pdf_to_xml1.run_audiveris(espanoleta_score)
    pdf_to_xml1.unzip_mxl()

