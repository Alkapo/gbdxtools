"""
Main Interface to GBDX API.

Contact: kostas.stamatiou@digitalglobe.com
"""
from __future__ import absolute_import
from builtins import object
from future import standard_library

import json
import os
import logging

from gbdxtools.auth import Auth

from gbdxtools.s3 import S3
from gbdxtools.ordering import Ordering
from gbdxtools.workflow import Workflow
from gbdxtools.catalog import Catalog
from gbdxtools.vectors import Vectors
from gbdxtools.idaho import Idaho
try:
    from gbdxtools import IdahoImage, CatalogImage, LandsatImage
    with_pixel_access = True
except:
    print('Advanced pixel functionality disabled.  install gbdxtools[with_pixel_access] to enable.')
    with_pixel_access = False
from gbdxtools.task_registry import TaskRegistry
import gbdxtools.simpleworkflows


class Interface(object):

    def __init__(self, **kwargs):
        interface = Auth(**kwargs)
        self.gbdx_connection = interface.gbdx_connection
        self.root_url = interface.root_url
        self.logger = interface.logger

        # create and store an instance of the GBDX s3 client
        self.s3 = S3()

        # create and store an instance of the GBDX Ordering Client
        self.ordering = Ordering()

        # create and store an instance of the GBDX Catalog Client
        self.catalog = Catalog()

        # create and store an instance of the GBDX Workflow Client
        self.workflow = Workflow()

        # create and store an instance of the Idaho Client
        self.idaho = Idaho()

        self.vectors = Vectors()

        if with_pixel_access:
            self.catalog_image = CatalogImage
            self.idaho_image = IdahoImage
            self.landsat_image = LandsatImage

        self.task_registry = TaskRegistry()

    def Task(self, __task_name, **kwargs):
        return gbdxtools.simpleworkflows.Task(__task_name, **kwargs)

    def Workflow(self, tasks, **kwargs):
        return gbdxtools.simpleworkflows.Workflow(tasks, **kwargs)
