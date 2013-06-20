import os

from music21 import converter

PATH = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))


class SongObject(object):
    def __init__(self, artist=None, title=None, directory='assets/midi', *args, **kwargs):
        self.artist = artist
        self.title = title
        self.directory = directory

    @property
    def corpus(self):
        return self._corpus

    @corpus.setter
    def corpus(self, m_objs):
        self._corpus = self.musicobjs(m_objs)

    def musicobjs(self, m_objs):
        return filter(None, [MusicObject(m_obj).items() for m_obj in m_objs])


class MidiObject(SongObject):
    @property
    def file_name(self):
        return "%s/%s.mid" % (self.artist, self.title)

    @property
    def file_location(self):
        return "%s/%s" % (self.directory, self.file_name)

    def from_midi(self):
        """Generate a list of music21 objects out of a MIDI file"""
        music_stream = converter.parse(PATH(self.file_location))
        return music_stream.recurse()


class Node(object):
    def __init__(self, node, *args, **kwargs):
        self.node = node


class Note(Node):
    @property
    def duration(self):
        return self.node.duration.type

    @property
    def octave(self):
        return self.node.pitch.octave

    @property
    def name(self):
        return self.node.name

    @property
    def pitch(self):
        return self.node.pitch.name

    @property
    def midi(self):
        return self.node.pitch.midi

    def __getstate__(self):
        d = self.__dict__.copy()
        print "D ARE ", d
        del d['__weakref__']
        return d


class Rest(Node):
    @property
    def name(self):
        # Markov requires a string
        return str(self.node.quarterLength)


class MusicObject(Node):
    @property
    def root(self):
        return self.node.__class__.__name__

    def items(self):
        cls_map = {
            'Note': Note,
            'Rest': Rest,
        }

        try:
            cls = cls_map[self.root]
        except KeyError:
            return

        return cls(self.node)
