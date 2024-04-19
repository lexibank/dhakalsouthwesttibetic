from pylotiger import (
        get_set_partitions, corrected_pas,
        get_rates
        )
from pylodata.wordlist import get_multistate_patterns

from lingpy import *
from collections import defaultdict
from phylogemetric.delta import DeltaScoreMetric
from phylogemetric.qresidual import QResidualMetric

from tabulate import tabulate

def get_matrix(taxa, patterns):
    """
    Retrieve matrix for delta scores.
    """
    matrix = {t: [] for t in taxa}
    for p, v in patterns.items():
        charset = []
        for val in v.values():
            charset += val
        charset = list(set(charset))
        converter = {}
        for char, new_val in zip(charset, 
                                 "abcdefghijklmnopqrstuvwxyz"):
            converter[char] = new_val

        for taxon in taxa:
            matrix[taxon] += [converter[v[taxon][0]] if v[taxon] else "-"]
    return matrix


wl1 = Wordlist("../wordlists/full-wordlist.tsv")
wl2 = Wordlist("../wordlists/base-wordlist.tsv")

patterns1, _ = get_multistate_patterns(wl1, ref="cogid")
set_partitions1 = get_set_partitions(patterns1, wl1.cols)
rates_a1 = get_rates(set_partitions1)
rates_b1 = get_rates(set_partitions1, partition_func=corrected_pas,
                    partition_kw={"taxlen": wl1.width})
delta1 = DeltaScoreMetric(matrix=get_matrix(wl1.cols, patterns1)).score()
qres1 = QResidualMetric(matrix=get_matrix(wl1.cols, patterns1)).score()

patterns2, _ = get_multistate_patterns(wl2, ref="cogid")
set_partitions2 = get_set_partitions(patterns2, wl2.cols)
rates_a2 = get_rates(set_partitions2)
rates_b2 = get_rates(set_partitions2, partition_func=corrected_pas,
                    partition_kw={"taxlen": wl2.width})
delta2 = DeltaScoreMetric(matrix=get_matrix(wl2.cols, patterns2)).score()
qres2 = QResidualMetric(matrix=get_matrix(wl2.cols, patterns2)).score()


print(tabulate(
    [["Combined", sum(rates_a1.values()) / len(rates_a1),
      sum(rates_b1.values()) / len(rates_b1), 
      sum(delta1.values()) / len(delta1),
      sum(qres1.values()) / len(qres1),
      ],
     ["Tibetic", sum(rates_a2.values()) / len(rates_a2),
      sum(rates_b2.values()) / len(rates_b2), 
      sum(delta2.values()) / len(delta2),
      sum(qres2.values()) / len(qres2),
      ],
     ],
    headers=["Wordlist", "TIGER", "Corrected TIGER", "Delta", "Q-Residuals"]))


