# music-pdf-to-speech

Converts a PDF of a musical score into an audio file that narrates the musical elements, by 
way of OMR (Optical Music Recognition), Music21 analysis of MusicXML, and text-to-speech.

Requires Python 3.11.x for Coqui TTS. 

## Installation:

Make sure Python 3.11x is installed. 

Clone repo.

Create a Python 3.11 virtual environment in the project directory:  
% python3.11 -m venv your-venv-name

Activate environment: 
% source venv/bin/activate  or Windows:  venv\Scripts\activate

Install Dependencies:  
% pip install -r requirements.txt

## Running the Pipeline:

cd to src 

Syntax:

python3 main.py path/to/pdf midi_instrument   (Piano, Marimba, Guitar for midi_instrument)

The purpose of choosing an instrument is that the output of Audiveris always seems to 
default to Voice 'ooos' for Part 1 of the MusicXML, so my code changes that. For now I give a few 
other General MIDI choices that have a more distinct attack, which I like. 

Example:

python3 main.py ../score_processing/pdf/OnTopOfOldSmoky.pdf Marimba

## Technical Notes:

The full source for Audiveris is included. I tried to include it as a git submodule,
but that process was so painful I abandoned it. If you want, feel free to fork and try,
it would enable tracking of the latest updates. As it stands, this project has Version 5.6.0

Getting the CLI interface for Audiveris to work was quite challenging, but I managed to figure
it out. It involves running the .jar with a classpath that, to the best of my knowlege,
isn't documented. The GUI of Audiveris can still be run with Gradle ( ie  ./gradlew run ).
That being said, I am not trying to be overly critical, and I undertand that Audiveris 
is generally run as a GUI and it works great, especially in cleaning up the OMR output.

The fruit of that labor is in the shell script in the root of the project directory.
Note that the code there that involves unarchiving isn't really necessary since that's already
been done, but if you go the route of including Audiveris as a submodule, on first run you will
need to unarchive the binary in order to run the shell script command.
 
---

## Credits

This project includes **Audiveris**, an open-source Optical Music Recognition (OMR) software.

- Audiveris repository: [https://github.com/Audiveris/audiveris](https://github.com/Audiveris/audiveris)
- Audiveris Author: Hervé Bitteur and contributors

We thank the Audiveris team for their outstanding work and for making the project available 
under the GNU GPL v3 license.

Thanks to MIT for the fantastic Music21 library for analysis.

---

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the
LICENSE file for detials. 
