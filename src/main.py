from omr import OMR

if __name__ == "__main__":
    pachelbel = '../score_processing/pdf/Pachelbels-Canon.pdf'

    output_path = '../score_processing/MusicXML'

    # test = OMR(output_path)
    # test.run_audiveris()

    pdf_to_xml1 = OMR(output_path)
    pdf_to_xml1.run_audiveris(pachelbel)

