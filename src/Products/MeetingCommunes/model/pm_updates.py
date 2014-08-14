from Products.Archetypes.atapi import BooleanField
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import TextField
from Products.Archetypes.atapi import MultiSelectionWidget
from Products.Archetypes.atapi import TextAreaWidget
from Products.Archetypes.atapi import Schema
from Products.PloneMeeting.MeetingGroup import MeetingGroup
from Products.PloneMeeting.MeetingConfig import MeetingConfig


def update_group_schema(baseSchema):
    specificSchema = Schema((

        # field used to define list of services for echevin for a MeetingGroup
        LinesField(
            name='echevinServices',
            widget=MultiSelectionWidget(
                size=10,
                label='EchevinServices',
                label_msgid='MeetingCommunes_label_echevinServices',
                description='Leave empty if he is not an echevin',
                description_msgid='MeetingCommunes_descr_echevinServices',
                i18n_domain='PloneMeeting',
            ),
            enforceVocabulary=True,
            multiValued=1,
            vocabulary='listEchevinServices',
        ),
        # field used to define specific signatures for a MeetingGroup
        TextField(
            name='signatures',
            allowable_content_types=('text/plain',),
            widget=TextAreaWidget(
                label='Signatures',
                label_msgid='MeetingCommunes_label_signatures',
                description='Leave empty to use the signatures defined on the meeting',
                description_msgid='MeetingCommunes_descr_signatures',
                i18n_domain='PloneMeeting',
            ),
            default_content_type='text/plain',
        ),
    ),)

    completeSchema = baseSchema + specificSchema.copy()
    return completeSchema
MeetingGroup.schema = update_group_schema(MeetingGroup.schema)


def update_config_schema(baseSchema):
    specificSchema = Schema((
        TextField(
            name='itemDecisionReportText',
            widget=TextAreaWidget(
                description="ItemDecisionReportText",
                description_msgid="item_decision_report_text_descr",
                label='ItemDecisionReportText',
                label_msgid='MeetingCommunes_label_itemDecisionReportText',
                i18n_domain='PloneMeeting',
            ),
            allowable_content_types=('text/plain', 'text/html', ),
            default_output_type="text/plain",
        ),
        BooleanField(
            name='initItemDecisionIfEmptyOnDecide',
            default=True,
            widget=BooleanField._properties['widget'](
                description="InitItemDecisionIfEmptyOnDecide",
                description_msgid="init_item_decision_if_empty_on_decide",
                label='Inititemdecisionifemptyondecide',
                label_msgid='MeetingCommunes_label_initItemDecisionIfEmptyOnDecide',
                i18n_domain='PloneMeeting'),
        ),
    ),)
    completeConfigSchema = baseSchema + specificSchema.copy()
    completeConfigSchema.moveField('itemDecisionReportText', after='budgetDefault')
    return completeConfigSchema
MeetingConfig.schema = update_config_schema(MeetingConfig.schema)


# Classes have already been registered, but we register them again here
# because we have potentially applied some schema adaptations (see above).
# Class registering includes generation of accessors and mutators, for
# example, so this is why we need to do it again now.
from Products.PloneMeeting.config import registerClasses
registerClasses()
