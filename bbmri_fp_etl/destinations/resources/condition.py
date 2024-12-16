# Copyright (c) CRS4 2024
#
# This file is part of BBMRI-FP-ETL.
#
# BBMRI-FP-ETL is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# BBMRI-FP-ETL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with BBMRI-FP-ETL. If not, see <https://www.gnu.org/licenses/>.

from fhirclient.models.condition import Condition as FHIRCondition
from fhirclient.models import fhirdate


class Condition(FHIRCondition):

    resource_type = "Condition"

    def __init__(self, jsondict=None, strict=True):
        self.recordedDate = None
        """Date record was first recorded.
        Type `FHIRDate` (represented as `str` in JSON). """

        super(Condition, self).__init__(jsondict=jsondict, strict=strict)

    def elementProperties(self):
        js = super(Condition, self).elementProperties()
        js.extend([
            ("recordedDate", "recordedDate", fhirdate.FHIRDate, False, None, False),
        ])
        return js
