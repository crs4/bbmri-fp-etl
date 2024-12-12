from abc import ABC, abstractmethod


class AbstractSource(ABC):

    @abstractmethod
    def get_cases_data(self):
        """
        This method should return the data in the Biobank represented as Case
        Each Case contains data about the donor, his/her samples and events related to the donor and to the samples
        (e.g., Diagnosis Event, Sampling Event, etc...)
        :return: a list of Case
        """

    def get_biobanks_data(self):
        """
        This method should return data about Biobanks and Collections
        :return:
        """


