# Copyright (c) CRS4 2024
#
# This file is part of BBMRI-FP-ETL.
#
# BBMRI-FP-ETL is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# BBMRI-FP-ETL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with BBMRI-FP-ETL. If not, see <https://www.gnu.org/licenses/>.

from fhirclient.models.age import Age
from fhirclient.models.bundle import Bundle, BundleEntry, BundleEntryRequest
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.extension import Extension
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.meta import Meta
from fhirclient.models.organization import Organization, OrganizationContact
from fhirclient.models.patient import Patient
from fhirclient.models.specimen import Specimen, SpecimenCollection

from bbmri_fp_etl.destinations import transform_id
from bbmri_fp_etl.destinations.resources import Condition
from bbmri_fp_etl.models import Aggregate, RoleType, Biobank, DataCategory, CollectionType, Sex, \
    Collection, AgeUnit, DiseaseOntology, SamplingEvent, SampleType

PATIENT_PROFILE = 'https://fhir.bbmri.de/StructureDefinition/Patient'
CONDITION_PROFILE = 'https://fhir.bbmri.de/StructureDefinition/Condition'
SPECIMEN_PROFILE = 'https://fhir.bbmri.de/StructureDefinition/Specimen'
BIOBANK_PROFILE = 'https://fhir.bbmri.de/StructureDefinition/Biobank'
COLLECTION_PROFILE = 'https://fhir.bbmri.de/StructureDefinition/Collection'

CUSTODIAN_EXTENSION = 'https://fhir.bbmri.de/StructureDefinition/Custodian'
SAMPLE_DIAGNOSIS_EXTENSION = 'https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis'
STORAGE_TEMPERATURE_EXTENSION = 'https://fhir.bbmri.de/StructureDefinition/StorageTemperature'
DESCRIPTION_EXTENSION = 'https://fhir.bbmri.de/StructureDefinition/OrganizationDescription'
COLLECTION_TYPE_EXTENSION = 'https://fhir.bbmri.de/StructureDefinition/CollectionType'
DATA_CATEGORY_EXTENSION = 'https://fhir.bbmri.de/StructureDefinition/DataCategory'
CONTACT_ROLE_EXTENSION = 'https://fhir.bbmri.de/StructureDefinition/ContactRole'

COLLECTION_TYPE_CODE_SYSTEM = 'https://fhir.bbmri.de/CodeSystem/CollectionType'
DATA_CATEGORY_CODE_SYSTEM = 'https://fhir.bbmri.de/ValueSet/DataCategory'

BBMRI_ERIC_IDENTIFIER_SYSTEM = 'http://www.bbmri-eric.eu/'

CONTACT_POINT_PURPOSE = 'http://terminology.hl7.org/CodeSystem/contactentity-type'
CONTACT_POINT_PURPOSE_ADMIN = 'ADMIN'
CONTACT_POINT_PURPOSE_RESEARCH = 'RESEARCH'

FHIR_STORE_PATIENT_URL = '{base_url}/Patient'
FHIR_STORE_SPECIMEN_URL = '{base_url}/Specimen'
FHIR_STORE_CONDITION_URL = '{base_url}/Condition'

COLLECTION_TYPE_MAP = {
    CollectionType.BIRTH_COHORT: ('BIRTH_COHORT', 'Birth Cohort'),
    CollectionType.CASE_CONTROL: ('CASE_CONTROL', 'Case-Control'),
    CollectionType.COHORT: ('COHORT', 'Cohort'),
    CollectionType.CROSS_SECTIONAL: ('CROSS_SECTIONAL', 'Cross-sectional'),
    CollectionType.DISEASE_SPECIFIC: ('DISEASE_SPECIFIC', 'Disease specific'),
    CollectionType.HOSPITAL: ('HOSPITAL', 'Hospital'),
    CollectionType.IMAGE: ('IMAGE', 'Image collection'),
    CollectionType.LONGITUDINAL: ('LONGITUDINAL', 'Longitudinal'),
    CollectionType.NON_HUMAN: ('NON_HUMAN', 'Non-human'),
    CollectionType.OTHER: ('OTHER', 'Other'),
    CollectionType.POPULATION_BASED: ('POPULATION_BASED', 'Population-based'),
    CollectionType.PROSPECTIVE_COLLECTION: ('PROSPECTIVE_COLLECTION', 'Prospective collection'),
    CollectionType.QUALITY_CONTROL: ('QUALITY_CONTROL', 'Quality control'),
    CollectionType.RD: ('RD', 'Rare disease colleciton'),
    CollectionType.SAMPLE: ('SAMPLE', 'Sample collection'),
    CollectionType.TWIN_STUDY: ('TWIN_STUDY', 'Twin study'),
}

DATA_CATEGORY_MAP = {
    DataCategory.BIOLOGICAL_SAMPLES: ('BIOLOGICAL_SAMPLES', 'Biological Samples'),
    DataCategory.GENEALOGICAL_RECORDS: ('GENEALOGICAL_RECORDS', 'Genealogical records'),
    DataCategory.IMAGING_DATA: ('IMAGING_DATA', 'Imaging data'),
    DataCategory.MEDICAL_RECORDS: ('MEDICAL_RECORDS', 'Medical records'),
    DataCategory.NATIONAL_REGISTRIES: ('NATIONAL_REGISTRIES', 'National registries'),
    DataCategory.NAV: ('NAV', 'Not available'),
    DataCategory.OTHER: ('OTHER', 'other'),
    DataCategory.PHYSIOLOGICAL_BIOCHEMICAL_MEASUREMENTS: (
        'PHYSIOLOGICAL_BIOCHEMICAL_MEASUREMENTS', 'Physiological/Biochemical measurements'),
    DataCategory.SURVEY_DATA: ('SURVEY_DATA', 'Survey data')
}

GENDER_MAP = {
    Sex.FEMALE: 'female',
    Sex.MALE: 'male',
    Sex.UNDIFFERENTIATED: 'other',
    Sex.UNKNOWN: 'unknown'
}

SPECIMEN_TYPE_MAP = {
    SampleType.AMNIOTIC_FLUID: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.ASCITES_FLUID: ('ascites', 'Ascites'),
    SampleType.BILE: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.BODY_CAVITY_FLUID: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.BONE: ('derivative-other', 'Other Derivative'),
    SampleType.BONE_MARROW_ASPIRATE: ('bone marrow', 'Bone Marrow'),
    SampleType.BONE_MARROW_PLASMA: ('bone marrow', 'Bone Marrow'),
    SampleType.BONE_MARROW_WHOLE: ('bone marrow', 'Bone Marrow'),
    SampleType.BREAST_MILK: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.BRONCHOALVEOLAR_LAVAGE: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.BUFFY_COAT: ('buffy-coat', 'Buffy-Coat'),
    SampleType.CANCER_CELL_LINES: ('derivative-other', 'Other Derivative'),
    SampleType.CEREBROSPINAL_FLUID: ('csf-liquor', 'CSF/Liquor'),
    SampleType.CORD_BLOOD: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.DENTAL_PULP: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.DIGITAL_SAMPLE: ('derivative-other', 'Other Derivative'),
    SampleType.DNA: ('dna', 'DNA'),
    SampleType.EMBRYO: ('tissue-other', 'Other tissue storage'),
    SampleType.ENTIRE_BODY_ORGAN: ('derivative-other', 'Other Derivative'),
    SampleType.FECES: ('stool-faeces', 'Stool/Faeces'),
    SampleType.FETAL_TISSUE: ('tissue-other', 'Other tissue storage'),
    SampleType.FIBROBLASTS: ('derivative-other', 'Other Derivative'),  # TODO: check
    SampleType.GAS_EXHALED_BREATH: ('derivative-other', 'Other Derivative'),
    SampleType.GASTRIC_FLUID: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.HAIR: ('derivative-other', 'Other Derivative'),
    SampleType.IMMORTALIZED_CELL_LINES: ('derivative-other', 'Other Derivative'),
    SampleType.ISOLATED_MICROBES: ('derivative-other', 'Other Derivative'),
    SampleType.MENSTRUAL_BLOOD: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.NAIL: ('derivative-other', 'Other Derivative'),
    SampleType.NASAL_WASHING: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.OTHER: ('derivative-other', 'Other Derivative'),
    SampleType.PERICARDIAL_FLUID: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.PBMC: ('peripheral-blood-cells-vital', 'Peripheral blood mononuclear cells (PBMCs, viable)'),
    SampleType.PROTEINS: ('derivative-other', 'Other Derivative'),
    SampleType.PLACENTA: ('derivative-other', 'Other Derivative'),
    SampleType.PLASMA: ('blood-plasma', 'Plasma'),
    SampleType.PLEURAL_FLUID: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.POSTMORTEM_TISSUE: ('tissue-other', 'Other tissue storage'),
    SampleType.PRIMARY_CELLS: ('derivative-other', 'Other Derivative'),  # TODO: check
    SampleType.RED_BLOOD_CELLS: ('derivative-other', 'Other Derivative'),
    SampleType.RNA: ('rna', 'RNA'),
    SampleType.SALIVA: ('saliva', 'Saliva'),
    SampleType.SEMEN: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.SERUM: ('blood-serum', 'Blood Serum'),
    SampleType.SPUTUM: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.STEM_IPS_CELLS: ('derivative-other', 'Other Derivative'),
    SampleType.SWAB: ('swab', 'Swab'),
    SampleType.SWEAT: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.SYNOVIAL_FLUID: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.TEARS: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.TEETH: ('derivative-other', 'Other Derivative'),
    SampleType.TISSUE_FFPE: ('tissue-other', 'Other tissue storage'),
    SampleType.TISSUE_FROZEN_OR_FFPE: ('tissue-other', 'Other tissue storage'),
    SampleType.TISSUE_FROZEN: ('tissue-other', 'Other tissue storage'),
    SampleType.UMBILICAL_CORD: ('derivative-other', 'Other Derivative'),
    SampleType.URINE: ('urine', 'Urine'),
    SampleType.URINE_SEDIMENT: ('urine', 'Urine'),
    SampleType.VENOUS_BLOOD: ('whole-blood', 'Whole Blood'),
    SampleType.VITREOUS_FLUID: ('liquid-other', 'Other liquid biosample/storage'),
    SampleType.WHOLE_BLOOD_DRIED: ('dried-whole-blood', 'Dried Whole Blood'),
    SampleType.WHOLE_BLOOD: ('whole-blood', 'Whole Blood')
}

AGE_UNIT_MAP = {
    AgeUnit.YEARS: 'a',
    AgeUnit.MONTHS: 'mo',
    AgeUnit.WEEKS: 'wk',
    AgeUnit.DAYS: 'd'
}


class FHIRDest:
    def __init__(self, serializer):
        self.output = serializer

    @staticmethod
    def _create_patient_entry(data):
        patient = Patient()
        patient.meta = Meta({
            'profile': [PATIENT_PROFILE]
        })
        patient.id = transform_id(data.id)
        patient.identifier = [Identifier({
            'value': data.id
        })]
        if data.birth_date is not None:
            patient.birthDate = FHIRDate(data.birth_date.isoformat())
        patient.gender = GENDER_MAP[data.gender]

        patient_entry = BundleEntry()
        patient_entry.resource = patient
        patient_entry.request = BundleEntryRequest({
            'method': 'PUT',
            'url': f'Patient/{patient.id}'
        })
        return patient_entry

    def _create_condition_entry(self, patient_id, data):
        condition = Condition()
        condition.id = self._transform_resource_id(data.id)
        condition.meta = Meta({
            'profile': [CONDITION_PROFILE]
        })

        try:
            if data.age_at_event is not None:
                condition.onsetAge = Age({
                    'unit': AGE_UNIT_MAP[data.age_at_event_unit],
                    'value': data.age_at_event
                })
            elif data.date_at_event:
                osdt = FHIRDate(data.date_at_event)
                condition.onsetDateTime = osdt
                condition.recordedDate = osdt
        except TypeError:
            pass

        condition.code = CodeableConcept({
            'coding': [{
                'system': d.ontology,
                'code': d.code
            } for d in [data.disease.main_code] + data.disease.mapping_codes]
        })

        condition.subject = FHIRReference({'reference': f'Patient/{patient_id}'})

        condition_entry = BundleEntry()
        condition_entry.resource = condition
        condition_entry.request = BundleEntryRequest({
            'method': 'PUT',
            'url': f'Condition/{condition.id}'
        })
        return condition_entry

    def _create_specimen_entry(self, patient_id, data):
        specimen = Specimen()
        specimen.id = transform_id(data.id)
        specimen.identifier = [Identifier({
            'value': data.id
        })]
        specimen.meta = Meta({
            'profile': [SPECIMEN_PROFILE]
        })
        specimen.subject = FHIRReference({'reference': f'Patient/{patient_id}'})

        collected_date_time = None
        for event in data.events:
            if isinstance(event, SamplingEvent):
                collected_date_time = event.date_at_event

        if data.anatomical_site is not None:
            specimen.collection = SpecimenCollection({
                'bodySite': {
                    'coding': [{
                        'system': data.anatomical_site.ontology,
                        'code': data.anatomical_site.code,
                        'display': data.anatomical_site.free_text
                    }]
                },
                'collectedDateTime': collected_date_time
            })
        specimen_types = []
        if data.type is not None:  # some values are not mapped to obib so skip them
            # Adds the miabis value (as obib term)
            specimen_types.append({
                'system': data.type.value.ontology,
                'code': data.type.value.code,
                'display': data.type.value.free_text
            })
        # adds the SampleMaterialiType from
        specimen_types.append({
            'system': 'https://fhir.bbmri.de/CodeSystem/SampleMaterialType',
            'code': SPECIMEN_TYPE_MAP[data.type][0],
            'display': SPECIMEN_TYPE_MAP[data.type][1]
        })

        # adds any other additional type
        for t in data.additional_types:
            specimen_types.append({
                'system': t.ontology,
                'code': t.code,
                'display': t.free_text
            })
        specimen.type = CodeableConcept({
            'coding': specimen_types
        })

        disease_extensions = []
        if data.content_diagnosis is not None:
            for disease in data.content_diagnosis:
                disease_code = {
                    'coding': [{
                        'system': d.ontology,
                        'code': d.code
                    } for d in [disease.main_code] + disease.mapping_codes]
                }

                disease_extensions.append(
                    Extension({
                        'url': SAMPLE_DIAGNOSIS_EXTENSION,
                        'valueCodeableConcept': disease_code
                    }))
        try:
            specimen.extension = [Extension({
                'url': CUSTODIAN_EXTENSION,
                'valueReference': {
                    'identifier': {
                        'system': 'https://bbmri-eric.eu/',
                        'value': self._transform_resource_id(data.collection.id)
                    }
                }
            })] + disease_extensions
        except KeyError:
            specimen.extension = disease_extensions

        specimen_entry = BundleEntry()
        specimen_entry.resource = specimen
        specimen_entry.request = BundleEntryRequest({
            'method': 'PUT',
            'url': f'Specimen/{specimen.id}'
        })

        return specimen_entry

    def _create_specimens_entry(self, patient_id, data):
        return [self._create_specimen_entry(patient_id, specimen) for specimen in data if specimen is not None]

    def _create_conditions_entry(self, patient_id, diagnosis_event):
        return [self._create_condition_entry(patient_id, de) for de in diagnosis_event]

    @staticmethod
    def _transform_resource_id(id_):
        transformation = {
            "/": "-",
            "_": "-",
            "(": "",
            ")": "",
            ' ': '-',
            '+': '',
            ':': '-'
        }
        return id_.translate(str.maketrans(transformation))

    def create_participant(self, record):
        b = Bundle()
        b.type = 'transaction'
        b.entry = []

        patient_entry = self._create_patient_entry(record.donor)
        b.entry.append(patient_entry)

        condition_entries = self._create_conditions_entry(patient_entry.resource.id, record.donor.events)
        for ce in condition_entries:
            b.entry.append(ce)

        specimens_entries = self._create_specimens_entry(patient_entry.resource.id, record.samples)
        for se in specimens_entries:
            b.entry.append(se)

        self.save(patient_entry.resource.id, b.as_json())

    def create_organizations(self, record: Aggregate):
        b = Bundle()
        b.type = 'transaction'
        b.entry = []

        resource = Organization()
        resource.id = self._transform_resource_id(record.id)
        resource.identifier = [Identifier({
            'system': BBMRI_ERIC_IDENTIFIER_SYSTEM,
            'value': record.id
        })]
        resource.name = record.name
        resource.acronym = record.acronym
        resource.extension = [Extension({
            'url': DESCRIPTION_EXTENSION,
            'valueString': record.description
        })]
        resource.telecom = [ContactPoint({
            'system': 'url',
            'value': t
        }) for t in record.url] if record.url is not None else None
        contacts = []
        if record.contact:
            for c in record.contact:
                contact = OrganizationContact()
                if c.role.type == RoleType.HEAD and c.role.description is not None:
                    contact.extension = [Extension({
                        'url': CONTACT_ROLE_EXTENSION,
                        'valueString': c.role.description
                    })]
                contact.purpose = CodeableConcept({
                    'coding': [{
                        'system': CONTACT_POINT_PURPOSE,
                        'code': CONTACT_POINT_PURPOSE_ADMIN if c.role.type == RoleType.HEAD else CONTACT_POINT_PURPOSE_RESEARCH
                    }]
                })
                contact.name = HumanName({
                    'given': [c.name.given] if c.name is not None else None,
                    'family': c.name.family if c.name is not None else None,
                    'prefix': c.name.prefix if c.name is not None else None,
                    'suffix': c.name.suffix if c.name is not None else None
                })
                contact.telecom = [ContactPoint({
                    'system': t.type.value,
                    'value': t.value
                }) for t in c.telecom]
                contacts.append(contact)
        resource.contact = contacts

        if isinstance(record, Biobank):
            resource.type = [CodeableConcept({
                'coding': [{
                    'code': 'Biobank'
                }]
            })]
            resource.meta = Meta({
                'profile': [BIOBANK_PROFILE]
            })
        elif isinstance(record, Collection):
            resource.type = [CodeableConcept({
                'coding': [{
                    'code': 'Collection'
                }]
            })]
            resource.meta = Meta({
                'profile': [COLLECTION_PROFILE]
            })
            resource.extension.extend(Extension({
                'url': COLLECTION_TYPE_EXTENSION,
                'valueCodeableConcept': {
                    'coding': [{
                        'system': COLLECTION_TYPE_CODE_SYSTEM,
                        'code': COLLECTION_TYPE_MAP[t][0],
                        'display': COLLECTION_TYPE_MAP[t][1]
                    }]
                }
            }) for t in record.type)

            resource.extension.extend(Extension({
                'url': DATA_CATEGORY_EXTENSION,
                'valueCodeableConcept': {
                    'coding': [{
                        'system': DATA_CATEGORY_CODE_SYSTEM,
                        'code': DATA_CATEGORY_MAP[c][0],
                        'display': DATA_CATEGORY_MAP[c][1]
                    }]
                }
            }) for c in record.data_category)
            resource.partOf = FHIRReference(
                {'reference': f'Organization/{self._transform_resource_id(record.biobank.id)}'})

        entry = BundleEntry()
        entry.resource = resource
        entry.request = BundleEntryRequest({
            'method': 'PUT',
            'url': f'Organization/{resource.id}'
        })
        b.entry.append(entry)
        self.save(resource.id, b.as_json())

    def save(self, file_name, json_data):
        self.output.serialize(file_name, json_data)
