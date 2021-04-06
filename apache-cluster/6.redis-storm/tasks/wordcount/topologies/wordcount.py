"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.wordcount import RedisWordCountBolt
from spouts.words import WordSpout


class WordCount(Topology):
    word_spout = WordSpout.spec()
    count_bolt = RedisWordCountBolt.spec(
        inputs = {word_spout: Grouping.fields('word')}, par = 2
    )
