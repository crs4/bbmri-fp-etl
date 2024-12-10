# BBMRI Federated Platform ETL 

This project contains a tool to help source with data of samples in converting them in formats compatible
with the BBMRI Federated Platform. In particular, it can convert data into FHIR Resources for the 
[BBMRI Sample Locator](https://samply.github.io/bbmri-fhir-ig/overview.html) and in OMOP for the BCPlatform. 

The utility implements an internal data model compatible with [MIABIS](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7310316/).

To convert data from a new source, a new class extending `AbstractSource` should be implemented.
An example of a class implementing a source from a mock dataset can be found in `examples` directory.

## Dependencies

To use the script Python 3.10 and [Poetry](https://python-poetry.org/) are needed. All other python dependencies will 
be installed using poetry

### Install dependencies

To install all the packages needed, run

```commandline
poetry install
```

## Usage
The package can convert data about aggregated objects (i.e., biobanks and collections) or about cases.
The source can provide data about one type of entity or both: indeed in some cases, the Case data may refer to a 
collection/biobank whose data are taken from another source (e.g., the collections and biobanks are from the 
BBMRI directory). 

Depending on what type of data the source provides, the correct methods of the abstract class must be implemented:
in case biobanks data are provided, the method `get_biobanks_data` has to be implemented, while in case of samples,
the method `get_cases_data` has to be implemented. 

To generate data from a source a `Converter` must be instantiated with a Source and a Destination class. 

An example is:

```python
source = ExampleSource()
output_dir = os.path.join(os.path.dirname(__file__), 'output')

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

destination = FHIRDest(JsonFile(output_dir))
c = Converter(source, destination, Converter.CASE)
c.run()
```