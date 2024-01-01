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
    Sources = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):

    #Tone_Value = attr.ib(default=None)
    #Gloss_In_Source = attr.ib(default=None)
    Morpheme_Structure = attr.ib(default=None, metadata={
        "datatype": "string", "separator": " "})
    Grouped_Segments = attr.ib(default=None, metadata={
        "datatype": "string", "separator": " "})
    Partial_Cognacy = attr.ib(default=None, metadata={"datatype": "string",
                                                      "separator": " "})
    Internal_Cognacy = attr.ib(default=None, metadata={"datatype": "integer"})
    Combined = attr.ib(default=None, metadata={"datatype": "integer"})
    Alignment = attr.ib(default=None, metadata={"datatype": "string",
                                                "separator": " "})
    Subset = attr.ib(default=None)



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
        with open(self.raw_dir / "data-2.tsv", "w") as f:
            f.write(fetch("tibeticcombined",
                          base_url="https://lingulist.de/edev/",
                          columns=["DOCULECT", "CONCEPT", "FORM", "COGID", "TOKENS", "NOTE"]),
                    )
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
        c2c = {}
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
            concepts[concept["CONCEPTICON_GLOSS"]] = idx
            
            c2c[concept["ENGLISH"]] = concept["CONCEPTICON_GLOSS"]
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
        
        wls = Wordlist(str(self.raw_dir / "data-2.tsv"))
        lookup = {(wls[idx, "doculect"], wls[idx, "form"]): idx for idx in wls}
        wl = Wordlist(str(self.raw_dir / "data.tsv"))
        for idx in wl:
            if not wl[idx, "concept"].startswith("*") and not \
                    wl[idx, "language"] == "Pattern": 
                doc, form = wl[idx, "doculect"], wl[idx, "form"]
                if (doc, form) in lookup and c2c[wl[idx, "concept"]] in wls.rows:
                    cognacy = wls[lookup[doc, form], "cogid"]
                    combined = 1
                elif c2c[wl[idx, "concept"]] in wls.rows:
                    args.log.info("problem with {0} / {1}".format(doc, form))
                    cognacy = 0
                    combined = 1
                else:
                    cognacy = None
                    combined = 0
                args.writer.add_form_with_segments(
                        Language_ID=wl[idx, "doculect"],
                        Parameter_ID=concepts[wl[idx, "concept"]],
                        Value=wl[idx, "value"],
                        Form=wl[idx, "form"],
                        Segments=split_tokens(wl[idx, "tokens"]),
                        Grouped_Segments=wl[idx, "tokens"],
                        Morpheme_Structure=wl[idx, "morphemes"],
                        Internal_Cognacy=wl[idx, "cogid"],
                        Cognacy=cognacy,
                        Partial_Cognacy=[str(c) for c in wl[idx, "cogids"]],
                        Comment=wl[idx, "note"],
                        Source="Dhakal2024",
                        Combined=combined,
                        Alignment=wl[idx, "alignment"],
                        Subset="Dhakal2024"
                        )
        args.log.info("adding final wordlist by Sagart et al. 2019")
        # add new data points
        for idx, language, concept, form, tokens, cogid, note in wls.iter_rows(
                "doculect", "concept", "form", "tokens", "cogid", "note"):
            if language in ["OldTibetan", "Alike", "Batang", "Xiahe",
                            "OldChinese", "Lhasa"]:
                args.writer.add_form_with_segments(
                        Language_ID=language,
                        Parameter_ID=concepts[concept],
                        Value=form.strip() or "".join(tokens),
                        Form=form.strip() or "".join(tokens),
                        Segments=split_tokens(tokens),
                        Grouped_Segments=tokens,
                        Cognacy=cogid,
                        Combined=1,
                        Comment=note,
                        Source="Sagart2019",
                        Subset="Sagart2019"
                        )

