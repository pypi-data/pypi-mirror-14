from __future__ import absolute_import

import os.path
import yaml
from .bases import MutableOverdub, Overdub
from collections import OrderedDict


class OverdubLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))

OverdubLoader.add_constructor('tag:yaml.org,2002:map', construct_mapping)
OverdubLoader.add_constructor('tag:yaml.org,2002:omap', construct_mapping)


class OverdubDumper(yaml.SafeDumper):
    pass


def represent_dict(dumper, data):
    return dumper.represent_mapping('tag:yaml.org,2002:map', data.items())

OverdubDumper.add_representer(OrderedDict, represent_dict)
OverdubDumper.add_representer(Overdub, represent_dict)


def load_from_file(*filenames, **kwargs):
    """Merge from various yaml files to obtain an overdubbed instance.
    """
    assert filenames, 'filename required'
    kwargs.setdefault('Loader', OverdubLoader)
    overdub = MutableOverdub()
    for filename in filenames:
        filename = os.path.expanduser(filename)
        if os.path.exists(filename):
            with open(filename) as file:
                data = yaml.load(file, **kwargs)
                overdub.merge(data)
    return overdub


def dump(data, **kwargs):
    kwargs.setdefault('Dumper', OverdubDumper)
    return yaml.dump(data, **kwargs)
