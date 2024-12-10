import datetime
import re

from bbmri_fp_etl.models import Sex, DiseaseOntology, SampleType, EventType

# Aggregate, RoleType, Biobank, DataCategory, CollectionType, Sex, \
#    Collection, AgeUnit, DiseaseOntology, SamplingEvent, SampleType


GENDER_MAP = {
    Sex.FEMALE: ['FEMALE', 8532],
    Sex.MALE: ['MALE', 8507],
    Sex.UNDIFFERENTIATED: ['AMBIGUOUS', 8570],
    Sex.UNKNOWN: ['UNKNOWN', 8551]
}

SPECIMEN_TYPE_MAP = {
    SampleType.AMNIOTIC_FLUID: ('Amniotic fluid specimen', 119373006, 4002223),
    SampleType.ASCITES_FLUID: ('Ascitic fluid sample', 309201001, 4206413),
    SampleType.BILE: ('Bile specimen', 119341000, 4001061),
    # impossibile to match. chosen one
    SampleType.BODY_CAVITY_FLUID: ('Specimen from abdominal cavity', 443654002, 40482757),
    # 443654002	443654002 Specimen from abdominal cavity
    # 443418008	40481476 Specimen from thoracic cavity
    # 309185002	4202637 Oral cavity sample
    SampleType.BONE: ('Bone biopsy sample', 309105004, 4205816),
    SampleType.BONE_MARROW_ASPIRATE: ('Specimen from bone marrow obtained by aspiration', 396997002, 4264108),
    # missing bone marrow plasma. set to bone marrow source
    # 119361006 Plasma specimen
    SampleType.BONE_MARROW_PLASMA: ('Bone marrow source', 167913002, 4043443),
    SampleType.BONE_MARROW_WHOLE: ('Bone marrow source', 167913002, 4043443),
    SampleType.BREAST_MILK: ('Human breast milk specimen', 430791000124104, 765496),
    SampleType.BRONCHOALVEOLAR_LAVAGE: ('Bronchoalveolar lavage fluid sample', 258607008, 4121345),
    SampleType.BUFFY_COAT: ('Buffy coat', 258587000, 4122286),
    # arguable
    # 441518000	40479563 Lymphoblastoid cell line specimen
    # 455541000124107 764477 Cultured cells specimen
    SampleType.CANCER_CELL_LINES: ('Lymphoblastoid cell line specimen', 441518000, 40479563),
    SampleType.CEREBROSPINAL_FLUID: ('Cerebrospinal fluid sample', 258450006, 4124259),
    SampleType.CORD_BLOOD: ('Cord blood specimen', 122556008, 4046835),
    SampleType.DENTAL_PULP: ('Dental tissue sample', 309187005, 4204330),
    # couldn't find a proper code
    # SampleType.DIGITAL_SAMPLE: ('derivative-other', 'Other Derivative'),
    SampleType.DNA: ('Deoxyribonucleic acid sample', 258566005, 4120355),
    SampleType.EMBRYO: ('Embryo biopsy sample', 258421004, 4124252),
    # taken from qualifier value not specimen in SNOMED
    SampleType.ENTIRE_BODY_ORGAN: ('Solid organ', 256885008, 4105056),
    SampleType.FECES: ('Stool specimen', 119339001, 4002879),
    SampleType.FETAL_TISSUE: ('Fetal cytologic material', 110968003, 4006654),
    SampleType.FIBROBLASTS: ('Fibroblast specimen', 119333000, 4001356),
    SampleType.GAS_EXHALED_BREATH: ('Breath sample', 803281000000109, 44806862),
    SampleType.GASTRIC_FLUID: ('Gastric fluid sample', 258459007, 4120336),
    SampleType.HAIR: ('Hair specimen', 119326000, 4001355),
    # couldn't find
    # SampleType.IMMORTALIZED_CELL_LINES: ('derivative-other', 'Other Derivative'),
    # couldn't find
    # SampleType.ISOLATED_MICROBES: ('derivative-other', 'Other Derivative'),
    SampleType.MENSTRUAL_BLOOD: ('Menstrual blood specimen', 119345009, 4002219),
    SampleType.NAIL: ('Nail specimen', 119327009, 4000618),
    SampleType.NASAL_WASHING: ('Nasal washings', 433871000124101, 762931),
    # not sure
    SampleType.OTHER: ('Specimen of unknown material', 119324002, 4002873),
    SampleType.PERICARDIAL_FLUID: ('Pericardial fluid specimen', 122571007, 4048848),
    # missing the mononuclear cells attribute
    SampleType.PBMC: ('Peripheral blood specimen', 122551003, 4047495),
    # not so sure
    SampleType.PROTEINS: ('Protein', 88878007, 4230216),
    SampleType.PLACENTA: ('Specimen from placenta', 119403008),
    SampleType.PLASMA: ('Plasma specimen', 119361006, 4000626),
    SampleType.PLEURAL_FLUID: ('Pleural fluid specimen', 418564007, 4302933),
    SampleType.POSTMORTEM_TISSUE: ('Postmortem tissue sample', 258484005, 4124267),
    # not sure
    SampleType.PRIMARY_CELLS: ('Cytologic material obtained from unspecified body', 430297000, 4332527),
    SampleType.RED_BLOOD_CELLS: ('Red blood cell fluid sample', 256912003, 4105828),
    SampleType.RNA: ('Ribonucleic acid sample', 382141000000103, 44792517),
    SampleType.SALIVA: ('Saliva specimen', 119342007, 4001062),
    SampleType.SEMEN: ('Semen specimen', 842461000000103, 44808818),
    SampleType.SERUM: ('Serum specimen', 119364003, 4001181),
    SampleType.SPUTUM: ('Sputum specimen', 119334006, 4002876),
    # missing the IPS induced pluripotent attribute
    # and derived from anatomic site not specimen domain
    SampleType.STEM_IPS_CELLS: ('Stem cell', 419758009, 4303257),
    SampleType.SWAB: ('Swab', 257261003, 4120698),
    SampleType.SWEAT: ('Sweat specimenr', 122569007, 4046838),
    SampleType.SYNOVIAL_FLUID: ('Synovial fluid specimenr', 119332005, 4002875),
    SampleType.TEARS: ('Tears specimenr', 122594008, 4046369),
    SampleType.TEETH: ('Specimen from tooth', 430319000, 4332635),
    SampleType.TISSUE_FFPE: ('Formalin-fixed paraffin-embedded tissue specimen', 441652008, 40480027),
    # coulnd't find. we have frozen or FFPE not both
    SampleType.TISSUE_FROZEN_OR_FFPE: ('Tissue specimen', 119376003, 4002890),
    SampleType.TISSUE_FROZEN: ('Frozen tissue section sample', 16214131000119104, 46270236),
    SampleType.UMBILICAL_CORD: ('Umbilical cord tissue sample', 258436001, 4122249),
    SampleType.URINE: ('Urine specimen', 122575003, 4046280),
    SampleType.URINE_SEDIMENT: ('Urine sediment specimen', 122567009, 4045758),
    SampleType.VITREOUS_FLUID: ('Vitreous fluid specimen', 119375004, 40282697),
    # missing 'whole' attribute
    SampleType.WHOLE_BLOOD_DRIED: ('Dried blood specimen', 119294007, 4000611),
    SampleType.WHOLE_BLOOD: ('Whole blood sample', 258580003, 4122283)
}

PROCEDURE_MAP = {
    # EventType.DIAGNOSIS goes to Condition
    # The others go to procedures
    EventType.SURGERY: ('operation on rectum', 74971002),
    EventType.RADIATION_THERAPY: ('radiation therapy for rectal cancer', 17360001000004105),
    EventType.TARGETED_THERAPY: ('drug therapy', 416608005),
    EventType.PHARMACOTHERAPY: ('chemotherapy', 367336001),
    EventType.RESPONSE_TO_THERAPY: ('Evaluating response to treatment', 225953001)
}


class OMOPDest:
    def __init__(self, serializer):
        self.output = serializer
        self._person_file = 'person.csv'
        self.condition_file = 'condition_occurence.csv'
        self.observation_period_file = 'observation_period.csv'
        self.specimen_file = 'specimen.csv'
        self._person_cols = ['person_id', 'gender_concept_id', 'year_of_birth', 'month_of_birth', 'day_of_birth',
                             'birth_datetime', 'race_concept_id', 'ethnicity_concept_id', 'location_id',
                             'provider_id', 'care_site_id', 'person_source_value', 'gender_source_value',
                             'gender_source_concept_id', 'race_source_value', 'race_source_concept_id',
                             'ethnicity_source_value', 'ethnicity_source_concept_id']
        self._condition_cols = ['condition_occurrence_id', 'person_id', 'condition_concept_id', 'condition_start_date',
                                'condition_start_datetime', 'condition_end_date', 'condition_end_datetime',
                                'condition_type_concept_id', 'condition_status_concept_id', 'stop_reason',
                                'provider_id', 'visit_occurrence_id', 'visit_detail_id', 'condition_source_value',
                                'condition_source_concept_id', 'condition_status_source_value']
        self._specimen_cols = ['specimen_id', 'person_id', 'specimen_concept_id', 'specimen_type_concept_id',
                               'specimen_date', 'specimen_datetime', 'quantity', 'unit_concept_id',
                               'anatomic_site_concept_id', 'disease_status_concept_id', 'specimen_source_id',
                               'specimen_source_value', 'unit_source_value', 'anatomic_site_source_value',
                               'disease_status_source_value']
        self._procedure_cols = ['procedure_occurrence_id', 'person_id', 'procedure_concept_id', 'procedure_date',
                                'procedure_datetime', 'procedure_end_date', 'procedure_end_datetime',
                                'procedure_type_concept_id',
                                'modifier_concept_id', 'quantity', 'provider_id', 'visit_occurrence_id',
                                'visit_detail_id',
                                'procedure_source_value', 'procedure_source_concept_id', 'modifier_source_value']
        self._observation_period_cols = ['observation_period_id', 'person_id', 'observation_period_start_date',
                                         'observation_period_end_date', 'period_type_concept_id']

    def _create_person_entry(self, donor):
        pe = [donor.id, GENDER_MAP[donor.gender][1]]

        if donor.birth_date is not None:
            birthdate = donor.birth_date.isoformat()
            bd = re.split('T|-', birthdate)
            year_of_birth = int(bd[0])
            month_of_birth = int(bd[1]) if len(bd) > 1 else ''
            day_of_birth = int(bd[2]) if len(bd) > 2 else ''
            bdatetime = birthdate
        else:
            year_of_birth = ''
            month_of_birth = ''
            day_of_birth = ''
            bdatetime = ''

        pe.extend([year_of_birth, month_of_birth, day_of_birth, bdatetime])
        race_concept_id = 0
        ethnicity_concept_id = ''
        location_id = ''
        provider_id = ''
        care_site_id = ''
        person_source_value = donor.id_source
        gender_source_value = GENDER_MAP[donor.gender][0]
        gender_source_concept_id = GENDER_MAP[donor.gender][1]
        race_source_value = ''
        race_source_concept_id = 0
        ethnicity_source_value = ''
        ethnicity_source_concept_id = 0
        pe.extend([race_concept_id, ethnicity_concept_id, location_id,
                   provider_id, care_site_id, person_source_value,
                   gender_source_value, gender_source_concept_id,
                   race_source_value, race_source_concept_id,
                   ethnicity_source_value, ethnicity_source_concept_id])

        return pe

    def _create_condition_occurrence_entry(self, donor, pe):
        co = []

        if donor.events is not None:

            for event in donor.events:
                if event.age_at_event is not None:
                    if event.event_type == EventType.DIAGNOSIS:
                        condition_start_datetime = ''
                        # sum birthday year and age at event to find date
                        if pe[2] != '':
                            by = int(pe[2])
                            m = 1
                            if event.age_at_event_unit == 'month':
                                m = 1 / 12.
                            year = pe[2] + m * event.age_at_event
                            d = datetime.date(year, 1, 1)
                        else:
                            # I know age at event but not birthday
                            # set datetime as age_at_event
                            if event.age_at_event_unit == 'month':
                                m = 1 / 12.
                            year = m * event.age_at_event
                            d = datetime.date(year, 1, 1)
                        if event.date_at_event is not None:
                            d = event.date_at_event
                        else:
                            d = datetime.date(1, 1, 1)
                        condition_occurrence_id = event.id
                        person_id = donor.id
                        if event.disease is not None:
                            condition_concept_id = event.disease.code
                            condition_source_value = event.disease.description
                            condition_source_concept_id = event.disease.code
                        else:
                            condition_concept_id = ''
                            condition_source_value = ''
                            condition_source_concept_id = ''
                        condition_start_date = d.isoformat()
                        condition_start_datetime = d
                        condition_end_date = ''
                        condition_end_datetime = ''
                        condition_type_concept_id = ''
                        if event.provenance is not None:
                            condition_status_source_value = event.provenance.description
                            condition_status_concept_id = event.provenance.code
                        else:
                            condition_status_source_value = ''
                            condition_status_concept_id = ''
                        stop_reason = ''
                        provider_id = ''
                        visit_occurrence_id = ''
                        visit_detail_id = ''

                        co.extend([condition_occurrence_id, person_id, condition_concept_id,
                                   condition_start_date, condition_start_datetime, condition_end_date,
                                   condition_end_datetime, condition_type_concept_id,
                                   condition_status_concept_id, stop_reason, provider_id,
                                   visit_occurrence_id, visit_detail_id, condition_source_value,
                                   condition_source_concept_id, condition_status_source_value])

        return [co, condition_status_concept_id]

    def _create_procedure_occurrence_entry(self, donor, pe):
        po = []

        if donor.events is not None:

            for event in donor.events:
                if event.age_at_event is not None and event.event_type != EventType.DIAGNOSIS:
                    procedure_start_datetime = ''
                    # sum birthday year and age at event to find date
                    if pe[2] != '':
                        m = 1
                        if event.age_at_event_unit == 'month':
                            m = 1 / 12.
                        year = pe[2] + m * event.age_at_event
                        d = datetime.date(year, 1, 1)
                    else:
                        # I know age at event but not birthday
                        # set datetime as age_at_event
                        if event.age_at_event_unit == 'month':
                            m = 1 / 12.
                        year = m * event.age_at_event
                        d = datetime.date(year, 1, 1)
                    if event.date_at_event is not None:
                        d = event.date_at_event
                    else:
                        d = datetime.date(1, 1, 1)
                    procedure_occurrence_id = event.id
                    person_id = donor.id
                    mappedprocedure = PROCEDURE_MAP[event.event_type]
                    procedure_concept_id = mappedprocedure[1]
                    procedure_source_value = mappedprocedure[0]
                    procedure_source_concept_id = mappedprocedure[1]
                    procedure_date = d.isoformat()
                    procedure_datetime = d
                    procedure_end_date = ''
                    procedure_end_datetime = ''
                    procedure_type_concept_id = ''
                    modifier_concept_id = ''
                    quantity = ''
                    provider_id = ''
                    visit_occurrence_id = ''
                    visit_detail_id = ''
                    modifier_source_value = ''
                    po.append([procedure_occurrence_id, person_id, procedure_concept_id,
                               procedure_date, procedure_datetime, procedure_end_date,
                               procedure_end_datetime, procedure_type_concept_id,
                               modifier_concept_id, quantity, provider_id,
                               visit_occurrence_id, visit_detail_id, procedure_source_value,
                               procedure_source_concept_id, modifier_source_value])

        return po

    def _create_specimen_entry(self, donor, samples):
        sa = []
        first_sample_acquisition = None
        if samples is not None:
            for sample in samples:
                specimen_id = sample.id
                person_id = donor.id
                specimen_concept_id = SPECIMEN_TYPE_MAP[sample.type][2]
                # OMOP4822448 581378 EHR Detail
                specimen_type_concept_id = 581378
                specimen_date = sample.creation_time.strftime("%Y-%m-%d")
                specimen_datetime = sample.creation_time
                if first_sample_acquisition is None or first_sample_acquisition < specimen_date:
                    first_sample_acquisition = specimen_date
                quantity = ''
                unit_concept_id = ''
                anatomic_site_concept_id = ''
                anatomic_site_source_value = ''
                # if SNOMED is used
                if sample.anatomical_site is not None:
                    anatomic_site_concept_id = sample.anatomical_site.code
                    anatomic_site_source_value = sample.anatomical_site.description

                disease_status_concept_id = ''
                disease_status_source_value = ''
                if sample.content_diagnosis is not None:
                    for cd in sample.content_diagnosis:
                        if cd.ontology == DiseaseOntology.ORPHANET:
                            dc = self._get_SNOMED_codes(cd.code)
                            disease_status_concept_id = dc[0]
                            disease_status_source_value = dc[1]
                        elif cd.ontology == 'SNOMED':
                            disease_status_concept_id = cd.code
                            disease_status_source_value = cd.description

                specimen_source_id = sample.id
                specimen_source_value = ''
                unit_source_value = ''
                # anatomic_site_source_value=''
                if sample.anatomical_site is not None:
                    anatomic_site_source_value = sample.anatomical_site.code

                sa.append([specimen_id, person_id, specimen_concept_id, specimen_type_concept_id, specimen_date,
                           specimen_datetime, quantity, unit_concept_id, anatomic_site_concept_id,
                           disease_status_concept_id, specimen_source_id, specimen_source_value, unit_source_value,
                           anatomic_site_source_value, disease_status_source_value])

        return [sa, first_sample_acquisition]

    def _create_observation_period_entry(self, donor, first_sample_acquisition, condition_status_concept_id):

        # observation_period_id coincide with donor.id (one per donor)
        op = []
        observation_period_id = donor.id
        person_id = donor.id
        observation_period_start_date = first_sample_acquisition
        observation_period_end_date = donor.last_update
        period_type_concept_id = condition_status_concept_id
        op.extend([observation_period_id, person_id, observation_period_start_date, observation_period_end_date,
                   period_type_concept_id])

        return op

    def _get_SNOMED_codes(self, disease_data):
        pass
        # snomed_codes = self.orphacodes.orphaToSNOMED(disease_data.code.split('_')[1])
        # if snomed_codes is not None:
        #     return [{
        #         'system': DiseaseOntology.ICD_10,
        #         'code': code['code']
        #     } for code in snomed_codes if code['mapping_type'] in ('E', 'BTNT')]
        # else:
        #     return []

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

        pe = self._create_person_entry(record.donor)

        [co, observation_concept_id] = self._create_condition_occurrence_entry(record.donor, pe)

        po = self._create_procedure_occurrence_entry(record.donor, pe)

        [se, first_sample_acquisition] = self._create_specimen_entry(record.donor, record.samples)

        op = self._create_observation_period_entry(record.donor, first_sample_acquisition, observation_concept_id)

        self.save('person', self._person_cols, pe)
        self.save('condition_occurrence', self._condition_cols, co)
        self.save('observation_period', self._observation_period_cols, op)
        for spec in se:
            self.save('specimen', self._specimen_cols, spec)
        for proc in po:
            self.save('procedure_occurrence', self._procedure_cols, proc)

    # def create_organizations(self, record: Aggregate):
    #     b = Bundle()
    #     b.type = 'transaction'
    #     b.entry = []

    #     resource = Organization()
    #     resource.id = self._transform_resource_id(record.id)
    #     resource.identifier = [Identifier({
    #         'system': BBMRI_ERIC_IDENTIFIER_SYSTEM,
    #         'value': record.id
    #     })]
    #     resource.name = record.name
    #     resource.acronym = record.acronym
    #     resource.extension = [Extension({
    #         'url': DESCRIPTION_EXTENSION,
    #         'valueString': record.description
    #     })]
    #     resource.telecom = [ContactPoint({
    #         'system': 'url',
    #         'value': t
    #     }) for t in record.url] if record.url is not None else None
    #     contacts = []
    #     for c in record.contact:
    #         contact = OrganizationContact()
    #         if c.role.type == RoleType.HEAD and c.role.description is not None:
    #             contact.extension = [Extension({
    #                 'url': CONTACT_ROLE_EXTENSION,
    #                 'valueString': c.role.description
    #             })]
    #         contact.purpose = CodeableConcept({
    #             'coding': [{
    #                 'system': CONTACT_POINT_PURPOSE,
    #                 'code': CONTACT_POINT_PURPOSE_ADMIN if c.role.type == RoleType.HEAD else CONTACT_POINT_PURPOSE_RESEARCH
    #             }]
    #         })
    #         contact.name = HumanName({
    #             'given': [c.name.given] if c.name is not None else None,
    #             'family': c.name.family if c.name is not None else None,
    #             'prefix': c.name.prefix if c.name is not None else None,
    #             'suffix': c.name.suffix if c.name is not None else None
    #         })
    #         contact.telecom = [ContactPoint({
    #             'system': t.type.value,
    #             'value': t.value
    #         }) for t in c.telecom]
    #         contacts.append(contact)
    #     resource.contact = contacts

    #     if isinstance(record, Biobank):
    #         resource.type = [CodeableConcept({
    #             'coding': [{
    #                 'code': 'Biobank'
    #             }]
    #         })]
    #         resource.meta = Meta({
    #             'profile': [BIOBANK_PROFILE]
    #         })
    #     elif isinstance(record, Collection):
    #         resource.type = [CodeableConcept({
    #             'coding': [{
    #                 'code': 'Collection'
    #             }]
    #         })]
    #         resource.meta = Meta({
    #             'profile': [COLLECTION_PROFILE]
    #         })
    #         resource.extension.extend(Extension({
    #             'url': COLLECTION_TYPE_EXTENSION,
    #             'valueCodeableConcept': {
    #                 'coding': [{
    #                     'system': COLLECTION_TYPE_CODE_SYSTEM,
    #                     'code': COLLECTION_TYPE_MAP[t][0],
    #                     'display': COLLECTION_TYPE_MAP[t][1]
    #                 }]
    #             }
    #         }) for t in record.type)

    #         resource.extension.extend(Extension({
    #             'url': DATA_CATEGORY_EXTENSION,
    #             'valueCodeableConcept': {
    #                 'coding': [{
    #                     'system': DATA_CATEGORY_CODE_SYSTEM,
    #                     'code': DATA_CATEGORY_MAP[c][0],
    #                     'display': DATA_CATEGORY_MAP[c][1]
    #                 }]
    #             }
    #         }) for c in record.data_category)
    #         resource.partOf = FHIRReference(
    #             {'reference': f'Organization/{self._transform_resource_id(record.biobank.id)}'})

    #     entry = BundleEntry()
    #     entry.resource = resource
    #     entry.request = BundleEntryRequest({
    #         'method': 'PUT',
    #         'url': f'Organization/{resource.id}'
    #     })
    #     b.entry.append(entry)
    #     self.save(resource.id, b.as_json())

    def save(self, file_name, header, csvdata):
        self.output.serialize(file_name, header, csvdata)
