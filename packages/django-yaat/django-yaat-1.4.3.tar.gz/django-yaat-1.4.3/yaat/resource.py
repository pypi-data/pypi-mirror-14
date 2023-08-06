# coding: utf-8

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage
from django.apps import apps
from restify.http import status
from restify.http.response import ApiResponse
from restify.resource import Resource
from restify.resource.model import ModelResourceMixin

from .forms import YaatValidatorForm
from .meta import YaatModelResourceMeta
from .models import Column


class YaatModelResource(Resource, ModelResourceMixin, metaclass=YaatModelResourceMeta):
    VALIDATOR_FORM = YaatValidatorForm

    @classmethod
    def invalidate_column_cache(cls, user):
        user_class = apps.get_model(getattr(settings, 'YAAT_FOREIGN_KEY', settings.AUTH_USER_MODEL))
        if not isinstance(user, user_class):
            raise TypeError('expected {0!r} received {1!r} instead'.format(user_class, user.__class__))

        key = Column.cached.KEY_TEMPLATE % (user.pk, cls._meta.resource_name)
        cache.delete(key)

    def get_columns(self):
        columns = []

        for c in self._meta.columns:
            if isinstance(c, str):
                field = self._meta.model._meta.get_field(c)
                column = Column(key=field.name,
                                value=field.verbose_name,
                                resource=self._meta.resource_name,
                                is_virtual=False)
                columns.append(column)
            elif isinstance(c, Column):
                c.resource = self._meta.resource_name
                columns.append(c)
            else:
                raise TypeError('Column item is expected to be string or Column')

        return columns

    def get_stateful_columns(self, columns):
        retval = []

        mapper = {columns[i].key: i for i in range(0, len(columns))}

        if self._meta.stateful and not isinstance(self.request.user, AnonymousUser):
            column_user = getattr(self.request, getattr(settings, 'YAAT_REQUEST_ATTR', 'user'))
            retval = Column.cached.filter(resource=self._meta.resource_name, user=column_user)

        for col in retval:
            col.value = columns[mapper[col.key]].value

        return retval

    def get_queryset_order_keys(self, columns):
        keys = []
        for column in columns:
            ordering = column.get_ordering()
            if ordering:
                keys.append(ordering)
        return keys

    def get_queryset(self, columns):
        order_keys = self.get_queryset_order_keys(columns)
        return super().get_queryset().order_by(*order_keys).all()

    def get_page(self, qs, limit, page_number=1):
        paginator = Paginator(qs, limit)
        return paginator.page(page_number)

    def row_hook(self, row, obj):
        return row

    def get_rows(self, page, cols, **kwargs):
        rows = []
        for obj in page:
            cells = []
            for col in cols:
                if col.is_shown != False:
                    value = getattr(obj, col.key)
                    if hasattr(value, '__call__'):
                        value = value(**kwargs)
                    cells.append(value)
            rows.append(self.row_hook({'id': obj.pk, 'values': cells}, obj))
        return rows

    def common(self, request, *args, **kwargs):
        available_columns = self.get_columns()
        stateful_columns = self.get_stateful_columns(available_columns)

        self.validator_form = self.VALIDATOR_FORM(
            request.POST,
            request=request,
            columns=stateful_columns or available_columns,
            resource=self)

    def _compose(self, form):
        queryset = self.get_queryset(form.cleaned_data['headers'])
        page = self.get_page(queryset, form.cleaned_data['limit'], form.cleaned_data['offset'])
        rows = self.get_rows(page, form.cleaned_data['headers'])
        return page, rows

    def post(self, request, *args, **kwargs):
        form = self.validator_form
        if form.is_valid():
            try:
                page, rows = self._compose(form)
            except EmptyPage:
                form.reset_offset()
                page, rows = self._compose(form)

            if self._meta.stateful and not isinstance(request.user, AnonymousUser):
                form.save()

            return ApiResponse({'columns': form.cleaned_data['headers'],
                                'rows': rows,
                                'pages': page})
        else:
            return ApiResponse(form, status_code=status.HTTP_400_BAD_REQUEST)
