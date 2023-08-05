from directed_edge import Item

from . import app_settings
from .utils import ident, rident, get_database, to_pks

def related(obj, tags=(), max_results=20):
    if not app_settings.ENABLED:
        return []

    item = Item(get_database(), ident(obj))
    items = item.related(map(ident, tags), maxResults=max_results)

    return rident(items)

def recommended(obj, tags=(), max_results=20, pks=False):
    if not app_settings.ENABLED:
        return []

    item = Item(get_database(), ident(obj))
    items = item.recommended(map(ident, tags), maxResults=max_results)

    if pks:
        return to_pks(items)

    return rident(items)
