import subprocess
import os 
from pathlib import Path
import shutil

class OMR:
    """
    This class will perform Optical Music Recognition on a PDF using Audiveris, then
    output to MusicXML file, while cleaning up extraneous files and folders. 
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def run_audiveris(self, input_pdf_path: str = None) -> None:
        """
        Run Audiveris CLI to convert a PDF into a MusicXML file.
        """
        script_path = "../audiveris-cli.sh"
        cmd = [
            script_path, 
            "-batch", 
            "-export", 
            "-output", self.output_dir,
            input_pdf_path
        ]

        try:
            subprocess.run(cmd, check=True)
            print("Audiveris processing completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Audiveris failed with exit code {e.returncode}")

    def unzip_mxls(self) -> None:
        """
        Unzip the resulting .mxl file(s)
        """
        output_path = Path(self.output_dir)
        mxl_files = output_path.glob("*.mxl")

        print("--- Unzip .mxl file(s) --- ")
        
        for mxl_file in mxl_files:
            try:
                subprocess.run(["unzip", "-o", mxl_file, "-d", str(output_path)], check=True)
                print(f"{mxl_file} unzipped successfully")
            except subprocess.CalledProcessError as e:
                print(f"unzip failed with exit code {e.returncode}")
    
    def check_for_xml_file(self) -> bool:
        directory = Path(self.output_dir)

        return any(directory.glob("*.xml"))

    def delete_files_metafolder(self) -> None:
        """
        Delete non .xml files and 'META-INF' folder, keep log file  
        (Produced by Audioveris and The unzipping of the .mxl file(s))
        """
        directory = Path(self.output_dir)
        extensions = {'.mxl', '.omr'}

        print("--- Delete non .xml files and folders, keep log --- ")

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
        else:
            print("OMR Succeeded!")
            
