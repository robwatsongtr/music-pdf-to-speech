import subprocess
import glob
import os 

"""
This class will perform optical music recognition on a pdf using Audiveris, then
Output to MusicXML 
"""
# ./audiveris-cli.sh -batch -export -output data data/Pachelbels-Canon.pdf

class OMR:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def run_audiveris(self, input_pdf_path: str = None) -> None:
        script_path = "../audiveris-cli.sh"
        # cmd_test = [ script_path, "-help" ]
        cmd = [
            script_path, 
            "-batch", 
            "-export", 
            "-output", self.output_dir,
            input_pdf_path
        ]

        try:
            subprocess.run(cmd, check=True)
            print("Audiveris processing completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Audiveris failed with exit code {e.returncode}")

    def unzip_mxl(self):
        mxl_files = glob.glob(os.path.join(self.output_dir, "*.mxl"))
        
        for mxl_file in mxl_files:
            try:
                subprocess.run(["unzip", "-o", mxl_file, "-d", self.output_dir], check=True)
                print(f"{mxl_file} unzipped successfully")
            except subprocess.CalledProcessError as e:
                print(f"unzip failed with exit code {e.returncode}")

        
