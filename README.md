# BBMRI Federated Platform Converter 

This project contains a tool to help developers in converting data about samples read from a data source into formats compatible
with the [BBMRI Federated Platform](https://www.bbmri-eric.eu/federated-platform/). In particular, it can convert data into FHIR Resources for the 
[BBMRI Sample Locator](https://locator.bbmri-eric.eu/) and in OMOP for the [BBMRI Finder](https://finder.bbmri-eric.eu/). 

The utility implements an internal data model compatible with [MIABIS](https://github.com/BBMRI-ERIC/miabis).

To convert data from a new source, a new class extending `AbstractSource` should be implemented to create the MIABIS
classes that can be then converted and serialized for the needed Federated Platform solution.

A schema of the ETL process using the tool is the following

![ETL PROCESS](images/etl_process.png)

An example of a class implementing a source from a mock dataset can be found in `examples` directory.

## Dependencies

To use the tool Python 3.12 and [Poetry](https://python-poetry.org/) are needed. All other python dependencies will 
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

## License 

This project is licensed under the terms of the GNU General Public License v3.0 (GNU GPLv3). See the [LICENSE](LICENSE) for details

## Acknowledgments

This work has been partially supported by the following sources:
 * The [European Joint Programme on Rare Disease (EJPRD)](https://www.ejprarediseases.org/) project (grant agreement N. 825575)
 * The [EOSC-Life](https://www.eosc-life.eu/) European project (grant agreement N. 824087), within the EOSC-Life WP1 Demonstrator “Cloudification of BBMRI-ERIC CRC-Cohort and its Digital Pathology Imaging” (APPID 1228).
