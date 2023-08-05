import contextlib

from directed_edge import Exporter, Item

from .utils import ident, get_database

@contextlib.contextmanager
def get_exporter(target=None):
    if target is None:
        target = get_database()

    exporter = DjangoExporter(target)

    yield exporter

    exporter.finish()

class DjangoExporter(Exporter):
    def export(self, item):
        super(DjangoExporter, self).export(self.to_item(item))

    def to_item(self, instance):
        if isinstance(instance, (basestring, Item)):
            return instance

        item = DjangoItem(self._Exporter__database, ident(instance))
        item.add_tag(ident(type(instance)))

        return item

class DjangoItem(Item):
    def link_to(self, other, *args, **kwargs):
        super(DjangoItem, self).link_to(ident(other), *args, **kwargs)
