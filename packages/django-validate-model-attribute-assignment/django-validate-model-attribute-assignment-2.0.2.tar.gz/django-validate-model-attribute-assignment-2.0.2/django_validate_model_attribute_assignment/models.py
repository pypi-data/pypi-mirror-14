import sys

from django.db import models
from django.conf import settings

FIELDS = {}
EXCEPTIONS = {
    'auth.User': ('backend',),
}

def setattr_validate(self, name, value):
    super(models.Model, self).__setattr__(name, value)

    # Real field names cannot start with underscores
    if name.startswith('_'):
        return

    # Magic
    if name == 'pk':
        return

    k = '%s.%s' % (self._meta.app_label, self._meta.object_name)
    try:
        fields = FIELDS[k]
    except KeyError:
        fields = FIELDS[k] = set(
            getattr(x, y) for x in self._meta.fields
            for y in ('attname', 'name')
        )

    # Field is in allowed list
    if name in fields:
        return

    # Field is in known exceptions
    if name in EXCEPTIONS.get(k, ()):
        return

    # Always allow Django internals to set values (eg. aggregates)
    if 'django/db/models' in sys._getframe().f_back.f_code.co_filename:
        return

    raise ValueError(
        "Refusing to set unknown attribute '%s' on %s instance. "
        "(Did you misspell %s?)" % (name, k, ', '.join(fields))
    )

# Let's assume we have good test coverage
if settings.DEBUG:
    models.Model.__setattr__ = setattr_validate
