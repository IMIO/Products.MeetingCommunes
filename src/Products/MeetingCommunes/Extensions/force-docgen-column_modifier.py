import transaction
from plone import api


def force_column_modifier(modifier='disabled'):
    print("entering force_column_modifier : modifier=" + modifier)
    print("value was " + api.portal.get_registry_record('collective.documentgenerator.browser.controlpanel.'
                                   'IDocumentGeneratorControlPanelSchema.column_modifier'))

    api.portal.set_registry_record('collective.documentgenerator.browser.controlpanel.'
                                   'IDocumentGeneratorControlPanelSchema.column_modifier',
                                   modifier)
    print("value is " + api.portal.get_registry_record('collective.documentgenerator.browser.controlpanel.'
                                   'IDocumentGeneratorControlPanelSchema.column_modifier'))
    transaction.commit()


force_column_modifier()
