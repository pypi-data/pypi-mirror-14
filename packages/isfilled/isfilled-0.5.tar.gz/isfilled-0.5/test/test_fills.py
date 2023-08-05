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

class EmployeeFillsExcludeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['editor_of_choice','starting_date',]

class EditorForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['editor_of_choice']

class EmployeeFills(Filled):
    name = 'employee-fills'
    form = EmployeeFillsForm

class EmployeeExpertFills(Filled):
    form = EmployeeFillsForm
    fields = ['expert_in',]

class EmployeeExpertExcludeFills(Filled):
    form = EmployeeFillsForm
    exclude = ['expert_in',]

class FillsTest(BaseSuite):

    def test_fills(self):
        e = Employee.objects.create(name="Jared")

        f = Fill.objects.create(
                name="employee-hr",
                fill="test.test_fills.EmployeeFills",)

        self.assertEqual(e.check_fills().state, False)

        e.expert_in = "iOS"
        e.starting_date = datetime.date.today()
        e.editor_of_choice = 'vim'
        e.save()

        self.assertEqual(e.check_fills().state, True)

    def test_model_fills(self):
        e = Employee.objects.create(name="Jared")

        f = Fill.objects.create(
                name="employee",
                model="test.Employee",)

        self.assertEqual(e.check_fills().state, False)

        e.expert_in = "Android C++ C#"
        e.starting_date = datetime.date.today()
        e.editor_of_choice = 'vim'
        e.save()

        self.assertEqual(e.check_fills().state, True)

    def test_form_fills(self):
        e = Employee.objects.create(name="Jared")

        f = Fill.objects.create(
                name="employee",
                form="test.test_fills.EmployeeFillsForm",)

        self.assertEqual(e.check_fills().state, False)

        e.expert_in = "Android C++ C#"
        e.save()

        self.assertEqual(e.check_fills().state, False)

        e.starting_date = datetime.date.today()
        e.save()

        self.assertEqual(e.check_fills().state, False)

        e.editor_of_choice = 'vim'
        e.save()

        self.assertEqual(e.check_fills().state, True)

    def test_selected_form_fills(self):
        e = Employee.objects.create(name="Jared")

        f = Fill.objects.create(
                name="employee",
                form="test.test_fills.EditorForm",)

        self.assertEqual(e.check_fills().state, False)

        e.editor_of_choice = "emacs"

        self.assertEqual(e.check_fills().state, True)

    def test_selected_form_fills_noop(self):
        e = Employee.objects.create(name="Jared")

        f = Fill.objects.create(
                name="employee",
                form="test.test_fills.EditorForm",
                exclude="editor_of_choice")

        self.assertEqual(e.check_fills().state, True)

    def test_model_is_filled(self):
        e = Employee.objects.create(name="Jared")
        self.assertFalse(e.is_filled())
        e.expert_in = "Android C++ C#"
        e.starting_date = datetime.date.today()
        e.editor_of_choice = 'vim'
        self.assertTrue(e.is_filled())

    def test_model_is_filled_given_a_form(self):
        e = Employee.objects.create(name="Jared")
        self.assertFalse(e.is_filled(form=EmployeeFillsForm))
        e.expert_in = "Android C++ C#"
        e.starting_date = datetime.date.today()
        e.editor_of_choice = 'vim'
        self.assertTrue(e.is_filled(form=EmployeeFillsForm))

    def test_model_is_filled_given_a_form_exclude(self):
        e = Employee.objects.create(name="Jared")
        self.assertFalse(e.is_filled(form=EmployeeFillsExcludeForm))
        e.expert_in = "Android C++ C#"
        self.assertTrue(e.is_filled(form=EmployeeFillsExcludeForm))

    def test_model_is_filled_given_a_fill(self):
        e = Employee.objects.create(name="Jared")

        f = Fill.objects.create(fill="test.test_fills.EmployeeFills", exclude="editor_of_choice")

        self.assertFalse(e.is_filled(fill=EmployeeFills))

        e.expert_in = "Android C++ C#"
        e.starting_date = datetime.date.today()
        self.assertTrue(e.is_filled(fill=EmployeeFills))

    def test_model_is_filled_given_a_fill_expert_fields(self):
        e = Employee.objects.create(name="Jared")
        self.assertFalse(e.is_filled(fill=EmployeeExpertFills))
        e.expert_in = "food"
        self.assertTrue(e.is_filled(fill=EmployeeExpertFills))

    def test_model_is_filled_given_a_fill_expert_exclude(self):
        e = Employee.objects.create(name="Jared")
        self.assertFalse(e.is_filled(fill=EmployeeExpertExcludeFills))
        e.expert_in = "food"
        self.assertFalse(e.is_filled(fill=EmployeeExpertExcludeFills))
        e.editor_of_choice = 'vim'
        e.expert_in = None
        e.starting_date = datetime.date.today()
        self.assertTrue(e.is_filled(fill=EmployeeExpertExcludeFills))
