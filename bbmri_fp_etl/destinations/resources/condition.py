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
