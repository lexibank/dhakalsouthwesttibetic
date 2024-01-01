from lingpy import basictypes

def run(wordlist):
    
    dct = {0: 
           [
               "doculect", "concept", "form", "tokens", 
               "cogid", "source", "note"
               ]}

    for idx in wordlist:
        if wordlist[idx, "combined"] == 1:
            dct[idx] = [wordlist[idx, h] for h in dct[0]]

    return dct

