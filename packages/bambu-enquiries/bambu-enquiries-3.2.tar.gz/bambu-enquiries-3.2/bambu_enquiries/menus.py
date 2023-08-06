from bambu_navigation import MenuBuilder, site

class EnquiriesMenuBuilder(MenuBuilder):
    def register_partials(self):
        return (
            {
                'name': 'enquiries',
                'description': 'Adds a link to the Enquiries page'
            },
        )
    
    def add_to_menu(self, name, items, **kwargs):
        items.append(
            {
                'url': ('enquiry',),
                'title': u'Contact us',
                'selection': 'enquiry',
                'order': 99
            }
        )

site.register(EnquiriesMenuBuilder)