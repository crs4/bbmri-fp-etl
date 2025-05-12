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

from abc import ABC, abstractmethod
from typing import Iterable
from . models import Aggregate, Case


class AbstractSource(ABC):

    @abstractmethod
    def get_cases_data(self) -> Iterable[Case]:
        """
        This method should return the data in the Biobank represented as Case
        Each Case contains data about the donor, his/her samples and events related to the donor and to the samples
        (e.g., Diagnosis Event, Sampling Event, etc...)
        :return: Iterable[Case]
        """

    @abstractmethod
    def get_biobanks_data(self) -> Iterable[Aggregate]:
        """
        This method should return data about Biobanks and Collections
        :return:  Iterable[Aggregate]
        """
