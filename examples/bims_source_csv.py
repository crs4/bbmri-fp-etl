# Copyright (c) CRS4 2024
#
# This file is part of BBMRI-FP-ETL.
#
# BBMRI-FP-ETL is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# BBMRI-FP-ETL is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BBMRI-FP-ETL. If not, see <https://www.gnu.org/licenses/>.

import os
from collections import namedtuple
from datetime import datetime, date
from typing import Iterable

from bbmri_fp_etl.converter import Converter
from bbmri_fp_etl.destinations.fhir import FHIRDest
from bbmri_fp_etl.destinations.omop import OMOPDest
from bbmri_fp_etl.models import (
    Donor,
    Sex,
    Case,
    SampleType,
    EventType,
    SamplingEvent,
    Sample,
    Biobank,
    Collection,
    StorageTemperature,
    DiagnosisEvent,
    Disease,
    DiseaseOntologyCode,
    AgeUnit,
    Contact,
    Name,
    ContactRole,
    Address,
    Telecom,
    TelecomType,
    RoleType,
    Consent,
    ConsentCondition,
    CCE,
    ConsentCategory,
)
from bbmri_fp_etl.serializer import JsonFile, CSVFile
from bbmri_fp_etl.sources import AbstractSource
from bbmri_fp_etl.models import EventType

from dateutil import parser
import pytz
import argparse
import yaml
import sys


# read biobank config
def read_biobank_config_file(inputfile):
    with open(inputfile, "r") as f:
        biobank_data = yaml.safe_load(f)
    return biobank_data


# read collection config
def read_collection_config_file(inputfile):
    with open(inputfile, "r") as f:
        collection_data = yaml.safe_load(f)
    return collection_data


# read consent config
def read_consent_config_file(inputfile):
    with open(inputfile, "r") as f:
        consent_data = yaml.safe_load(f)
    return consent_data


# read minimal dataset from csv file
def read_minimal_dataset_from_csv_file(file_path, consent_boolean):
    # I'm assuming one consent per patient per collection under which all the samples are covered
    with open(file_path, "r") as f:
        csv_data = f.readlines()
    patients = []
    current_patient = None
    current_patient_data = {}
    current_patient_specimens = []
    for line in csv_data[1:]:
        line = line.strip()
        if not line:
            current_patient_data["specimens"] = current_patient_specimens
            patients.append(current_patient_data)
            current_patient_data = {}
            current_patient_specimens = []
            continue
        line = line.split(",")
        if not current_patient:
            current_patient = line[1]
            if consent_boolean:
                cces_pairs = line[13 : 13 + 22]
                it = iter(cces_pairs)
                pairs_dict = dict(zip(it, it))
                consent = {
                    "consent_id": line[10],
                    "consent_datetime": line[11],
                    "consent_status": line[12],
                    "consent_CCEs": pairs_dict,
                }
                current_patient_data["consent"] = consent
            current_patient_data["id"] = line[1]
            current_patient_data["birth_date"] = line[6]
            current_patient_data["sex"] = line[7]

        elif line[1] != current_patient:
            current_patient_data["specimens"] = current_patient_specimens
            patients.append(current_patient_data)
            current_patient_data = {}
            current_patient_specimens = []
            if consent_boolean:
                cces_pairs = line[13 : 13 + 22]
                it = iter(cces_pairs)
                pairs_dict = dict(zip(it, it))
                consent = {
                    "consent_id": line[10],
                    "consent_datetime": line[11],
                    "consent_status": line[12],
                    "consent_CCEs": pairs_dict,
                }
                current_patient_data["consent"] = consent
            current_patient_data["id"] = line[1]
            current_patient_data["birth_date"] = line[6]
            current_patient_data["sex"] = line[7]

        specimen = {
            "id": line[0],
            "sampling_date": line[2],
            "diagnosis": line[3],
            "diagnosis_date": line[4],
            "diagnosis_donor_age": line[5],
            "material_type": line[8],
            "storage_temperature": line[9],
        }
        current_patient_specimens.append(specimen)

    return patients


# read minimal dataset from excel file
def read_minimal_dataset_from_excel_file(file_path):
    pass


# read minimal dataset from REST API
def read_minimal_dataset_from_rest_api():
    pass


def parse_to_utc(inputvalue: str):
    newvalue = parser.parse(inputvalue).astimezone(pytz.UTC)
    return newvalue.replace(microsecond=0)


SEX_MAPPING = {
    "Undifferentiated": Sex.UNDIFFERENTIATED,
    "Unknown": Sex.UNKNOWN,
    "Male": Sex.MALE,
    "Female": Sex.FEMALE,
}

MATERIAL_TYPE_MAPPING = {
    "Plasma": SampleType.PLASMA,
    "RNA": SampleType.RNA,
    "Saliva": SampleType.SALIVA,
    "Serum": SampleType.SERUM,
    "Throat swab": SampleType.SWAB,
    "Tissue (frozen)": SampleType.TISSUE_FROZEN,
    "Tissue (paraffin preserved)": SampleType.TISSUE_FFPE,
    "Tissue (stained sections/slides)": SampleType.PROCESSED_SPECIMEN,
    "Urine": SampleType.URINE,
    "Any": SampleType.ANY,
}

STORAGE_TEMP_MAPPING = {
    "-18°C to -35°C": StorageTemperature.TEMP_MINUS_18_TO_MINUS_35,
    "-60°C to -80°C": StorageTemperature.TEMP_MINUS_60_TO_MINUS_85,
    "2°C to 10°C": StorageTemperature.TEMP_2_TO_10,
    "Liquid Nitrogen": StorageTemperature.LNL,
    "Other": StorageTemperature.OTHER,
    "Room temperature": StorageTemperature.RT,
}


class BIMSSource(AbstractSource):
    """
    class that implements the AbstractSource for the BIMS
    """

    def __init__(self, patientsdata, biobankdata, collectiondata, consentdata=None):
        self.patientsdata = patientsdata
        self.biobankdata = biobankdata
        self.collectiondata = collectiondata
        self.consentdata = consentdata

    def get_biobanks_data(self):
        organizations = []
        self.biobank = self._create_biobank()
        self.collection = self._create_collection()
        self.collection.biobank = self.biobank
        organizations.append(self.biobank)
        organizations.append(self.collection)
        # return organizations
        return organizations

    def _create_biobank(self):
        Contact_director = Contact(
            name=Name(
                given=" ".join(self.biobankdata["DIRECTOR_GIVEN_NAME"]),
                family=self.biobankdata["DIRECTOR_FAMILY_NAME"],
                prefix=",".join(self.biobankdata["DIRECTOR_PREFIX_NAME"]),
            ),
            telecom=[
                Telecom(
                    type=TelecomType.EMAIL,
                    value=self.biobankdata["DIRECTOR_EMAIL"],
                ),
                Telecom(
                    type=TelecomType.PHONE,
                    value=f"{self.biobankdata["DIRECTOR_PHONE"]}",
                ),
            ],
            role=ContactRole(
                type=RoleType.DIRECTOR,
                description="biobank director (primary contact person)",
            ),
        )
        Contact_research_contact = Contact(
            name=Name(
                given=" ".join(self.biobankdata["CONTACT_GIVEN_NAME"]),
                family=self.biobankdata["CONTACT_FAMILY_NAME"],
                prefix=",".join(self.biobankdata["CONTACT_PREFIX_NAME"]),
            ),
            telecom=[
                Telecom(
                    type=TelecomType.EMAIL,
                    value=self.biobankdata["CONTACT_EMAIL"],
                ),
                Telecom(
                    type=TelecomType.PHONE,
                    value=f"{self.biobankdata["CONTACT_PHONE"]}",
                ),
            ],
            role=ContactRole(
                type=RoleType.RESEARCH_CONTACT,
                description="secondary point of contact (Research contact)",
            ),
            address=Address(
                country=self.biobankdata["CONTACT_ADD_COUNTRY"],
                street=" ".join(self.biobankdata["CONTACT_ADD_LINE"]),
                city=self.biobankdata["CONTACT_ADD_CITY"],
                zip=f"{self.biobankdata["CONTACT_ADD_POSTAL_CODE"]}",
            ),
        )
        mybiobank = Biobank(
            id=self.biobankdata["BIOBANK_DIRECTORY_ID"],
            acronym=",".join(self.biobankdata["BIOBANK_ALIAS"]),
            description=self.biobankdata["BIOBANK_DESCRIPTION"],
            contact=[Contact_director, Contact_research_contact],
            name=self.biobankdata["BIOBANK_NAME"],
            juristic_person=self.biobankdata["BIOBANK_JURIDICALPERSON"],
            address=Address(
                country=self.biobankdata["BIOBANK_COUNTRY"],
                street=" ".join(self.biobankdata["BIOBANK_LINE"]),
                city=self.biobankdata["BIOBANK_CITY"],
                zip=f"{self.biobankdata["BIOBANK_POSTAL_CODE"]}",
            ),
        )
        return mybiobank

    def _create_collection(self):
        mycollection = Collection(
            id=self.collectiondata["COLLECTION_DIRECTORY_ID"],
            acronym=self.collectiondata["COLLECTION_ALIAS"],
            description=self.collectiondata["COLLECTION_DESCRIPTION"],
            contact=[
                Contact(
                    name=Name(
                        given=" ".join(
                            self.collectiondata["COLLECTION_CONTACT_GIVEN_NAME"]
                        ),
                        family=self.collectiondata["COLLECTION_CONTACT_FAMILY_NAME"],
                        prefix=",".join(
                            self.collectiondata["COLLECTION_CONTACT_PREFIX_NAME"]
                        ),
                    ),
                    telecom=[
                        Telecom(
                            type=TelecomType.EMAIL,
                            value=self.collectiondata["COLLECTION_CONTACT_EMAIL"],
                        ),
                        Telecom(
                            type=TelecomType.PHONE,
                            value=f"{self.collectiondata["COLLECTION_CONTACT_PHONE"]}",
                        ),
                    ],
                    role=ContactRole(
                        type=RoleType.COLLECTION_POINT_OF_CONTACT,
                    ),
                )
            ],
            name=self.collectiondata["COLLECTION_NAME"],
            address=Address(
                country=self.collectiondata["COLLECTION_COUNTRY"],
                street=" ".join(self.collectiondata["COLLECTION_LINE"]),
                city=self.collectiondata["COLLECTION_CITY"],
                zip=f"{self.collectiondata["COLLECTION_POSTAL_CODE"]}",
            ),
            data_category=self.collectiondata["DATA_CATEGORY_CODE"].split(","),
            type=self.collectiondata["COLLECTION_TYPE_CODE"].split(","),
        )
        return mycollection

    def get_cases_data(self) -> Iterable[Case]:
        cases = []
        for p in self.patientsdata:
            s = p["specimens"][0]
            diagnosis_event = DiagnosisEvent(
                id=f"diagnosis:{p["id"]}",
                event_date=date.fromisoformat(s["diagnosis_date"]),
                age_at_event=s["diagnosis_donor_age"],
                age_at_event_unit=AgeUnit.YEARS,
                event_type=EventType.DIAGNOSIS,
                disease=Disease(
                    main_code=DiseaseOntologyCode(
                        ontology="http://hl7.org/fhir/sid/icd-10",
                        code=s["diagnosis"],
                    ),
                    mapping_codes=[],
                ),
            )
            donor = Donor(
                id=p["id"],
                gender=SEX_MAPPING[p["sex"]],
                birth_date=parser.parse(p["birth_date"]).date(),
                events=(
                    [diagnosis_event]
                    if diagnosis_event is not None
                    else diagnosis_event
                ),
            )

            samples = []
            for s in p["specimens"]:
                sampling_event = SamplingEvent(
                    id=f"sampling:{s["id"]}",
                    event_date=date.fromisoformat(s["sampling_date"]),
                    event_type=EventType.SPECIMEN_COLLECTION,
                )
                samples.append(
                    Sample(
                        id=s["id"],
                        type=MATERIAL_TYPE_MAPPING[s["material_type"]],
                        events=[sampling_event],
                        collection=self.collection,
                        storage_temperature=[
                            STORAGE_TEMP_MAPPING[s["storage_temperature"]]
                        ],
                        content_diagnosis=[
                            Disease(
                                main_code=DiseaseOntologyCode(
                                    ontology="http://hl7.org/fhir/sid/icd-10",
                                    code=s["diagnosis"],
                                ),
                                mapping_codes=[],
                            )
                        ],
                    )
                )
            if self.consentdata is not None:
                consent = Consent(
                    id=p["consent"]["consent_id"],
                    scope=self.consentdata["CONSENT_SCOPE"],
                    category=ConsentCategory[self.consentdata["CONSENT_CATEGORY"]],
                    status=p["consent"]["consent_status"],
                    datetime_of_creation=parse_to_utc(p["consent"]["consent_datetime"]),
                    organization=self.biobank,
                    base_policy=self.consentdata["CONSENT_BASE_POLICY"],
                    meaning=self.consentdata["CONSENT_CONDITION_SUBJECT_MEANING"],
                    main_class=self.consentdata["CONSENT_CLASS"],
                    start_time=parse_to_utc(p["consent"]["consent_datetime"]),
                    patient=donor,
                    consent_conditions=[
                        ConsentCondition(cce=CCE[k], decision=v, specimens=samples)
                        for k, v in p["consent"]["consent_CCEs"].items()
                    ],
                )
                cases.append(Case(donor=donor, samples=samples, consent=consent))
            else:
                cases.append(Case(donor=donor, samples=samples))

        return cases


def main():
    argparser = argparse.ArgumentParser(
        description="Tool to generate objects, compatible with BBMRI Federated search services "
        "from BIMS source"
    )

    argparser.add_argument("--inputdir", "-i", help="Input directory", default="input")
    argparser.add_argument(
        "--outputdir", "-o", help="Output directory", default="output"
    )
    argparser.add_argument(
        "--consent",
        "-nc",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable/Disable consent from input/output",
        dest="consent_boolean",
    )
    argparser.add_argument(
        "--minimal_dataset_input_file",
        "-f",
        help="Input file",
        default="minimal-dataset-with-consent-template.csv",
    )
    argparser.add_argument(
        "--minimal_dataset_type_of_input",
        "-m",
        help="Type of input",
        choices=["csv", "excel", "REST_API"],
        default="csv",
    )

    argparser.add_argument(
        "--biobank_yaml_config_file",
        "-b",
        help="Biobank config file in yaml format",
        default="biobank_config.yaml",
    )
    argparser.add_argument(
        "--collection_yaml_config_file",
        "-c",
        help="Collection config file in yaml format",
        default="collection_config.yaml",
    )
    argparser.add_argument(
        "--consent_yaml_config_file",
        "-co",
        help="Consent config file in yaml format",
        default="consent_config.yaml",
    )
    argparser.add_argument(
        "--url",
        "-u",
        help="URL for the REST API",
        default="http://localhost:8000/api/v1/collection",
    )

    args = argparser.parse_args()

    consent_boolean = args.consent_boolean

    if args.inputdir[0] == "/":
        inputdir = args.inputdir
    else:
        inputdir = os.path.join(os.path.dirname(__file__), args.inputdir)

    input_minimal_dataset_file = inputdir + "/" + args.minimal_dataset_input_file
    input_biobank_config_file = inputdir + "/" + args.biobank_yaml_config_file
    input_collection_config_file = inputdir + "/" + args.collection_yaml_config_file
    input_consent_config_file = inputdir + "/" + args.consent_yaml_config_file

    if args.outputdir[0] == "/":
        output_dir = args.outputdir
    else:
        output_dir = os.path.join(os.path.dirname(__file__), args.outputdir)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    type_of_input = args.minimal_dataset_type_of_input

    biobank_data = read_biobank_config_file(input_biobank_config_file)
    collection_data = read_collection_config_file(input_collection_config_file)
    if consent_boolean:
        consent_data = read_consent_config_file(input_consent_config_file)
    if type_of_input == "csv":
        minimal_data = read_minimal_dataset_from_csv_file(
            input_minimal_dataset_file, consent_boolean
        )
    elif type_of_input == "excel":
        minimal_data = read_minimal_dataset_from_excel_file(
            input_minimal_dataset_file, consent_boolean
        )
    elif type_of_input == "REST_API":
        url = args.url
        collection_id = collection_data["COLLECTION_ID"]
        minimal_data = read_minimal_dataset_from_rest_api(
            url, collection_id, consent_boolean
        )

    if minimal_data is None:
        print("No minimal dataset found")
        return

    if consent_boolean:
        source = BIMSSource(minimal_data, biobank_data, collection_data, consent_data)
    else:
        source = BIMSSource(minimal_data, biobank_data, collection_data)

    fhir_destination = FHIRDest(JsonFile(output_dir))
    c = Converter(source, fhir_destination, Converter.ORGANIZATION)
    c.run()

    fhir_destination = FHIRDest(JsonFile(output_dir))
    c = Converter(source, fhir_destination, Converter.CASE)
    c.run()


if __name__ == "__main__":
    main()
