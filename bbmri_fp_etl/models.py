# Copyright (c) CRS4 2024
#
# This file is part of BBMRI-FP-ETL.
#
# BBMRI-FP-ETL is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# BBMRI-FP-ETL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with BBMRI-FP-ETL. If not, see <https://www.gnu.org/licenses/>.

"""
Modules with the models used between the sources and the destinations.
The destinations expect to handle data with the models defined here.
The sources have to output data using these models
"""
from datetime import datetime
from enum import Enum
from enum import StrEnum
from typing import List, Optional, NamedTuple

from pydantic import BaseModel, Field
from pydantic.types import date


class TelecomType(StrEnum):
    URL = 'url'
    EMAIL = 'email'
    PHONE = 'phone'


class RoleType(StrEnum):
    HEAD = 'head'
    RESEARCHER = 'researcher'


class CollectionType(StrEnum):
    BIRTH_COHORT = "BIRTH_COHORT"
    CASE_CONTROL = "CASE_CONTROL"
    COHORT = "COHORT"
    CROSS_SECTIONAL = "CROSS_SECTIONAL"
    DISEASE_SPECIFIC = "DISEASE_SPECIFIC"
    HOSPITAL = "HOSPITAL"
    IMAGE = "IMAGE"
    LONGITUDINAL = "LONGITUDINAL"
    NON_HUMAN = "NON_HUMAN"
    OTHER = "OTHER"
    POPULATION_BASED = "POPULATION_BASED"
    PROSPECTIVE_COLLECTION = "PROSPECTIVE_COLLECTION"
    QUALITY_CONTROL = "QUALITY_CONTROL"
    RD = "RD"
    SAMPLE = "SAMPLE"
    TWIN_STUDY = "TWIN_STUDY"


class Country(StrEnum):
    AU = 'AU'
    AT = 'AT'
    BY = 'BY'
    BE = 'BE'
    BG = 'BG'
    CA = 'CA'
    CN = 'CN'
    HR = 'HR'
    CY = 'CY'
    CZ = 'CZ'
    DK = 'DK'
    EG = 'EG'
    FI = 'FI'
    FR = 'FR'
    DE = 'DE'
    GR = 'GR'
    HU = 'HU'
    IE = 'IE'
    IL = 'IL'
    IT = 'IT'
    JP = 'JP'
    MT = 'MT'
    MX = 'MX'
    NL = 'NL'
    NZ = 'NZ'
    NO = 'NO'
    PL = 'PL'
    PT = 'PT'
    RS = 'RS'
    SI = 'SI'
    ES = 'ES'
    SE = 'SE'
    CH = 'CH'
    TR = 'TR'
    UA = 'UA'
    UK = 'UK'
    US = 'US'


class Sex(StrEnum):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    UNDIFFERENTIATED = 'D'


class AgeUnit(StrEnum):
    YEARS = 'years'
    MONTHS = 'months'
    WEEKS = 'weeks'
    DAYS = 'days'


class SampleTypeOntologyTuple(NamedTuple):
    ontology: str
    code: str
    free_text: str


class SampleType(Enum):
    AMNIOTIC_FLUID = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                             "http://purl.obolibrary.org/obo/OBI_0002500", "amniotic fluid specimen")
    ASCITES_FLUID = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                            "http://purl.obolibrary.org/obo/UBERON_0007795", "ascitic fluid")
    BILE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                   "http://purl.obolibrary.org/obo/OBI_0002501", "bile specimen")
    BODY_CAVITY_FLUID = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                "http://purl.obolibrary.org/obo/OBI_2000009", "bodily fluid specimen")
    BONE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                   "http://purl.obolibrary.org/obo/UBERON_0001474", "bone element")
    BONE_MARROW_ASPIRATE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                   "http://purl.obolibrary.org/obo/OBI_0002512", "bone marrow")
    BONE_MARROW_PLASMA = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                 "http://purl.obolibrary.org/obo/OBI_0002512", "bone marrow")
    BONE_MARROW_WHOLE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                "http://purl.obolibrary.org/obo/OBI_0002512", "bone marrow")
    BREAST_MILK = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                          "http://purl.obolibrary.org/obo/OBI_0002505", "milk specimen")
    BRONCHOALVEOLAR_LAVAGE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                     "http://purl.obolibrary.org/obo/OBI_0100067",
                                                     "bronchial alveolar lavage")
    BUFFY_COAT = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                         "http://purl.obolibrary.org/obo/OBIB_0000036", "buffy coat specimen")
    CANCER_CELL_LINES = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obi.owl",
                                                "http://purl.obolibrary.org/obo/OBI_0001906", "cancer cell line")
    CEREBROSPINAL_FLUID = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                  "http://purl.obolibrary.org/obo/OBI_0002502",
                                                  "cerebrospinal fluid specimen")
    CORD_BLOOD = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                         "http://purl.obolibrary.org/obo/OBI_2000012", "umbilical cord blood specimen")
    DENTAL_PULP = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                          "http://purl.obolibrary.org/obo/UBERON_0001754", "dental pulp")
    DIGITAL_SAMPLE = SampleTypeOntologyTuple(None, None, None)
    DNA = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                  "http://purl.obolibrary.org/obo/OBI_0001051", "DNA extract")
    EMBRYO = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                     "http://purl.obolibrary.org/obo/UBERON_0005291", "embryonic tissue")
    ENTIRE_BODY_ORGAN = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                                "http://purl.obolibrary.org/obo/UBERON_0000062", "organ")
    FECES = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                    "http://purl.obolibrary.org/obo/OBI_0002503", "feces specimen")
    FETAL_TISSUE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                           "http://purl.obolibrary.org/obo/UBERON_0005291", "embryonic tissue")
    FIBROBLASTS = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/cl.owl",
                                          "http://purl.obolibrary.org/obo/CL_0000057", "fibroblasts")
    GAS_EXHALED_BREATH = SampleTypeOntologyTuple(None, None, None)
    GASTRIC_FLUID = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                            "http://purl.obolibrary.org/obo/UBERON_0001971", "gastric juice")
    HAIR = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                   "http://purl.obolibrary.org/obo/OBI_0002517", "hair specimen")
    IMMORTALIZED_CELL_LINES = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obi.owl",
                                                      "http://purl.obolibrary.org/obo/CLO_0009828",
                                                      "immortal cell line")
    ISOLATED_MICROBES = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                "http://purl.obolibrary.org/obo/IDO_0000528", "pathogen")
    MENSTRUAL_BLOOD = SampleTypeOntologyTuple(None, None, None)
    NAIL = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                   "http://purl.obolibrary.org/obo/UBERON_0001705", "nail")
    NASAL_WASHING = SampleTypeOntologyTuple(None, None, None)
    PERICARDIAL_FLUID = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                "http://purl.obolibrary.org/obo/OBI_0002506",
                                                "pericardial fluid specimen")
    PBMC = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/cl.owl", "http://purl.obolibrary.org/obo/CL_2000001",
                                   "peripheral blood mononuclear cell")
    PLACENTA = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                       "http://purl.obolibrary.org/obo/OBI_0002513", "placenta specimen")
    PLASMA = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                     "http://purl.obolibrary.org/obo/OBI_0100016", "blood plasma specimen")
    PLEURAL_FLUID = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                            "http://purl.obolibrary.org/obo/OBI_0002515", "pleural fluid specimen")
    PRIMARY_CELLS = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/cl.owl",
                                            "http://purl.obolibrary.org/obo/CL_0000001", "primary cultured cell")
    POSTMORTEM_TISSUE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obi.owl",
                                                "http://purl.obolibrary.org/obo/OBI_0000902", "post-mortem specimen")
    PROTEINS = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                       "http://purl.obolibrary.org/obo/PR_000000001", "protein")
    RED_BLOOD_CELLS = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/cl.owl",
                                              "http://purl.obolibrary.org/obo/CL_0000232", "erythrocyte")
    RNA = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                  "http://purl.obolibrary.org/obo/OBI_0000880", "RNA extract")
    SALIVA = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                     "http://purl.obolibrary.org/obo/OBI_0002507", "saliva specimen")
    SEMEN = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                    "http://purl.obolibrary.org/obo/OBI_2000008", "semen specimen")
    SERUM = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                    "http://purl.obolibrary.org/obo/OBI_0100017", "blood serum specimen")
    SPUTUM = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                     "http://purl.obolibrary.org/obo/OBI_0002508", "sputum specimen")
    STEM_IPS_CELLS = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/cl.owl",
                                             "http://purl.obolibrary.org/obo/CL_0000034", "stem cells")
    SWAB = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                   "http://purl.obolibrary.org/obo/OBI_0002599", "swab specimen")
    SWEAT = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                    "http://purl.obolibrary.org/obo/OBI_0002509", "sweat specimen")
    SYNOVIAL_FLUID = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                             "http://purl.obolibrary.org/obo/OBI_0002510", "synovial specimn fluid")
    TEARS = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                    "http://purl.obolibrary.org/obo/UBERON_0001827", "secretion of lacrimal gland")
    TEETH = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                    "http://purl.obolibrary.org/obo/UBERON_0001091", "calcareus tooth")
    TISSUE_FROZEN_OR_FFPE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                    "http://purl.obolibrary.org/obo/OBI_0001472",
                                                    "specimen with known storage state")
    TISSUE_FROZEN = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                            "http://purl.obolibrary.org/obo/OBI_0000922", "Frozen Specimen")
    TISSUE_FFPE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                          "http://purl.obolibrary.org/obo/OBI_1200000", "FFPE Specimen")
    UMBILICAL_CORD = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/uberon.owl",
                                             "http://purl.obolibrary.org/obo/UBERON_0002331", "umbilical cord")
    URINE = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                    "http://purl.obolibrary.org/obo/OBI_0000651", "urine specimen")
    URINE_SEDIMENT = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                             "http://purl.obolibrary.org/obo/OBI_0000651", "urine specimen")
    VITREOUS_FLUID = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                             "http://purl.obolibrary.org/obo/OBI_0002511", "vitreous humor specimen")
    WHOLE_BLOOD = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                          "http://purl.obolibrary.org/obo/OBI_0000655", "blood specimen")
    WHOLE_BLOOD_DRIED = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                                "http://purl.obolibrary.org/obo/OBI_0000655", "blood specimen")
    VENOUS_BLOOD = SampleTypeOntologyTuple("http://purl.obolibrary.org/obo/obib.owl",
                                           "http://purl.obolibrary.org/obo/OBI_2000014", "venous blood specimen")
    OTHER = SampleTypeOntologyTuple(None, None, None)


class CollectionSampleType(StrEnum):
    """
    In MIABIS 3 Collections use an aggregated version of Material Type
    """
    BUFFY_COAT = 'BUFFY_COAT'
    CDNA = 'CDNA'
    CELL_LINES = 'CELL_LINES'
    DNA = 'DNA'
    FECES = 'FECES'
    MICRO_RNA = 'MICRO_RNA'
    NASAL_SWAB = 'NASAL_SWAB'
    NAV = 'NAV'
    OTHER = 'OTHER'
    PATHOGEN = 'PATHOGEN'
    PERIPHERAL_BLOOD_CELLS = 'PERIPHERAL_BLOOD_CELLS'
    PLASMA = 'PLASMA'
    RNA = 'RNA'
    SALIVA = 'SALIVA'
    SERUM = 'SERUM'
    THROAT_SWAB = 'THROAT_SWAB'
    TISSUE_FROZEN = 'TISSUE_FROZEN'
    TISSUE_PARAFFIN_EMBEDDED = 'TISSUE_PARAFFIN_EMBEDDED'
    TISSUE_STAINED = 'TISSUE_STAINED'
    URINE = 'URINE'
    WHOLE_BLOOD = 'WHOLE_BLOOD'


class DataCategory(StrEnum):
    ANTIBODIES = "ANTIBODIES"
    BIOLOGICAL_SAMPLES = "BIOLOGICAL_SAMPLES"
    BLOOD = "BLOOD"
    CLINICAL_SYMPTOMS = "CLINICAL_SYMPTOMS"
    CT = "CT"
    DiseaseDuration = "DiseaseDuration"
    GENEALOGICAL_RECORDS = "GENEALOGICAL_RECORDS"
    IMAGING_DATA = "IMAGING_DATA"
    MEDICAL_RECORDS = "MEDICAL_RECORDS"
    NATIONAL_REGISTRIES = "NATIONAL_REGISTRIES"
    NAV = "NAV"
    OTHER = "OTHER"
    PHYSIOLOGICAL_BIOCHEMICAL_MEASUREMENTS = "PHYSIOLOGICAL_BIOCHEMICAL_MEASUREMENTS"
    SURVEY_DATA = "SURVEY_DATA"
    TREATMENT_PROTOCOL = "TREATMENT_PROTOCOL"


class StorageTemperature(StrEnum):
    TEMP_18_TO_35 = "temperature-18to-35"
    TEMP_60_TO_85 = "temperature-60to-85"
    TEMP_2_TO_10 = "temperature2to10"
    LN = "temperatureLN"
    ROOM = "temperatureRoom"
    OTHER = "temperatureOther"


class DiseaseOntology(StrEnum):
    ORPHANET = 'http://www.orpha.net/ORDO/'
    ICD_10 = 'http://hl7.org/fhir/sid/icd-10'
    SNOMED = 'https://www.snomed.org/'


class AnatomicalSiteOntology(StrEnum):
    UBERON = 'http://purl.obolibrary.org/obo/uberon.owl'
    ICD_O_3 = 'icd-3'
    SNOMED = 'https://www.snomed.org/'


class Name(BaseModel):
    given: str
    family: str
    prefix: Optional[str] = Field(default=None)
    suffix: Optional[str] = Field(default=None)


class Telecom(BaseModel):
    type: TelecomType
    value: str


class Address(BaseModel):
    country: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    street: Optional[str] = Field(default=None)
    zip: Optional[str] = Field(default=None)


class ContactRole(BaseModel):
    type: RoleType
    description: Optional[str] = Field(default=None)


class Contact(BaseModel):
    name: Optional[Name] = Field(default=None)
    telecom: List[Telecom] = Field(default=None)
    address: Optional[Address] = Field(default=None)
    role: ContactRole


class DiseaseOntologyCode(BaseModel):
    ontology: DiseaseOntology
    ontology_version: Optional[str] = Field(default=None)
    code: str
    description: Optional[str] = Field(default=None)
    free_text: Optional[str] = Field(default=None)


class AnatomicalSiteOntologyCode(BaseModel):
    ontology: AnatomicalSiteOntology
    ontology_version: Optional[str] = Field(default=None)
    code: str
    description: Optional[str] = Field(default=None)
    free_text: Optional[str] = Field(default=None)


class SampleTypeOntologyCode(BaseModel):
    ontology: str
    ontology_version: Optional[str] = Field(default=None)
    code: str
    description: Optional[str] = Field(default=None)
    free_text: Optional[str] = Field(default=None)


class Disease(BaseModel):
    main_code: DiseaseOntologyCode
    mapping_codes: Optional[List[DiseaseOntologyCode]]


class Aggregate(BaseModel):
    id: str
    acronym: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    url: Optional[List[str]] = Field(default_factory=list)
    contact: Optional[List[Contact]] = Field(default_factory=list)
    country: Optional[Country] = Field(default=None)


class Biobank(Aggregate):
    jurystic_person: str


class Collection(Aggregate):
    sex: Optional[List[Sex]] = Field(default_factory=list)
    age_low: Optional[int] = Field(default=None)
    age_high: Optional[int] = Field(default=None)
    age_unit: Optional[List[AgeUnit]] = Field(default=None)
    data_category: Optional[List[DataCategory]] = Field(default=None)
    material_type: Optional[List[CollectionSampleType]] = Field(default=None)
    storage_temperature: Optional[List[StorageTemperature]] = Field(default=None)
    type: Optional[List[CollectionType]] = Field(default=None)
    disease: Optional[List[DiseaseOntologyCode]] = Field(default=None)
    biobank: Optional[Biobank] = Field(default=None)


class EventType(StrEnum):
    DIAGNOSIS = 'diagnosis'
    SURGERY = 'surgery'
    RADIATION_THERAPY = 'radiation therapy'
    TARGETED_THERAPY = 'targeted therapy'
    PHARMACOTHERAPY = 'pharmacotherapy'
    RESPONSE_TO_THERAPY = 'response to therapy'


class Event(BaseModel):
    id: str
    age_at_event: Optional[int] = Field(default=None)
    age_at_event_unit: Optional[AgeUnit] = Field(default=None)
    date_at_event: Optional[date] = Field(default=None)
    event_type: Optional[EventType] = Field(default=None)


class Donor(BaseModel):
    id: str
    id_source: Optional[str] = Field(default=None)
    gender: Sex
    birth_date: Optional[date] = Field(default=None)
    last_update: Optional[date] = Field(default=None)
    events: Optional[List[Event]] = Field(default_factory=list)


class Sample(BaseModel):
    id: str
    type: SampleType  # the MIABIS Sample Type
    additional_types: List[SampleTypeOntologyCode] = Field(
        default_factory=list)  # A list of other Sample Type if needed
    content_diagnosis: Optional[List[Disease]] = Field(default_factory=list)
    creation_time: Optional[datetime] = Field(default=None)
    events: List[Event]
    collection: Collection
    anatomical_site: Optional[AnatomicalSiteOntologyCode] = Field(default=None)


class StatusOntology(StrEnum):
    OMOP = 'https://athena.ohdsi.org/search-terms/terms?domain=Condition+Status&standardConcept=Standard'


class StatusOntologyCode(BaseModel):
    ontology: str
    ontology_version: Optional[str] = Field(default=None)
    code: str
    description: Optional[str] = Field(default=None)
    free_text: Optional[str] = Field(default=None)


class DiagnosisEvent(Event):
    disease: Disease
    provenance: Optional[StatusOntologyCode] = Field(default=None)


class SamplingEvent(Event):
    pass


class Case(BaseModel):
    donor: Donor
    samples: List[Sample]
