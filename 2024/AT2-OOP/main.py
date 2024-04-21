import xmltodict
import json


FIFTHS_SHARPS = ["B", "E", 'A', "D", "G", "C", "F"]
FIFTHS_FLATS = ["F", "C", "G", "D", "A", "E", "B"]

# Can use this to overwrite with custom symbols for flats and sharps
FLAT = "Flat"
SHARP = "Sharp"


def getSongBPMPerBar(part):
    """A function to get the bpm of each bar of a song, because musicxml only stores
    bpm changes on the first instrument... im gonna lose my sanity soon

    Args:
        part (dict): the instrument

    Returns:
        _type_: _description_
    """

    bpmList = []
    bpm = 0
    for count, i in enumerate(part["measure"]):
        try:
            # Float is used instead of int for the rare cases where people
            # decide to use a decimal bpm
            bpm = float(i["direction"]["sound"]["@tempo"])


            # secondsPerBeat = 60 / bpm
        except:
            pass

        bpmList.append(bpm)
    return bpmList

def getSongTimeSigPerBar(part):
    """Gets the number of beats in each bar of a song. This is the main reason that
    the program only works for songs in times over 4. this exists for the same
    reason as above

    Args:
        part (dict): the instrument

    Returns:
        _type_: _description_
    """
    timeSigList = []
    beats = 0
    for i in part["measure"]:
        try:  # Deals with time sig changes
            if str(type(i["attributes"])) != "<class 'list'>":
                beats = int(i["attributes"]["time"]["beats"])
            else:
                beats = int(int(i["attributes"][0]["time"]["beats"]))
        except:  # Exception will be caused if it can't get the attributes or the time object
            pass
        timeSigList.append(beats)

    return(timeSigList)


class song:
    def __init__(self, songfile):
        # read song file and get the score of it from the xml
        with open(songfile, "r") as f:
            scoreXML = f.read()
        self.score = xmltodict.parse(scoreXML)["score-partwise"]
        self.parts = []

        # Create the list of parts

        if str(type(self.score["part"])) == "<class 'list'>":  # will be list if multiple parts
            songBPMList = getSongBPMPerBar(self.score["part"][0])
            songTimeSigList = getSongTimeSigPerBar(self.score["part"][0])
            # quit()
            for i in self.score["part"]:
                self.parts.append(part(i, songBPMList, songTimeSigList))

        else:  # otherwise if there is just one add it to index 0
            songBPMList = getSongBPMPerBar(self.score["part"])
            songTimeSigList = getSongTimeSigPerBar(self.score["part"])
            self.parts.append(part(self.score["part"], songBPMList, songTimeSigList))

        # Get the tempo of the first bar (initial tempo of the piece)
        self.tempo = self.parts[0].part["measure"][0]["direction"]["sound"]["@tempo"]

    def print_mathematica(self):
        for i in self.parts:
            i.print_mathematica()


class part:
    def __init__(self, part: dict, songBPMList: list, songTimeSigList: list):
        self.part = part
        self.bars = []

        # divisions = how long a quarter note is
        self.divisions = int(self.part["measure"][0]["attributes"]["divisions"])

        bpm = 0  # musicxml should define the bpm in the first bar
        secondsPerBeat = 0  # useful for calculations. Will be equal to 60/bpm
        currentBeat = 0
        currentTimeSeconds = 0
        for count, i in enumerate(self.part["measure"]):
            # Set up variables that are used for each iteration
            bpm = songBPMList[count]  # bpm of current bar (from bpm list)
            secondsPerBeat = 60/bpm  # how many seconds each beat lasts

            # Key signature stuff
            if "attributes" in i:
                if "key" in i["attributes"]:
                    fifths = int(i["attributes"]["key"]["fifths"])
                    if fifths < 0: # < 0 means key is in flats
                        sharps = False
                        key = FIFTHS_FLATS[:abs(fifths)]
                    else:
                        sharps = True
                        key = FIFTHS_FLATS[:abs(fifths)]

            beatsInBar = songTimeSigList[count]

            self.bars.append(bar(i, bpm, currentBeat, currentTimeSeconds,
                                  key, sharps, self.divisions))



            currentTimeSeconds += secondsPerBeat * beatsInBar
            # print(currentTimeSeconds)

    def print_mathematica(self):
        for i in self.bars:
            i.print_mathematica()

    def getTotalBeats(self) -> int:
        """Gets the total beats in a part (and in the entire song)

        Returns:
            int: the total number of beats in the part
        """

        totalBeats = 0
        for i in self.part["measure"]:
            try:  # Deals with time sig changes
                if str(type(i["attributes"])) != "<class 'list'>":
                    timeSigBeats = int(i["attributes"]["time"]["beats"])
                else:
                    timeSigBeats = int(int(i["attributes"][0]["time"]["beats"]))

            except:
                pass
            totalBeats += timeSigBeats

        return totalBeats


class bar:
    def __init__(self, bar: dict, bpm: float, currentBeat: int, currentTimeSeconds: float,
                  key: list, sharps: bool, divisions: int):
        """A bar element

        Args:
            bar (dict): The json object of the bar
            bpm (float): the bpm of the piece
            currentBeat (int): the current beat the song is on
            currentTimeSeconds (float): the current amount of seconds into the piece we are
            secondsPerBeat (float): amount of seconds per beat
            key (list): the key as a list of the notes to apply a sharp/flat to
            sharps (bool): whether the key sig is in sharps or flats
        """
        self.bar = bar

        secondsPerBeat = 60/bpm  # How many seconds each beat (quarter note) lasts for
        # print(f"!!!!!!!!!secondsPerBeat: {secondsPerBeat}")

        notes = bar["note"]
        # This handles when there is only one note in the bar (happens if there
        # is a bar rest or something). There should never be an occurence where
        # there is nothing in the bar, as rests occur in blank bars
        if str(type(notes)) == "<class 'dict'>":
            notes = [notes]

        self.notes = []
        staff = 1

        i = 0
        relTimeSeconds = 0
        while i < len(notes):
            if "staff" in notes[i]:
                if not notes[i]["staff"] == staff:
                    # print("staff change")
                    staff = notes[i]["staff"]
                    relTimeSeconds = 0

            noteList = []

            # the note duration in musicXML just uses division units - basically
            # 4 is a quarter note/crotchet, 8 is an eighth note, 2 is a half note,
            # etc (basically just the fraction of the bar)
            noteLength = int(notes[i]["duration"])

            # Deal with a funny thing for 2/4 time (in my testing this didn't occur
            # in 3/4 time)

            noteLengthSeconds = (noteLength/divisions) * secondsPerBeat

            # the notelist works as a list of notes, each note being [note name, note octave]

            first = True  # track whether its the first time running the loop
            while True and i <len(notes):
                if not "chord" in notes[i] and not first:
                    break
                if "staff" in notes[i]:  # Deal with a bug where chords get recognised across staffs
                    if not notes[i]["staff"] == staff:
                        break

                first = False
                if "pitch" in notes[i]:  # if pitch isnt there its a rest
                    noteName = notes[i]["pitch"]["step"]
                    noteOctave = notes[i]["pitch"]["octave"]

                    if "accidental" in notes[i]:
                        if notes[i]["accidental"] != "natural":
                            accidental = notes[i]["accidental"][0].upper() + notes[i]["accidental"][1:]
                            noteName += accidental
                    elif noteName in key:
                        if sharps:
                            noteName += SHARP
                        else:
                            noteName += FLAT
                    noteList.append([noteName, noteOctave])
                i += 1

            # print(f"current tie secomeds: {currentTimeSeconds}")
            noteTimeSeconds = relTimeSeconds + currentTimeSeconds
            # print(f"note time seconds: {noteTimeSeconds}")
            # print(f"rel time seconds: {relTimeSeconds}")
            if not len(noteList) == 0:
                self.notes.append(note(noteList, noteTimeSeconds, noteLengthSeconds))

            relTimeSeconds += noteLengthSeconds

    def print_mathematica(self):
        for i in self.notes:
            i.print_mathematica()



class note:
    def __init__(self, noteList: list, startSeconds: float, duration: float):
        """an object for a note

        Args:
            noteList (list): a list of notes, in the format of [[note, octave]]
            startSeconds (float): the time in seconds when the note starts playing
            duration (float): the duration of the note in seconds
        """
        if len(noteList) == 1:
            self.isChord = False
            self.singleNote = noteList[0]  # singleNote is available as an alternative for scripting
        else:
            self.isChord = True
            self.singleNote = None


        self.notes = noteList
        self.startSeconds = startSeconds
        # print(self.startSeconds)
        self.duration = duration
        self.endSeconds = self.startSeconds+duration

        # print(self.notes)

    def print_mathematica(self):
        """Print the mathematica code for a note
        """
        try:
            print(f"SoundNote[{{{self.notes_string('"', '","', '"')}}}, {{{self.startSeconds}, {self.endSeconds}}}],")
        except:
            pass

    def notes_list(self):
        notes = []
        for i in self.notes:
            notes.append(i[0]+str(i[1]))

        return notes

    def notes_string(self, startString: str = "", splitString: str = "", endString: str = ""):
        notes = "" + startString
        # print(self.notes)
        for count, i in enumerate(self.notes):
            if not count == 0:
                notes += splitString
            notes += i[0]+i[1]

        notes += endString
        # print(notes)
        return notes


# -------------- testing ------------------
songTest = song("prologue.xml")

# songTest = song("prologue.xml")
# print(songTest.parts[0].getTotalBeats())
songTest.print_mathematica()
# print(print(json.dumps(songTest.parts[0].bars[23].bar, indent=4)))
