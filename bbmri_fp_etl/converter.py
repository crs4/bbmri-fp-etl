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

import logging

logger = logging.getLogger('bbmri_fp_etl')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


class Converter:
    ORGANIZATION = 'organization'
    CASE = 'case'

    def __init__(self, source, destination, resource_type):
        assert resource_type in (self.ORGANIZATION, self.CASE)
        self.source = source
        self.destination = destination
        self.resource_type = resource_type

    def run(self):
        try:
            logger.debug('Getting %s(s) from %s', self.resource_type, self.source)
            if self.resource_type == self.CASE:
                records = self.source.get_cases_data()
            else:
                records = self.source.get_biobanks_data()
        except Exception as e:
            logger.error(e)
            raise e
        else:
            logger.debug('Done getting data. Found %s %s(s)', len(records), self.resource_type)

        logger.debug('Generating outputs')
        for record in records:
            if self.resource_type == self.CASE:
                self.destination.create_participant(record)
            else:
                self.destination.create_organizations(record)

        logger.debug('found %s %s(s)', len(records), self.resource_type)
