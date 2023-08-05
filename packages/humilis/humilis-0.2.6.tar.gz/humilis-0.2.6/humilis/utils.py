#!/usr/bin/env python
# -*- coding: utf-8 -*-


import abc
import contextlib
import logging
import os
import io
import glob
import json
import shutil
from sys import exit
import tempfile

import yaml
import jinja2

from humilis.exceptions import FileFormatError


def zipdir(path, ziph):
    """Adds all files under a path to a zip file."""
    for root, dirs, files in os.walk(path):
        for file in files:
            relroot = os.path.relpath(root, path)
            arcname = os.path.join(relroot, file)
            ziph.write(os.path.join(root, file), arcname=arcname)


def unroll_tags(tags):
    """Unrolls the tag list of a resource into a dictionary."""
    return {tag['Key']: tag['Value'] for tag in tags}


def roll_tags(tags):
    """Rolls a dictionary of tags into a list of tags Key/Value dicts."""
    return [{'Key': k, 'Value': v} for k, v in tags.items()]


@contextlib.contextmanager
def move_aside(path):
    """Moves a file or directory aside so that it can be processed in place."""
    tmpdir = tempfile.mktemp()
    if os.path.isfile(path):
        os.makedirs(tmpdir)
        tmpfile = os.path.join(tmpdir, os.path.basename(path))
        shutil.copy(path, tmpfile)
        yield tmpfile
    elif os.path.isdir(path):
        shutil.copytree(path, tmpdir)
        yield tmpdir
    shutil.rmtree(tmpdir)


def get_cf_name(env_name, layer_name, stage=None):
    """Produces the CF stack name for layer."""
    cf_name = "{}-{}".format(env_name, layer_name)
    if stage is not None:
        cf_name = "{}-{}".format(cf_name, stage)
    return cf_name


def reference_parser(name=None):
    def decorator(func):
        """Declares a function as a reference parser."""
        setattr(func, '__is_humilis_reference_parser__', True)
        setattr(func, '__humilis_reference_parser_name__', name)
        return func
    return decorator


class TemplateLoader:
    @abc.abstractmethod
    def load_section(self, *args, **kwargs):
        pass


class DirTreeBackedObject(TemplateLoader):
    """Loads data from a directory tree of files in various formats."""
    def __init__(self, basedir, logger=None):
        self.basedir = basedir
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    @abc.abstractproperty
    def params(self):
        pass

    def get_section_files(self, section):
        """
        Produces a list of all files associated with a dir tree section
        """
        # We read all files within the section dir, and merge them in a dict
        basedir = os.path.join(self.basedir, section)
        if os.path.isdir(basedir):
            # Section file(s) in their own directory
            section_files = []
            for (dirpath, dirnames, filenames) in os.walk(basedir):
                section_files += [os.path.join(dirpath, fn)
                                  for fn in filenames]
        else:
            section_files = list(glob.glob("{}/{}.*".format(self.basedir,
                                                            section)))

        return section_files

    def load_section(self, section, files=None, params={}):
        """
        Reads all files associated with a layer section (parameters, resources,
        mappings, etc)
        """
        if files is None:
            files = self.get_section_files(section)

        data = {}

        for filename in files:
            self.logger.info("Loading {}".format(filename))
            with open(filename, 'r') as f:
                this_data = self.load_file(filename, f, params=params)
            if this_data is None:
                continue

            if len(this_data) != 1:
                raise FileFormatError(filename, self.logger)

            data_key = list(this_data.keys())[0]
            if data_key.lower() != section.lower():
                self.logger.critical("Error parsing %s: %s was expected but "
                                     "%s was found" %
                                     (filename, section.title(), data_key))
                exit(1)
            for k, v in list(this_data.values())[0].items():
                data[k] = v

        return data

    def load_file(self, filename, f, params={}):
        filename, file_ext = os.path.splitext(filename)
        if file_ext in {'.yml', '.yaml'}:
            data = yaml.load(f)
        elif file_ext == '.json':
            data = json.load(f)
        elif file_ext == '.j2':
            template = jinja2.Template(f.read())
            data = template.render(**params)
            data = self.load_file(filename, io.StringIO(data))
        else:
            self.logger.critical("Error loading %s: unknown file "
                                 "extension %s" % filename, file_ext)
            exit(1)

        return data
