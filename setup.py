from setuptools import setup
import json

with open('metadata.json', 'r', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_dhakalsouthwesttibetic',
    description=metadata['title'],
    license=metadata['license'],
    url=metadata['url'],
    py_modules=['lexibank_dhakalsouthwesttibetic'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'dhakalsouthwesttibetic=lexibank_dhakalsouthwesttibetic:Dataset',
        ]
    },
    install_requires=[
        'pylexibank>=2.1',
        'pyedictor>=0.4'
    ]
)
