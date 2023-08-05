"""
    drfchangemgmt.mixins
    ~~~~~~~~~~~~~~~~~~~~

    DRF related mixins to add change management functionality
"""

import six

from django.conf import settings
from rest_framework.relations import PrimaryKeyRelatedField


__all__ = ('ChangeMgmtSerializerMixin', 'PK_FAST_COMPARE')


try:
    PK_FAST_COMPARE = settings.DRF_CHANGEMGMT['PK_FAST_COMPARE']
except (AttributeError, KeyError):
    PK_FAST_COMPARE = True


def _get_changed_fields(model_instance):
    """ Return the changed fields data structure
    This will be bound to a model instance & should only ever
    be called from a model instance
    """

    return model_instance._changed_fields


def _get_new_pk(instance):
    """ Given a model instance return it's primary key value """

    return instance.pk


def _get_old_pk(instance, field_name):
    """ Given a model instance & field_name find the true name of the field
    This is needed to support the uncommon scenario where the
    instance's ForeignKey column name may have been overridden
    from the django default behavior of <field_name>_id.
    Using `get_attname` will return whatever the real fields name
    is that has just the foreign key value.
    """

    model_field_name = instance._meta.get_field(field_name).get_attname()
    return getattr(instance, model_field_name)


class ChangeMgmtSerializerMixin(object):
    """ DRF Serializer mixin for added change management functionality
    The DRF serializer will add a new private property named
    `_changed_fields` & a public method named `get_changed_fields`
    to the instance provided.
    The `_changed_fields` property contains an empty dict if no
    changes were made & if changes are present then each key is
    named after the field & the value is:
        {
            old: <old value>
            new: <new value>
        }
    By default PrimaryKeyRelatedFields are optimized to compare
    only the ID's & the old/new values will be limited to the
    keys as well.
    The DRF__CHANGEMGMT[PK_FAST_COMPARE] django settings can be
    set to False so full Model compares are performed causing
    a database query for the old value globally.
    INFO: Change tracking only occurs on the initial input of
          data from the requesting client against EXISTING models.
          New models are completely skipped & mutations after the
          fact by custom business logic are not tracked.
          This is by design.
    """

    def to_internal_value(self, data):
        """ Override the DRF native to_internal_value method
        Use the output from the native `to_internal_value` to
        automatically prune the list of fields to compare. It
        will only return fields that are both "writable" & provided
        by the requesting user.
        Additionally, it already takes care of the uncommon scenario
        of a field using the `source` argument where the backend
        object actually uses a different field than the API. That
        rename is already taken care of so we don't need to sweat it.
        INFO: Some helper methods are used but intentionally left
              off the mixin to avoid cluttering the parent serializer.
        """

        ret = super(ChangeMgmtSerializerMixin, self).to_internal_value(data)
        # new model so skip
        if not self.instance:
            return ret

        # existing so carry on
        fields = self.get_fields()

        # initialize the instance
        self.instance._changed_fields = {}
        self.instance.get_changed_fields = six.create_bound_method(
            _get_changed_fields,
            self.instance
        )

        for key, val in ret.items():
            field = fields[key].__class__

            if isinstance(PrimaryKeyRelatedField, field) and PK_FAST_COMPARE:
                old_val = _get_old_pk(self.instance, key)
                if val:
                    new_val = _get_new_pk(val)
            else:
                old_val = getattr(self.instance, key)
                new_val = val

            if new_val != old_val:
                self.instance._changed_fields[key] = {
                    'old': old_val,
                    'new': new_val,
                }

        # since we're overriding
        return ret
