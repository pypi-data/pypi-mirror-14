# -*- coding: utf-8 -*-
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.test import TestCase, TransactionTestCase, override_settings
from django.test.client import Client
from django.contrib.auth.models import Group, User
from django import forms

from isfilled.models import Fill
from isfilled.fills import FillsMixin, Filled

import os, logging, datetime
logging.basicConfig(level=logging.DEBUG)

class BaseSuite(TransactionTestCase):
    pass

class Employee(models.Model, FillsMixin):
    name = models.CharField(max_length=255)
    expert_in = models.CharField(max_length=255, blank=True, null=True)
    starting_date = models.DateField(blank=True, null=True)
    editor_of_choice = models.CharField(max_length=255, blank=True, null=True)

class EmployeeFillsForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = []

class EmployeeFills(Filled):
    form = EmployeeFillsForm

class FillsTest(BaseSuite):
    def test_form_fills(self):
        e = Employee.objects.create(name="Jared")

        f = Fill.objects.create(
                name="employee-hr",
                fill="test.test_fills.EmployeeFills",)

        state, ctx = e.check_fills()
        self.assertEqual(state, False)

        e.expert_in = "iOS"
        e.starting_date = datetime.date.today()
        e.editor_of_choice = 'vim'
        e.save()

        state, ctx = e.check_fills()
        self.assertEqual(state, True)

    def test_model_fills(self):
        e = Employee.objects.create(name="Jared")

        f = Fill.objects.create(
                name="employee",
                model="test.Employee",)

        state, ctx = e.check_fills()
        self.assertEqual(state, False)

        e.expert_in = "Android C++ C#"
        e.starting_date = datetime.date.today()
        e.editor_of_choice = 'vim'
        e.save()

        state, ctx = e.check_fills()
        self.assertEqual(state, True)

