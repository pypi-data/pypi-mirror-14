from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class AtLeastOneRequiredValidator(object):
    message = _('At least one of the fields ({}) is required.')

    def __init__(self, *fields):
        self.fields = fields

    def __call__(self, attrs):
        passes = False
        for field in self.fields:
            if attrs.get(field):
                passes = True
                break

        if not passes:
            fields_str = ', '.join(self.fields)
            raise serializers.ValidationError(self.message.format(fields_str))
