from django.conf.urls import url
from bambu_enquiries.views import enquiry, enquiry_thanks
from django.conf import settings

if 'bambu_bootstrap' in settings.INSTALLED_APPS:
    from bambu_bootstrap.decorators import body_classes
else:
    def body_classes(view, *classes):
        return view

urlpatterns = (
    url(r'^$', body_classes(enquiry, 'enquiries'), name = 'enquiry'),
    url(r'^thanks/$', body_classes(enquiry_thanks, 'enquiries', 'enquiries-thanks'),
        name = 'enquiry_thanks'
    )
)
