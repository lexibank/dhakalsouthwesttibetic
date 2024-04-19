### Data Collection

Data was collected, led by D. N. Dhakal, in 2018, using a questionnaire of 243 items. The original data as it was collected is available from the folder `raw/` in all files ending in `.tab` (`Kagate_240.tab`, etc.).

The CLDF conversion was first done with this original data, but later, we converted the data from the first CLDF version to the EDICTOR format that we needed for the curation and annotation process. As a result, the data that is shared with the CLDF repository contains additional, at times manual, modifications. A comparison with the original data is always possible, specifically also, since the forms in the original collection are available from the column `Value` in the CSV file providing the forms in CLDF (`cldf/forms.csv`).

### Requirements

We assume that you have Python in a fresh virtual environment available, as well as SQLite, and a basic terminal that offers a basic Shell (e.g. bash).

To install the required Python packages, type:

```shell
pip install -e .
```

### Comparison and Extension of the Data

Data was later compared and extended by adding data for Tibetic languages and Old Chinese from [Sagart et al. (2019)](https://github.com/lexibank/sagartst). The conversion was first carried out in a dedicated Python script, selecting those concepts present in both datasets. The CLDF version now provides a combined dataset with both the originally collected data (wordlists of about 240 items) and the comparative wordlist in which Tibetic languages and Old Chinese from Sagart et al. are added. Both versions (the original version of 8 varieties and the combined version with a limited number of concepts) can be retrieved with the commands we provide in the Makefile by typing:

```shell
make base-data
```

This code makes use of the SQLite version of the data provided in the folder `sqlite` which was created with the help of the `pycldf` package. The conversion of the data to SQLite can also be carried out with the help of the Makefile by typing:

```shell
make db
```

Accordingly, the base data can also be created:

```shell
make full-data
```

If you install the Python package `pyedictor` (`pip install pyedictor >= 0.4`), you can extract the base data and the full data also with slightly modified commands that yield, however, the same results.

```shell
make base-data-ed
make full-data-ed
```

Our phylogenetic analyses are based on the combined data. The nexus file we used as the basis here can also be created automatically with the help of the Makefile.

```shell
make nexus-file
```

The resulting Nexus file is stored in the folder `nexus` as `full-wordlist.nex`.

If you want to test TIGER scores, Delta Scores, and Q-Residuals in the data, you can also do this with the Makefile, but you must install additional packages first.

```shell
make install
make tiger-et-al
```

This will print out the scores computed for the base wordlist and the full wordlist.

```
Wordlist       TIGER    Corrected TIGER     Delta    Q-Residuals
----------  --------  -----------------  --------  -------------
Combined    0.678752           0.379645  0.342274     0.00852446
Tibetic     0.74708            0.193927  0.39871      0.0122
```

