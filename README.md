# Talking Music Score

Converts a PDF of a musical score into an audio file that narrates the musical elements, by way of OMR, Music21 analysis of MusicXML, and text-to-speech.

Requires Python 3.11.x for Coqui TTS. 

# Installation:

Make sure Python 3.11x is installed. 

Clone repo.

Create a virtual environment in the project directory:  % python3 -m venv venv 

Activate environment:  % source venv/bin/activate  or Windows:  venv\Scripts\activate

Install Dependencies:  % pip install -r requirements.txt

# Running the Pipeline:

cd to src 

Syntax:

python3 main.py path/to/pdf midi_instrument   (Piano, Marimba, Guitar for midi_instrument)

Example:

python3 main.py ../score_processing/pdf/OnTopOfOldSmoky.pdf Marimba

---

## Credits

This project includes **Audiveris**, an open-source Optical Music Recognition (OMR) software.

- Audiveris repository: [https://github.com/Audiveris/audiveris](https://github.com/Audiveris/audiveris)
- Audiveris Author: Hervé Bitteur and contributors

We thank the Audiveris team for their outstanding work and for making the project available under the GNU GPL v3 license.

---

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the
LICENSE file for detials. 
