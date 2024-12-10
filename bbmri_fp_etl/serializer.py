import json
import csv
import os


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

    def serialize(self, file_name, header,obj):
        if os.path.isfile(f'{self.output_dir}/{file_name}.csv'):
            with open(f'{self.output_dir}/{file_name}.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                nr=[str(v) for v in obj]   
                writer.writerow(nr)     
        else:
            with open(f'{self.output_dir}/{file_name}.csv', 'w',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header) 
                nr=[str(v) for v in obj]   
                writer.writerow(nr)        



        # try:
        #     with open(f'{self.output_dir}/{file_name}.csv', 'a',newline='') as f:
        #         writer = csv.writer(f)
        #         for oline in obj:
        #             writer.writerow(oline)

        # except FileNotFoundError:
        #      with open(f'{self.output_dir}/{file_name}.csv', 'w',newline='') as f:
        #         writer = csv.writer(f)
        #         writer.writerow(header)    
        #         for oline in obj:
        #             writer.writerow(oline)
            