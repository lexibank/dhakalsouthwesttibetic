import re
from pathlib import Path

from clldutils.misc import slug
from pylexibank.util import progressbar
from pylexibank import FormSpec, Lexeme, Concept, Language, progressbar
from pylexibank import Dataset as BaseDataset
import attr
from pyedictor import fetch
from lingpy import *


@attr.s
class CustomLanguage(Language):
    File_Name = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Family = attr.ib(default="Sino-Tibetan")


@attr.s
class CustomLexeme(Lexeme):

    #Tone_Value = attr.ib(default=None)
    #Gloss_In_Source = attr.ib(default=None)
    Morpheme_Structure = attr.ib(default=None)
    Grouped_Segments = attr.ib(default=None)
    Partial_Cognacy = attr.ib(default=None)



@attr.s
class CustomConcept(Concept):
    Nepali_Gloss = attr.ib(default=None)
    Number = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'dhakalsouthwesttibetic'
    
    lexeme_class = CustomLexeme
    language_class = CustomLanguage
    concept_class = CustomConcept

    form_spec = FormSpec(
        brackets={"[": "]", "{": "}", "(": ")"},
        separators=";/,~",
        missing_data=('-', ),
        strip_inside_brackets=True,
        first_form_only=True,
    )

    def cmd_download(self, args):
        with open(self.raw_dir / "data.tsv", "w") as f:
            f.write(fetch("dhakalsouthwesttibetic",
                          base_url="https://lingulist.de/edev/"))
        args.log.info('wrote data to file')

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        concepts = {}
        sagart = {
                c.concepticon_gloss: c.english for c in
                self.conceptlists[0].concepts.values()}
        backstrom = {
                c.concepticon_gloss: c.english for c in
                self.conceptlists[1].concepts.values()}
        matches1, matches2 = [], []
        for concept in self.concepts:
            idx = "{0}-{1}".format(
                    concept["NUMBER"],
                    slug(concept["ENGLISH"], lowercase=False))
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["ENGLISH"],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Nepali_Gloss=concept["NEPALI"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"])
            concepts[concept["ENGLISH"]] = idx
            if concept["CONCEPTICON_GLOSS"] in sagart:
                matches1.append(
                        (concept["ENGLISH"], concept["CONCEPTICON_GLOSS"]))
            if concept["CONCEPTICON_GLOSS"] in backstrom:
                matches2.append(
                        (concept["ENGLISH"], concept["CONCEPTICON_GLOSS"]))

        args.log.info(
                "found {0} concepts common with Sagart's list".format(len(matches1)))
        args.log.info(
                "found {0} concepts common with Backstrom's list".format(len(matches2)))
        for c in backstrom:
            if c not in [m[1] for m in matches2]:
                args.log.info("not found "+ c)

        for language in progressbar(self.languages):
            args.writer.add_language(**language)

        def split_tokens(tokens):
            out = []
            for t in tokens:
                out += t.split(".")
            return out

        wl = Wordlist(str(self.raw_dir / "data.tsv"))
        for idx in wl:
            if not wl[idx, "concept"].startswith("*") and not \
                    wl[idx, "language"] == "Pattern": 
                args.writer.add_form_with_segments(
                        Language_ID=wl[idx, "doculect"],
                        Parameter_ID=concepts[wl[idx, "concept"]],
                        Value=wl[idx, "value"],
                        Form=wl[idx, "form"],
                        Segments=split_tokens(wl[idx, "tokens"]),
                        Grouped_Segments=" ".join(wl[idx, "tokens"]),
                        Morpheme_Structure=" ".join(wl[idx, "morphemes"]),
                        Cognacy=wl[idx, "cogid"],
                        Partial_Cognacy=" ".join([str(c) for c in wl[idx, "cogids"]]),
                        Comment=wl[idx, "note"],
                        Source="Dhakal2024"
                        )

