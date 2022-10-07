import json
import os
from pathlib import Path
from pyexcel_xlsx import get_data



def read_xlsx(filename: str, **kwargs):
    path_to_file = os.path.join(Path(__file__).absolute().parent.parent, "in", filename)
    print(path_to_file)
    data = json.loads(json.dumps(get_data(path_to_file, **kwargs)))

    return data
