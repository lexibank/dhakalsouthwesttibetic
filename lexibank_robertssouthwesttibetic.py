import re
from pathlib import Path

from clldutils.misc import slug
from pylexibank.util import progressbar
from pylexibank import FormSpec, Lexeme, Concept, Language, progressbar
from pylexibank import Dataset as BaseDataset
import attr

@attr.s
class CustomLanguage(Language):
    File_Name = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Family = attr.ib(default="Sino-Tibetan")


@attr.s
class CustomLexeme(Lexeme):
    Tone_Value = attr.ib(default=None)
    Gloss_In_Source = attr.ib(default=None)


@attr.s
class CustomConcept(Concept):
    Tibetan_Gloss = attr.ib(default=None)
    Number = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'robertssouthwesttibetic'
    
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

    def cmd_makecldf(self, args):
        args.writer.add_sources()
        concepts = {}
        sagart = {
                c.concepticon_gloss: c.english for c in
                self.conceptlists[0].concepts.values()}
        matches = []
        for concept in self.concepts:
            idx = "{0}-{1}".format(
                    concept["NUMBER"],
                    slug(concept["ENGLISH"], lowercase=False))
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["ENGLISH"],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Tibetan_Gloss=concept["TIBETAN"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"])
            concepts[concept["ENGLISH"]+"-"+concept["TIBETAN"]] = idx
            if concept["CONCEPTICON_GLOSS"] in sagart:
                matches.append(
                        (concept["ENGLISH"], concept["CONCEPTICON_GLOSS"]))
        args.log.info(
                "found {0} concepts common with Sagart's list".format(len(matches)))
        for language in progressbar(self.languages):
            args.writer.add_language(**language)
            for row in self.raw_dir.read_csv(
                    language["File_Name"],
                    delimiter="\t", 
                    dicts=True):
                args.writer.add_form(
                        Language_ID=language["ID"],
                        Parameter_ID=concepts["{0}-{1}".format(
                            row["GLOSS"], row["SCRIPT"])],
                        Value=row["TRANSCRIPTION"],
                        Gloss_In_Source=row["SCRIPT"],
                        Form=row["TRANSCRIPTION"].strip(),
                        Tone_Value=row["TONE"],
                        Source="Roberts2022"
                        )

