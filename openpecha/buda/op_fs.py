from openpecha.buda.op import Openpecha
from os import walk
import pathlib
import yaml

class OpenpechaFS(Openpecha):
    """
    A class inheriting from the Openpecha class that defines the path to the local .opf folder

    TODO: perhaps this should be renamed OPF and be moved into serializers/ as it's really a reader/serializer for an .opf folder

    TODO: we could also implement write functions. Basically there would be:
       - readFromPath(path): would more or less replace the current __init__
       - writeToPath(path): would write the content to a path (removing all files that used to be there)
    """
    def __init__(self, lname, path_to_opf):
        Openpecha.__init__(self, lname)
        self.path = path_to_opf

    def get_rev(self):
        return None

    def list_paths(self):
        """
        Getting all the files in the directory
        """
        files = []
        for (dirpath, dirnames, filenames) in walk(self.path):
            for file in filenames:
                files.append(f'{dirpath}/{file}'.replace(self.path, ""))

        return files

    def read_file_content(self, oppath):
        with open(f'{opf}/'+oppath) as f:
            return f.read()

    def read_file_content_yml(self, oppath):
        with open(f'{opf}/'+oppath) as f:
            return yaml.safe_load(file)
