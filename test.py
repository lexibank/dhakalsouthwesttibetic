def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


# should be 210 items
def test_parameters(cldf_dataset):
    assert len(list(cldf_dataset["ParameterTable"])) == 243


# test we have some languages
def test_languages(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 14


