# -*- coding: utf-8 -*-
"""
Admin for the csv_generator app
"""
from __future__ import unicode_literals
from csv_generator.forms import CsvGeneratorForm, CsvGeneratorColumnForm
from csv_generator.forms import CsvGeneratorColumnFormSet
from csv_generator.models import CsvGenerator, CsvGeneratorColumn
from csv_generator.views import CsvExportView
from csv_generator.admin import CsvExportAdmin
from csv_generator.tests.models import TestModel
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


admin.site.register(TestModel, CsvExportAdmin)
