# convert the data to a wordlist compatible with lingpy / edictor
sqlite3 ../sqlite/dhakalsouthwesttibetic.sqlite3 <<EOF
.headers on
.separator "\t"

select 
	ROW_NUMBER() OVER() as ID, 
	l.cldf_id as DOCULECT, 
	p.cldf_name as CONCEPT, 
	f.cldf_value as VALUE, 
	f.cldf_form as FORM, 
	f.cldf_segments as TOKENS_IN_SOURCE,
       	f.grouped_segments as TOKENS, 
	f.cognacy as COGID 
from 
	languagetable as l,
	parametertable as p, 
	formtable as f 
where 
	l.cldf_id = f.cldf_languagereference 
and 
	p.cldf_id = f.cldf_parameterreference 
and 
	f.subset = 'Dhakal2024';

EOF

