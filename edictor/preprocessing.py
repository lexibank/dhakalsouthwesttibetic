from lingpy import *
from lingpy.sequence.sound_classes import syllabify
from lingpy.compare.partial import Partial

def run(wordlist):
    wordlist.add_entries("tokens", "tokens", lambda x: syllabify(x),
            override=True)
    part = Partial(wordlist)
    part.partial_cluster(method="sca", threshold=0.45, ref="cogids")
    part.add_cognate_ids("cogids", "cogid", idtype="strict")
    
    alms = Alignments(part, ref="cogids")
    alms.align()
    D = {0: ["doculect", "concept", "value", "form", "tokens", "cogids",
        "cogid", "alignment"]}
    for idx in part:
        D[idx] = [part[idx, h] for h in D[0]]
    return D
