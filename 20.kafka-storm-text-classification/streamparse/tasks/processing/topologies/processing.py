"""
processing topology
"""

from streamparse import Grouping, Topology

from bolts.processing import ProcessingBolt
from spouts.consumer import ConsumerSpout


class Processing(Topology):
    consumer_spout = ConsumerSpout.spec(par = 5)
    processing_bolt = ProcessingBolt.spec(
        inputs = {consumer_spout: Grouping.fields('sentences')}, par = 5
    )
