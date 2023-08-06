# coding: utf-8

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ordered_model.models import OrderedModel


class CachedManager(models.Manager):
    KEY_TEMPLATE = '%d_%s_columns'

    def filter(self, resource, user):
        key = self.KEY_TEMPLATE % (user.pk, resource)

        value = cache.get(key)

        if value is None:
            value = list(Column.objects.filter(resource=resource, user=user))
            cache.set(key, value)

        return value

    def bulk_create(self, columns):
        key = self.KEY_TEMPLATE % (columns[0].user_id, columns[0].resource)
        cache.set(key, columns)


class Column(OrderedModel):
    ORDER_DISALLOWED = None
    UNORDERED = 0
    ASC = 1
    DESC = 2

    HIDE_DISALLOWED = None

    ORDER_CHOICES = (
        (ORDER_DISALLOWED, _('Ordering disallowed')),
        (UNORDERED, _('Unordered')),
        (ASC, _('Ascending')),
        (DESC, _('Descending'))
    )

    user = models.ForeignKey(getattr(settings, 'YAAT_FOREIGN_KEY', settings.AUTH_USER_MODEL), verbose_name=_('User'), related_name='columns')

    resource = models.CharField(max_length=64, verbose_name=_('Resource name'))
    key = models.CharField(max_length=64, verbose_name=_('Column key'))
    is_shown = models.NullBooleanField(default=True, verbose_name=_('Show field'))
    ordering = models.PositiveSmallIntegerField(choices=ORDER_CHOICES, default=UNORDERED, null=True,
                                                verbose_name=_('Field order'))
    is_virtual = models.BooleanField(default=True)

    order_with_respect_to = ('resource', 'user')

    objects = models.Manager()
    cached = CachedManager()

    class Meta:
        unique_together = ('resource', 'user', 'key')

    def __init__(self, *args, **kwargs):
        self.value = kwargs.pop('value', None)
        super().__init__(*args, **kwargs)

        if self.is_virtual:
            self.ordering = self.ORDER_DISALLOWED

    def __eq__(self, other):
        left = [self.user_id, self.resource, self.key, self.order, self.is_shown, self.ordering]
        right = [other.user_id, other.resource, other.key, other.order, other.is_shown, other.ordering]

        return left == right

    def get_ordering(self):
        if self.is_shown is False:
            return None

        if self.ordering == self.ASC:
            return self.key
        elif self.ordering == self.DESC:
            return '-' + self.key

    def flatten(self):
        if self.value is None:
            raise ValueError('Cannot flatten because self.value is None')

        data = {
            'key': self.key,
            'value': str(self.value)
        }

        if self.ordering != self.ORDER_DISALLOWED:
            data['order'] = self.ordering

        if self.is_shown is not None:
            data['hidden'] = not self.is_shown

        return data
