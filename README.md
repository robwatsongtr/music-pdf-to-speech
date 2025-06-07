# music-pdf-to-speech

Converts a bitmap PDF or any other bitmap format of a musical score into an audio file that narrates 
the musical elements, by way of OMR (Optical Music Recognition), Music21 analysis of MusicXML, 
and text-to-speech.

Requires Python 3.11.x for Coqui TTS and Java for Audiveris.  

## Installation:

Make sure Python 3.11x is installed. If not, install it. 

% brew install python@3.11

Make sure Java is installed:

% java -version

If not, you can install it with:

% brew install temurin 

Clone repo and cd into repo.  

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

## Notes:

The full source for Audiveris (OMR app) is included. I tried to include it as a git submodule,
but that process was so painful I abandoned it. If you want, feel free to fork and try,
it would enable tracking of the latest updates. As it stands, this project has Version 5.6.0.
Audiveris is unique in that it is all in Java, not Python. 

Getting the CLI interface for Audiveris to work was quite challenging. It involves running a 
classpath that, to the best of my knowlege, isn't documented. The GUI of Audiveris can still 
be run with Gradle ( ie  ./gradlew run ). 

The fruit of that labor is in the shell script in the root of the project directory.
Note that the code there that involves unarchiving isn't really necessary since that's already
been done, but if you go the route of including Audiveris as a submodule, on first run you will
need to unarchive the binary in order to run the shell script command.

Optical Music Recognition is imprecise, you need a clean, aligned, well spaced score. 
There are examples that seem to work out of the box, but often there will be errors. 
Erros can be fixed in the Audiveris GUI or in a program like MuseScore. Sometimes Audiveris 
will produce a multi file xml output, currently the code does not concatenate these so the pipeline
will stop after Audiveris. 

Currently my parsing algorithm can only handle one-part non-contrapuntal (single voice) scores. 
Contrapuntal detection will come, hopefully soon, as the initial impetus for this project was to 
help a classical guitar student who is in the process of losing his sight, and classical guitar music 
is generally contrapuntal. Multi-part might be added as well, but contrapuntal first. 

Text-to-speech libraries have a harder time dealing with speaking single letters like "C";
screen readers do this better. The work-around is to spell spoken letters phonetically.

Questions or ideas,

Email me at: [rwatso [at] gmail [dot] com](mailto:rwatso@gmail.com)
 
---

## Credits

This project includes **Audiveris**, an open-source Optical Music Recognition (OMR) software.

- Audiveris repository: [https://github.com/Audiveris/audiveris](https://github.com/Audiveris/audiveris)
- Audiveris Author: Hervé Bitteur and contributors

Thanks to MIT for the fantastic Music21 library for analysis.

---

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the
LICENSE file for detials. 
