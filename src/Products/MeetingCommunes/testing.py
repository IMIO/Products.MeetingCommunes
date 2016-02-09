# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from Products.PloneMeeting.testing import PM_PLONE_FIXTURE
import Products.MeetingCommunes
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE

MC_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                          package=Products.MeetingCommunes,
                          name='MC_ZCML')

MC_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MC_ZCML),
                              name='MC_Z2')

MC_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingCommunes,
    additional_z2_products=('imio.dashboard',
                            'Products.MeetingCommunes',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow',
                            'Products.PasswordStrength'),
    gs_profile_id='Products.MeetingCommunes:testing',
    name="MC_TESTING_PROFILE")

MC_TESTING_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MC_TESTING_PROFILE,), name="MC_TESTING_PROFILE_FUNCTIONAL")

MC_EXAMPLES_FR_TESTING_PROFILE = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingCommunes,
    additional_z2_products=('Products.MeetingCommunes',
                            'Products.PloneMeeting',
                            'Products.CMFPlacefulWorkflow'),
    gs_profile_id='Products.MeetingCommunes:examples_fr',
    name="MC_TESTING_PROFILE")

MC_TESTING_ROBOT = FunctionalTesting(
    bases=(
        MC_EXAMPLES_FR_TESTING_PROFILE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="MC_TESTING_ROBOT",
)

# simple layer used for testSetup
MC_PLONE_FIXTURE = PloneWithPackageLayer(
    zcml_filename=PM_PLONE_FIXTURE.zcml_filename,
    zcml_package=Products.MeetingCommunes,
    additional_z2_products=PM_PLONE_FIXTURE.additional_z2_products,
    gs_profile_id=PM_PLONE_FIXTURE.gs_profile_id,
    name="MC_PLONE_FIXTURE")

MC_PLONE_INTEGRATION = IntegrationTesting(
    bases=(MC_PLONE_FIXTURE,),
    name="MC_PLONE_INTEGRATION"
)
