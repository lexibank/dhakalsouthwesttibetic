from lingpy import *
from lingpy.sequence.sound_classes import syllabify
from lingpy.compare.partial import Partial
from lingrex.cognates import common_morpheme_cognates

def run(wordlist):
    wordlist.add_entries("tokens", "tokens", lambda x: syllabify(x),
            override=True)
    part = Partial(wordlist)
    part.get_partial_scorer(runs=10000)
    part.partial_cluster(method="lexstat", threshold=0.45, ref="cogids")
    common_morpheme_cognates(
            part,
            cognates="cogids",
            ref="cogid",
            morphemes="morphemes")
    
    alms = Alignments(part, ref="cogids")
    alms.align()
    D = {0: ["doculect", "concept", "value", "form", "tokens", "cogids",
        "morphemes",
        "cogid", "alignment"]}
    for idx in alms:
        D[idx] = [alms[idx, h] for h in D[0]]
    return D
