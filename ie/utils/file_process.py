from __future__ import print_function, division

import json
import pickle
from collections import OrderedDict


def read_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)


def write_json_file(obj, filepath):
    with open(filepath, 'w') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2))


def read_pkl_file(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)


def write_pkl_file(obj, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def serialize_value(o):
    return json.dumps(o)


def deserialize_value(text):
    return json.loads(text)