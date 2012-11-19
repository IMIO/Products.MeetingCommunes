from Products.Archetypes.atapi import *


def update_meeting_schema(baseSchema):
   
    specificSchema = Schema((
    ),)

    baseSchema['assembly'].widget.description_msgid = "assembly_meeting_descr"

    completeSchema = baseSchema + specificSchema.copy()
    return completeSchema


def update_group_schema(baseSchema):
   
    specificSchema = Schema((

        # field used to define list of services for echevin for a MeetingGroup
        LinesField(
            name='echevinServices',
            widget=MultiSelectionWidget(
                size=10,
                label='EchevinServices',
                label_msgid='MeetingCommune_label_echevinServices',
                description='Leave empty if he is not an echevin',
                description_msgid='MeetingCommune_descr_echevinServices',
                i18n_domain='PloneMeeting',
            ),
            enforceVocabulary=True,
            multiValued=1,
            vocabulary='listEchevinServices',
        ),
        
        # field used to define specific signatures for a MeetingGroup
        TextField(
            name='signatures',
            widget=TextAreaWidget(
                label='Signatures',
                label_msgid='MeetingCommune_label_signatures',
                description='Leave empty to use the signatures defined on the meeting',
                description_msgid='MeetingCommune_descr_signatures',
                i18n_domain='PloneMeeting',
            ),
        ),
    ),)

    completeSchema = baseSchema + specificSchema.copy()
    return completeSchema

def update_config_schema(baseSchema):
    specificSchema = Schema((
    
        TextField(
            name='itemDecisionReportText',
            widget=TextAreaWidget(
                description="ItemDecisionReportText",
                description_msgid="item_decision_report_text_descr",
                label='ItemDecisionReportText',
                label_msgid='PloneMeeting_label_itemDecisionReportText',
                i18n_domain='PloneMeeting',
            ),
        allowable_content_types=('text/html',),
        default_output_type="text/html",
        )
    ),)
    
    completeConfigSchema = baseSchema + specificSchema.copy()
    completeConfigSchema.moveField('itemDecisionReportText', after='budgetDefault')    
    return completeConfigSchema
