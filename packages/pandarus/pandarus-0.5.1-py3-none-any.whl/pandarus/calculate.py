# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from eight import *

from .maps import Map
from .matching import matchmaker
from .export import json_exporter, csv_exporter, pickle_exporter

export_functions = {
    "json": json_exporter,
    "csv": csv_exporter,
    "pickle": pickle_exporter
}


class Pandarus(object):
    """Controller for all actions."""
    def __init__(self, from_filepath=None, to_filepath=None,
            from_metadata={}, to_metadata={}):
        self.from_map = Map(from_filepath, **from_metadata)
        if to_filepath is not None:
            self.to_map = Map(to_filepath, **to_metadata)

    def match(self, cpus=None):
        self.data = matchmaker(
            self.from_map.filepath,
            self.to_map.filepath,
            cpus=cpus,
        )
        return self.data

    def areas(self, cpus=None):
        self.data = matchmaker(
            self.from_map.filepath,
            None,
            cpus=cpus,
        )
        return self.data

    def add_from_map_fieldname(self, fieldname=None):
        """Turn feature integer indices into actual field values using field `fieldname`"""
        if not self.data:
            raise ValueError("Must match maps first")
        mapping_dict = self.from_map.get_fieldnames_dictionary(fieldname)
        self.data = {
            (mapping_dict[k[0]], k[1]): v
            for k, v in self.data.items()
        }

    def add_to_map_fieldname(self, fieldname=None):
        """Turn feature integer indices into actual field values using field `fieldname`"""
        if not self.data:
            raise ValueError("Must match maps first")
        mapping_dict = self.to_map.get_fieldnames_dictionary(fieldname)
        self.data = {
            (k[0], mapping_dict[k[1]]): v
            for k, v in self.data.items()
        }

    def add_areas_map_fieldname(self, fieldname=None):
        """Turn feature integer indices into actual field values using field `fieldname`"""
        if not self.data:
            raise ValueError("Must match maps first")
        mapping_dict = self.from_map.get_fieldnames_dictionary(fieldname)
        self.data = {mapping_dict[k]: v for k, v in self.data.items()}

    def export(self, filepath, kind="json", compress=True):
        exporter = export_functions[kind]
        if kind in {'csv', 'json'} and isinstance(list(self.data.keys())[0], tuple):
            self.unpack_tuples()
        else:
            self.unpack_dictionary()
        return exporter(self.data, filepath, compressed=compress)

    def unpack_tuples(self):
        self.data = [(k[0], k[1], v) for k, v in self.data.items()]

    def unpack_dictionary(self):
        self.data = [(k, v) for k, v in self.data.items()]
