help:
	echo "Usage make option"
	echo "Options:"
	echo "base-data (extract sublist of Tibetic varieties originally coded)"
	echo "combined-data (extract combined list of Tibetic varieties)"

base-data:
	cd code; sh create-base-wordlist.sh > ../wordlists/base-wordlist.tsv

full-data:
	cd code; sh create-full-wordlist.sh > ../wordlists/full-wordlist.tsv

base-data-ed:
	edictor wordlist --namespace='{"language_id": "doculect", "concept_name": "concept", "value": "value", "form": "form", "grouped_segments": "tokens", "morpheme_structure": "morpheme_structure", "internal_cognacy": "internal_cognacy", "partial_cognacy": "partial_cognacy", "comment": "note", "source": "source"}' --dataset=cldf/cldf-metadata.json --preprocessing=code/base.py --name=wordlists/dhakalsouthwesttibetic

	
db:
	cldf createdb cldf/cldf-metadata.json sqlite/dhakalsouthwesttibetic.sqlite3

full-data-ed: 
	edictor wordlist --namespace='{"language_id": "doculect", "concept_name": "concept", "value": "value", "form": "form", "grouped_segments": "tokens", "morpheme_structure": "morpheme_structure", "internal_cognacy": "internal_cognacy", "partial_cognacy": "partial_cognacy", "comment": "note", "source": "source", "combined": "combined"}' --dataset=cldf/cldf-metadata.json --preprocessing=code/combined.py --name=wordlists/tibeticcombined

nexus-file:
	lingpy wordlist -i wordlists/full-wordlist.tsv -o nexus/full-wordlist --format=paps.nex

