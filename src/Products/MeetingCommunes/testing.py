# -*- coding: utf-8 -*-
from plone.testing import z2, zca
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting
import Products.MeetingCommunes


MC_ZCML = zca.ZCMLSandbox(filename="testing.zcml",
                             package=Products.MeetingCommunes,
                             name='MC_ZCML')

MC_Z2 = z2.IntegrationTesting(bases=(z2.STARTUP, MC_ZCML),
                                 name='MC_Z2')

MC = PloneWithPackageLayer(
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingCommunes,
    additional_z2_products=('Products.MeetingCommunes','Products.PloneMeeting','Products.CMFPlacefulWorkflow'),
    gs_profile_id='Products.MeetingCommunes:default',
    name="MC")

MC_TESTS_PROFILE = PloneWithPackageLayer(
    bases=(MC, ),
    zcml_filename="testing.zcml",
    zcml_package=Products.MeetingCommunes,
    additional_z2_products=('Products.MeetingCommunes',),
    gs_profile_id='Products.MeetingCommunes:tests',
    name="MC_TESTS_PROFILE")

MC_INTEGRATION = IntegrationTesting(
    bases=(MC,), name="MC_INTEGRATION")

MC_TESTS_PROFILE_INTEGRATION = IntegrationTesting(
    bases=(MC_TESTS_PROFILE,), name="MC_TESTS_PROFILE_INTEGRATION")

MC_TESTS_PROFILE_FUNCTIONAL = FunctionalTesting(
    bases=(MC_TESTS_PROFILE,), name="MC_TESTS_PROFILE_FUNCTIONAL")

