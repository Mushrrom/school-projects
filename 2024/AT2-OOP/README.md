# MusicXML reader program

This is a program that has been constructed to read musicxml files.

Currently this program is only able to read the older format of musicXML (files ending in .musicxml or .xml) due to the newer .mxml file being compressed in order to save space

If you want to test this with your own MusicXML files you can export MusicXML from musescore by selecting File>Export>format: "MusicXML">file type: "uncompressed (*.musicxml)"

The main included function is the song.print_mathematica(), which is a demonstration of the capibilities of this program, and can print the code to play the song in mathematica. to play it, place the printed code inside of `Sound[{  }]` (inside the curly braces) in mathematica, and then it can play the song (will play every instrument as piano unfortunatley)

the main.py file includes some example uses, however much more is possible with the various attributes each

## Dependencies
The xmltodict library, by Martín Blech is required for this program, this library is useful as it allows the XML files to be read by python as a dictionary, which is much easier for scripting. It can be installed with `pip install xmltodict`.

## For my teachers
I have included some example MusicXML files that I have been using to test the program in the test_files directory, these were not created or scored by me, and are the intelecual property of their individual creators.
