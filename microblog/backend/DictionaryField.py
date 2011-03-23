#-*- coding: utf-8 -*-

from django import forms
from django.core import exceptions
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

class DictionaryField(models.Field):
	description = _("Dictionary object")

	__metaclass__ = models.SubfieldBase

	def get_internal_type(self):
		return "TextField"

	def to_python(self, value):
		if value is None:
			return None
		elif value == "":
			return {}
		elif isinstance(value, basestring):
			try:
				return dict(simplejson.loads(value))
			except (ValueError, TypeError):
				raise exceptions.ValidationError(self.error_messages['invalid'])

		if isinstance(value, dict):
			return value
		else:
			return {}

	def get_prep_value(self, value):
		if not value:
			return ""
		elif isinstance(value, basestring):
			return value
		else:
			return simplejson.dumps(value)

	def value_to_string(self, obj):
		value = self._get_val_from_obj(obj)
		return self.get_prep_value(value)

	def clean(self, value, model_instance):
		value = super(DictionaryField, self).clean(value, model_instance)
		return self.get_prep_value(value)

	def formfield(self, **kwargs):
		defaults = {'widget': forms.Textarea}
		defaults.update(kwargs)
		return super(DictionaryField, self).formfield(**defaults)

# rules for South migrations tool (for version >= 0.7)
try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ["^carting\.fields\.DictionaryField"])
except ImportError:
	pass