import django
from django.core import checks
from django.utils.functional import cached_property

if django.VERSION < (1, 8):
    from django.db.models.loading import get_model
else:
    from django.apps import apps
    get_model = apps.get_model


UNDEFINED = object()


class NonPrimaryForeignKey(object):
    """
    Descriptor class for handling non-primary foreign keys.

    The implementation is loosely based on ``GenericForeignKey`` from the
    ``django.contrib.contenttypes`` module.
    """

    def __init__(self, to_model, from_field, to_field=None):
        self._to_model = to_model
        self._from_field = from_field
        self._to_field = to_field or from_field  # Default to the fields sharing a name.
        self.editable = False

    @cached_property
    def to_model(self):
        return get_model(self._to_model)

    @cached_property
    def to_field(self):
        return self.to_model._meta.get_field(self._to_field)

    @cached_property
    def from_field(self):
        return self.model._meta.get_field(self._from_field)

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        self.cache_name = "_%s_cache" % name
        setattr(cls, name, self)

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        value = getattr(instance, self.from_field.attname, None)
        if value is None:
            return None
        cached = getattr(instance, self.cache_name, UNDEFINED)

        if cached is not UNDEFINED and getattr(cached, self.to_field.attname, None) == value:
            return cached

        rel_obj = None
        rel_obj = self.to_model._default_manager.get(
            **{self.to_field.attname: value})
        setattr(instance, self.cache_name, rel_obj)
        return rel_obj

    def __set__(self, instance, value):
        if not (value is None or isinstance(value, self.to_model)):
            raise TypeError('%r must is not a %s' % (value, self.to_model))
        set_value = getattr(value, self.to_field.attname, None)
        setattr(instance, self.cache_name, value)
        setattr(instance, self.from_field.attname, set_value)

    def __str__(self):
        model = self.model
        app = model._meta.app_label
        return '%s.%s.%s' % (app, model._meta.object_name, self.name)

    def check(self, **kwargs):
        errors = []
        if self.name.endswith("_"):
            errors.append(
                checks.Error(
                    'Field names must not end with an underscore.',
                    hint=None,
                    obj=self,
                    id='fields.E001',
                )
            )
        return errors

    def is_cached(self, instance):
        # Called in prefetching.
        return hasattr(instance, self.cache_name)

    def get_prefetch_queryset(self, instances, queryset=None):
        """
        Prefetches for the given instances.

        Based on the implementation in ``ReverseSingleRelatedObjectDescriptor``.
        """
        values = [
            getattr(instance, self.from_field.attname, None) for instance in instances
            if getattr(instance, self.from_field.attname, None) is not None]
        if queryset is None:
            queryset = self.to_model._default_manager
        queryset = queryset.filter(**{'%s__in' % self.to_field.attname: values})
        rel_obj_attr = lambda rel_obj: (getattr(rel_obj, self.to_field.attname), )
        instance_attr = lambda obj: (getattr(obj, self.from_field.attname), )
        return queryset, rel_obj_attr, instance_attr, True, self.cache_name
