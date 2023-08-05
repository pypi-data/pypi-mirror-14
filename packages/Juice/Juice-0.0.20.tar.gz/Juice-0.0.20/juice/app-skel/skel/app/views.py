"""
Juice
"""

from juice import (View, flash, abort, request, url_for, redirect)
from juice.decorators import (route, menu, template, plugin, methods)
from juice.plugins import (contact_page, )

# ------------------------------------------------------------------------------

@plugin(contact_page.contact_page, menu={"name": "Contact Us", "order": 3})
class Index(View):

    @menu("Home", order=1)
    def index(self):
        self.meta_tags(title="Hello View!")
        return {}





