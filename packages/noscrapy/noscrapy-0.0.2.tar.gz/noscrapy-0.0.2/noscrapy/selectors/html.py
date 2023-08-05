from .base import ItemsSelector

class HtmlSelector(ItemsSelector):
    def _get_item_data(self, item):
        yield {self.id: item.html()}
