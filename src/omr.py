"""
This script will perform optical music recognition on a pdf using audiveris, then
Output to MusicXML 
"""
# ./audiveris-cli.sh -batch -export -output data data/Pachelbels-Canon.pdf

import subprocess

class OMR:
    def __init__(self, input_pdf_path: str, output_dir: str):
        self.input_pdf_path = input_pdf_path
        self.output_dir = output_dir

    def run_audiveris(self) -> None:
        script_path = "../audiveris-cli.sh"
        cmd = [
            script_path, 
            "-batch", 
            "-export", 
            "-output", self.output_dir,
            self.input_pdf_path
        ]

        try:
            subprocess.run(cmd, check=True)
            print("Audiveris processing completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Audiveris failed with exit code {e.returncode}")

