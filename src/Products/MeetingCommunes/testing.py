from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import Products.MeetingCommunes


PRODUCTS_MEETINGCOMMUNES = PloneWithPackageLayer(
    zcml_package=Products.MeetingCommunes,
    zcml_filename='testing.zcml',
    gs_profile_id='Products.MeetingCommunes:testing',
    name="PRODUCTS_MEETINGCOMMUNES")

PRODUCTS_MEETINGCOMMUNES_INTEGRATION = IntegrationTesting(
    bases=(PRODUCTS_MEETINGCOMMUNES, ),
    name="PRODUCTS_MEETINGCOMMUNES_INTEGRATION")

PRODUCTS_MEETINGCOMMUNES_FUNCTIONAL = FunctionalTesting(
    bases=(PRODUCTS_MEETINGCOMMUNES, ),
    name="PRODUCTS_MEETINGCOMMUNES_FUNCTIONAL")
