# Copyright (c) CRS4 2024
#
# This file is part of BBMRI-FP-ETL.
#
# BBMRI-FP-ETL is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# BBMRI-FP-ETL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with BBMRI-FP-ETL. If not, see <https://www.gnu.org/licenses/>.

import os
from collections import namedtuple
from datetime import datetime, date
from typing import Iterable

from bbmri_fp_etl.converter import Converter
from bbmri_fp_etl.destinations.fhir import FHIRDest
from bbmri_fp_etl.destinations.omop import OMOPDest
from bbmri_fp_etl.models import Donor, Sex, Case, SampleType, SamplingEvent, Sample, Collection
from bbmri_fp_etl.serializer import JsonFile, CSVFile
from bbmri_fp_etl.sources import AbstractSource

# simulating a situation where there is one collection of samples
COLLECTION_ID = "sample_collection:1"

Patient = namedtuple('Patient', ['id', 'name', 'surname', 'sex', 'date_of_birth'])
Specimen = namedtuple('Specimen', ['id', 'patient_id', 'type', 'withdrawn', 'condition'])
Event = namedtuple('Event', ['id', 'patient_id', 'type'])

PATIENTS = [
    Patient("pid:1", "John", "Smith", "male", "18-05-1970"),
    Patient("pid:2", "Mariam", "Yale", "female", "05-11-1984"),
    Patient("pid:3", "Bob", "Taylor", "male", "24-08-2010"),
    Patient("pid:4", "Alice", "Brown", "unknown", "03-04-2016")
]

SPECIMENS = [
    Specimen("pid:1:specimen:1", "pid:1", "dna", "2010-10-19", "frozen"),
    Specimen("pid:1:specimen:2", "pid:1", "blood", "2010-10-19", "frozen"),
    Specimen("pid:1:specimen:3", "pid:1", "buffy-coated", "2010-10-19", "frozen"),
    Specimen("pid:2:specimen:1", "pid:2", "plasma", "2023-05-13", "ffpe"),
    Specimen("pid:2:specimen:1", "pid:2", "serum", "2023-05-13", "frozen"),
    Specimen("pid:3:specimen:1", "pid:3", "ascites", "1998-03-15", "ffpe"),
    Specimen("pid:4:specimen:1", "pid:4", "faeces", "2005-07-23", "frozen"),
    Specimen("pid:4:specimen:2", "pid:4", "urine", "2005-07-23", "ffpe"),
    Specimen("pid:4:specimen:3", "pid:4", "saliva", "2005-07-23", "ffpe"),
    Specimen("pid:4:specimen:4", "pid:4", "leucocyte", "2005-07-23", "ffpe"),
    Specimen("pid:4:specimen:5", "pid:4", "erythrocyte", "2005-07-23", "ffpe"),
]

SPECIMENS_MAPPING = {
    "dna": SampleType.DNA,
    "blood": SampleType.WHOLE_BLOOD,
    "buffy-coated": SampleType.BUFFY_COAT,
    "plasma": SampleType.PLASMA,
    "serum": SampleType.SERUM,
    "ascites": SampleType.ASCITES_FLUID,
    "faeces": SampleType.FECES,
    "urine": SampleType.URINE,
    "saliva": SampleType.SALIVA,
    "leucocyte": SampleType.PRIMARY_CELLS,
    "erythrocyte": SampleType.RED_BLOOD_CELLS
}

EVENTS = [{
    "type": "diagnosis",
}]

class ExampleSource(AbstractSource):
    """
    Example class that creates some Cases. This is intended to give an example of a possible
    creation of Cases starting from a fake data set.
    It shows how to fill the models and represent the data usinig the provided models.
    It also shows some issues that may occur, such as needed transcoding for materials etc
    It is not intended to be computationally efficient
    """

    def get_biobanks_data(self):
        raise NotImplementedError()

    def get_cases_data(self) -> Iterable[Case]:
        cases = []
        for p in PATIENTS:
            donor = Donor(
                id=p.id,
                # mapping of the internal gender values to the one used in the model
                gender={"male": Sex.MALE, "female": Sex.FEMALE, "unknown": Sex.UNKNOWN}[p.sex],
                birth_date=datetime.strptime(p.date_of_birth, "%d-%m-%Y")
            )
            samples = []
            for s in SPECIMENS:
                if p.id == s.patient_id:
                    sampling_event = SamplingEvent(
                        id=f"sampling:{s.id}",  # gives a name to the event
                        date_at_event=date.fromisoformat(s.withdrawn)
                    )
                    samples.append(Sample(
                        id=s.id,
                        type=SPECIMENS_MAPPING[s.type],
                        events=[sampling_event],
                        collection=Collection(
                            id=COLLECTION_ID
                        )
                    ))

            cases.append(Case(
                donor=donor,
                samples=samples
            ))

        return cases


if __name__ == '__main__':
    source = ExampleSource()
    output_dir = os.path.join(os.path.dirname(__file__), 'output')

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    fhir_destination = FHIRDest(JsonFile(output_dir))
    c = Converter(source, fhir_destination, Converter.CASE)
    c.run()

    omop_destination = OMOPDest(CSVFile(output_dir))
    c = Converter(source, omop_destination, Converter.CASE)
    c.run()
