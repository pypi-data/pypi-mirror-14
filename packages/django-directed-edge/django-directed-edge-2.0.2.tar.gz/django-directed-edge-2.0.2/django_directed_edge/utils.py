import collections

from directed_edge import Database

from django.db import models
from django.db.models.base import ModelBase

from . import app_settings

def get_database():
    return Database(app_settings.USERNAME, app_settings.PASSWORD)

def ident(obj, pk=None):
    """
    Converts a Django model or model instance into a text representation for
    storing in Directed Edge.

    >>> ident(User)
    auth.User

    >>> ident(User, 2)
    auth.User#2

    >>> ident(User.objects.get(pk=2))
    auth.User#2
    """

    if isinstance(obj, basestring):
        return obj

    ret = '%s.%s' % (obj._meta.app_label, obj._meta.object_name)

    if not isinstance(obj, ModelBase):
        if pk is not None:
            raise ValueError("Cannot specify a primary key with an instance")

        # Object is an instance
        ret += '#%d' % obj.pk

    if pk is not None:
        ret += '#%d' % pk

    return ret

def rident(items):
    """
    Converts a list of ident()-like values into Django model instances.

    Will perform n queries, where 'n' is the number of distinct models referred
    to by the items.
    """

    model_pks = collections.defaultdict(set)
    for item in items:
        appmodel, pk = item.split('#', 1)
        model_pks[appmodel].add(pk)

    instances = {}
    for appmodel, pks in model_pks.iteritems():
        app, model_name = appmodel.split('.', 1)

        model = models.get_model(app, model_name)
        if model is None:
            continue

        instances[appmodel] = model.objects.in_bulk(pks)

    result = []
    for item in items:
        appmodel, pk = item.split('#', 1)

        try:
            result.append(instances[appmodel][int(pk)])
        except KeyError:
            pass

    return result

def to_pks(items):
    return [int(x.split('#', 1)[1]) for x in items]
