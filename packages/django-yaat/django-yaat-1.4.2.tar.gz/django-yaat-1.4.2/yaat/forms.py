# coding: utf-8

import json
import six
from copy import deepcopy

from django import forms
from django.conf import settings
from django.db import transaction

from yaat.models import Column


class HeadersField(forms.Field):
    def to_python(self, value):
        if isinstance(value, six.string_types):
            try:
                return json.loads(value)
            except ValueError:
                raise forms.ValidationError('Enter valid JSON')
        return value


class YaatValidatorForm(forms.Form):
    limit = forms.ChoiceField()
    offset = forms.IntegerField(min_value=0, initial=1)
    headers = HeadersField(required=False)

    def __init__(self, *args, request, columns, resource, **kwargs):
        self.resource = resource
        self.request = request
        self.user = getattr(self.request, getattr(settings, 'YAAT_REQUEST_ATTR', 'user'))
        self.columns = columns
        self.stateful_init = self.resource._meta.stateful_init
        self._column_fields = {column.key: i for i, column in enumerate(self.columns)}

        super().__init__(*args, **kwargs)

        if self.resource._meta.limit is None:
            self.fields['limit'] = forms.IntegerField(min_value=0, initial=10)
        else:
            self.fields['limit'].initial = self.resource._meta.limit
            self.fields['limit'].choices = [(_, _) for _ in self.resource._meta.limit_choices]

    def _get_column(self, name):
        retval = deepcopy(self.columns[self._column_fields[name]])
        retval.pk = None
        return retval

    def full_clean(self):
        super().full_clean()
        is_init = False

        if 'limit' in self._errors.keys():
            self.cleaned_data['limit'] = self.fields['limit'].initial
            del self._errors['limit']

        if 'offset' in self._errors.keys():
            self.cleaned_data['offset'] = self.fields['offset'].initial
            del self._errors['offset']

        if 'headers' in self._errors.keys():
            is_init = True
            self.cleaned_data['headers'] = self.columns
            del self._errors['headers']

        if self.stateful_init:
            session_key = self.session_key(self.resource)
            state = {
                'limit': int(self.cleaned_data['limit']),
                'offset': self.cleaned_data['offset']
            }

            if is_init:
                state = self.request.session.get(session_key, state)
                self.cleaned_data['limit'] = state['limit']
                self.cleaned_data['offset'] = state['offset']
            self.request.session[session_key] = state

    @classmethod
    def limit_dict(cls, request, resource):
        if resource._meta.stateful_init:
            state = request.session.get(cls.session_key(resource), None)
            if state:
                limit = state['limit']
            else:
                limit = resource._meta.limit
        else:
            limit = resource._meta.limit

        return {
            'limit': limit,
            'options': resource._meta.limit_choices
        }

    def invalidate_state(self):
        self.request.session.pop(self.session_key(self.resource), None)

    def reset_offset(self):
        self.cleaned_data['offset'] = self.fields['offset'].initial
        if self.stateful_init:
            session_key = self.session_key(self.resource)
            state = self.request.session.get(session_key, None)
            if state:
                state['offset'] = self.cleaned_data['offset']
                self.request.session[session_key] = state

    @staticmethod
    def session_key(resource):
        return 'yaat_init_state_' + resource._meta.resource_name

    def clean_headers(self):
        posted = self.cleaned_data['headers']

        headers = []

        try:
            for head in posted:
                try:
                    col = self._get_column(head['key'])
                    headers.append(col)

                    if col.ordering != Column.ORDER_DISALLOWED:
                        col.ordering = head['order']

                    if col.is_shown != Column.HIDE_DISALLOWED:
                        col.is_shown = not head['hidden']
                except KeyError as k:
                    raise forms.ValidationError('Missing property {0!r}'.format(k))
        except TypeError:
            raise forms.ValidationError('Missing headers')

        return headers

    def save(self):
        if self.columns == self.cleaned_data['headers']:
            return

        for i in range(0, len(self.cleaned_data['headers'])):
            self.cleaned_data['headers'][i].order = i + 1
            self.cleaned_data['headers'][i].user = self.user

        with transaction.atomic():
            col = self.cleaned_data['headers'][0]
            Column.objects.filter(user_id=col.user_id, resource=col.resource).delete()
            Column.objects.bulk_create(self.cleaned_data['headers'])
            Column.cached.bulk_create(self.cleaned_data['headers'])
