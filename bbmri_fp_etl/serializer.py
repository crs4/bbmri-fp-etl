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
