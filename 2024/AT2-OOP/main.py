from musicXML_reader import song

# You can set this to whatever musicXML file you have
mySong = song("./test_files/duvet.boa.xml")


# Some example uses
print(f"song tempo: {mySong.tempo}")
print(f"Bars in song: {mySong.totalBars}")
print(f"First note of first bar of first instrument: {mySong.parts[0].bars[0].notes[0].notes_list()}")
print(f"Is the first note of first bar of first instrument a chord: {mySong.parts[0].bars[0].notes[0].isChord}")

# Uncomment this to print the mathematica
mySong.print_mathematica()