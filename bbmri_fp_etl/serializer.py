# Copyright (c) CRS4 2024
#
# This file is part of BBMRI-FP-ETL.
#
# BBMRI-FP-ETL is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# BBMRI-FP-ETL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with BBMRI-FP-ETL. If not, see <https://www.gnu.org/licenses/>.

import csv
import json


class BaseOutput:
    def serialize(self, *args, **kwargs):
        raise NotImplementedError


class JsonFile(BaseOutput):

    def __init__(self, directory):
        self.output_dir = directory

    def serialize(self, file_name, obj):
        with open(f'{self.output_dir}/{file_name}.json', 'w') as f:
            json.dump(obj, f, indent=2)


class CSVFile(BaseOutput):

    def __init__(self, directory):
        self.output_dir = directory

    def serialize(self, file_name, header, rows):
        with open(f'{self.output_dir}/{file_name}.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)
