from lingpy import basictypes

def run(wordlist):
    
    dct = {0: 
           [
               "doculect", "concept", "form", "tokens", "cogids", 
               "morphemes", "alignment", "cogid", "source", "note"
               ]}

    wordlist.add_entries("morphemes", "morpheme_structure", lambda x: x)
    wordlist.add_entries(
            "cogids", 
            "partial_cognacy", 
            lambda x: basictypes.ints(" ".join(x)) if x else basictypes.ints("0")
            )
    wordlist.add_entries(
            "cogid", 
            "internal_cognacy", 
            lambda x: int(x) if x else 0
            )

    for idx in wordlist:
        if wordlist[idx, "source"][0] == "Dhakal2024":
            dct[idx] = [wordlist[idx, h] for h in dct[0]]

    return dct

