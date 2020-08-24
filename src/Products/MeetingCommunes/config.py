# -*- coding: utf-8 -*-
#
# File: config.py
#
# Copyright (c) 2016 by Imio.be
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

from Products.CMFCore.permissions import setDefaultRoles
from Products.PloneMeeting import config


__author__ = """Gauthier Bastien <g.bastien@imio.be>, Stephan Geulette <s.geulette@imio.be>"""
__docformat__ = 'plaintext'

PROJECTNAME = "MeetingCommunes"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))

product_globals = globals()

# extra suffixes while using 'meetingadvicefinances_workflow'
FINANCE_GROUP_SUFFIXES = ('financialprecontrollers',
                          'financialcontrollers',
                          'financialeditors',
                          'financialreviewers',
                          'financialmanagers')

# the id of the collection querying finance advices
FINANCE_ADVICES_COLLECTION_ID = 'searchitemswithfinanceadvice'

# if True, a positive finances advice may be signed by a finances reviewer
# if not, only the finances manager may sign advices
POSITIVE_FINANCE_ADVICE_SIGNABLE_BY_REVIEWER = False

# text about FD advice used in templates
FINANCE_ADVICE_LEGAL_TEXT_PRE = "<p>Attendu la demande d'avis adressée sur " \
    "base d'un dossier complet au Directeur financier en date du {0};<br/></p>"

FINANCE_ADVICE_LEGAL_TEXT = "<p>Attendu l'avis {0} du Directeur financier " \
    "rendu en date du {1} conformément à l'article L1124-40 du Code de la " \
    "démocratie locale et de la décentralisation;</p>"

FINANCE_ADVICE_LEGAL_TEXT_NOT_GIVEN = "<p>Attendu l'absence d'avis du " \
    "Directeur financier rendu dans le délai prescrit à l'article L1124-40 " \
    "du Code de la démocratie locale et de la décentralisation;</p>"

SAMPLE_TEXT = u"<p><strong>Lorem ipsum dolor sit amet</strong>, consectetur adipiscing elit. " \
    u"Aliquam efficitur sapien quam, vitae auctor augue iaculis eget. <BR />Nulla blandit enim lectus. " \
    u"Ut in nunc ligula. Nunc nec magna et mi dictum molestie eu vitae est.<BR />Vestibulum justo erat, " \
    u"congue vel metus sed, condimentum vestibulum tortor. Sed nisi enim, posuere at cursus at, tincidunt " \
    u"eu est. Proin rhoncus ultricies justo. Nunc finibus quam non dolor imperdiet, non aliquet mi tincidunt. " \
    u"Aliquam at mauris suscipit, maximus purus at, dictum lectus.</p>" \
    u"<p>Nunc faucibus sem eu congue varius. Vestibulum consectetur porttitor nisi. Phasellus ante nunc, " \
    u"elementum et bibendum sit amet, tincidunt vitae est. Morbi in odio sagittis, convallis turpis a, " \
    u"tristique quam. Vestibulum ut urna arcu. Etiam non odio ut felis porttitor elementum. Donec venenatis " \
    u"porta purus et scelerisque. Nullam dapibus nec erat at pellentesque. Aliquam placerat nunc molestie " \
    u"venenatis malesuada. Nam ac pretium justo, id imperdiet lacus.</p>"
