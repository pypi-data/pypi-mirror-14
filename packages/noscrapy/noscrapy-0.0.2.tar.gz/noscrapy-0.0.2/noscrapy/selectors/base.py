import re
from collections import OrderedDict
from time import sleep

from noscrapy.utils import etree, Class, Field, PyQuery

class Selector(Class):
    id = Field()
    selector = Field(None)
    exclude = Field(None)
    parent_selectors = Field(lambda self: self.__dict__.setdefault('parents', OrderedDict()))
    item_css_selector = Field('*')
    multiple = Field(True)
    delay = Field(0)
    regex = Field(None)

    can_return_multiple = Field(True, readonly=True)
    can_have_childs = Field(False, readonly=True)
    can_have_local_childs = Field(False, readonly=True)
    can_create_new_jobs = Field(False, readonly=True)
    will_return_items = Field(False, readonly=True)

    @property
    def will_return_multiple(self):
        return self.can_return_multiple and self.multiple

    def __init__(self, selector_id, **features):
        self.id = selector_id
        for attr, value in features.items():
            setattr(self, attr, value)

    def __setattr__(self, attr, value):
        if attr.startswith('__') or attr in self.__fields__:
            return super().__setattr__(attr, value)
        raise AttributeError('field %s not known in %s' % (attr, type(self).__name__))

    def has_parent_selector(self, parent_selector_id):
        return parent_selector_id in self.parent_selectors

    def remove_parent_selector(self, parent_selector_id):
        return self.parent_selectors.pop(parent_selector_id, None)

    def rename_parent_selector(self, parent_selector_id, new_selector_id):
        link = self.parent_selectors.__map.get(parent_selector_id, None)
        if link:
            self.remove_parent_selector(new_selector_id)
            link.key = new_selector_id

    def get_parent_items(self, parent_item):
        if not isinstance(parent_item, PyQuery):
            try:
                parent_item = PyQuery(parent_item)
            except (etree.ParserError, etree.XMLSyntaxError) as e:
                if isinstance(parent_item, str):
                    if not parent_item.strip() or 'Document is empty' == str(e):
                        parent_item = PyQuery(None)
                    else:
                        raise
        query = parent_item(self.selector)
        if self.exclude:
            query = query.not_(self.exclude)
        for item in query.items():
            yield item
            if not self.multiple:
                break

    def get_data(self, parent_item):
        sleep(self.delay)
        yield from self._get_data(parent_item)

    def _get_data(self, parent_item):
        raise NotImplemented

    def get_columns(self):
        return [self.id]


class ItemsSelector(Selector):
    def _get_data(self, parent_item):
        yielded = False
        for item in self.get_parent_items(parent_item):
            for data in self._get_item_data(item):
                if self.regex:
                    matches = re.search(self.regex, data[self.id])
                    data[self.id] = matches.group() if matches else None
                yield data
                yielded = True
                if not self.multiple:
                    break
            if yielded and not self.multiple:
                break
        if not yielded:
            yield from self._get_noitems_data()

    def _get_item_data(self, item):
        raise NotImplementedError

    def _get_noitems_data(self):
        yield {self.id: None}
