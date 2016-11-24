*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Resource  Products/PloneMeeting/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging
Library  Selenium2Library
Library  Selenium2Screenshots

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Test Cases ***

Caractéristiques de l'application
    # first log to console line is buggy so here is a workaround line.
    Log To Console  *
    ConnectAs  admin  secret

# partie 2.3 Interface générale
    Log To Console  2.3 Interface générale
    ConnectAs  dgen  Meeting_12
    Sleep  0.5
    Select collection  portal_plonemeeting/meeting-config-college/searches/searches_items/searchallitems
    Wait until element is visible  css=.th_header_pretty_link  20
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-3_interface_generale.png  css=.site-plone  id=portal-footer

# partie 2.4.1 Création d'un point
    Log To Console  2.4.1 Création d'un point
    Click and Screenshot overlayForm  css=#newTemplateItemCreation  doc/caracteristique-de-l-application/2-4_1_creation_d_un_point.png  css=.overlay.overlay-ajax
    Click element  css=.fancytree-title
    Wait until element is visible  css=#cke_observations  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_1_creation_d_un_point-2.png  css=.site-plone  id=portal-footer
    Click element  name=form.button.save

# partie 2.4.2 Visualisation d'un point
    Log To Console  2.4.2 Visualisation d'un point
    Wait until element is visible  css=dl.portalMessage:nth-child(3)  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_2_interface_generale.png  css=.site-plone  id=portal-footer
    Go to  ${PLONE_URL}/Members/dgen/mymeetings/meeting-config-college/recurringofficialreport1
    Click and Screenshot overlayForm  css=.link-overlay  doc/caracteristique-de-l-application/2-4_2_interface_generale-historique.png  css=.overlay.overlay-ajax

# partie 2.4.3. Ajout d'annexes
    Log To Console  2.4.3. Ajout d'annexes
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Click element  css=#contentview-annexes_form
    Wait until element is visible  css=#annex_file  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_3_voir_les_anexes.png  css=.site-plone  id=portal-footer

# partie 2.4.4. Gestion des avis
    Log To Console  2.4.4. Gestion des avis
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Wait until element is visible  css=.warn_delay_advice
    Scroll Page  0  1000
    Add pointer  css=.warn_delay_advice  size=200
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_4_voir_les_demandes_d_avis.png  css=.site-plone  id=portal-footer
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Sleep  1.0
    Click and Screenshot overlayForm  css=.advices_of_type  doc/caracteristique-de-l-application/2-4_4_voir_les_demandes_d_avis2.png  css=.actionMenuContentAX.actionMenuContentAdvice
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Sleep  1.0
    Click and Screenshot overlayForm  css=.link-overlay-pm-advice.link-overlay  doc/caracteristique-de-l-application/2-4_4_ajout_d_avis.png  css=.overlay.overlay-ajax
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Sleep  1.0
    Click and Screenshot overlayForm  css=dl.actionMenuAX:nth-child(2) > dt:nth-child(1)  doc/caracteristique-de-l-application/2-4_4_avis_donne.png  css=dl.actionMenuAX:nth-child(2) > dd:nth-child(2)

# partie 2.4.5. Gestion des avis : ajout d'annexes
    Log To Console  2.4.5. Gestion des avis : ajout d'annexes
    Go to  ${PLONE_URL}/Members/agentCompta/mymeetings/meeting-config-college/template5
    Click element  css=dl.actionMenuAX:nth-child(2) > dt:nth-child(1)
    Sleep  0.5
    Add pointer  css=dl.actionMenuAX:nth-child(2) > dd:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > fieldset:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5)  size=50
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_5_avis_ajout_annexe.png  css=dl.actionMenuAX:nth-child(2) > dd:nth-child(2)
    Go to  ${PLONE_URL}/Members/agentCompta/mymeetings/meeting-config-college/template5
    Click element  css=dl.actionMenuAX:nth-child(2) > dt:nth-child(1)
    Click element  css=dl.actionMenuAX:nth-child(2) > dd:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > fieldset:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5)
    Wait until element is visible  id=annex_file  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_5_avis_ajout_annexe2.png  css=.site-plone  id=portal-footer

# partie 2.4.6. Gestion des avis : avis avec délai
    Log To Console  2.4.6. Gestion des avis : avis avec délai
    Go to  ${PLONE_URL}/Members/agentCompta/mymeetings/meeting-config-college/template5
    Wait until element is visible  id=contentview-edit  10
    Click element  id=contentview-edit
    Wait until element is visible  id=optionalAdvisers  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_6_avis_avec_delais.png  id=optionalAdvisers
    Sleep  0.5
    Click element  name=form.button.cancel
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Click and Screenshot overlayForm  css=.advices_of_type  doc/caracteristique-de-l-application/2-4_6_voir_les_demandes_d_avis.png  css=.actionMenuContentAX.actionMenuContentAdvice
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3

# partie 2.4.7. Tableau récapitulatif affichant des points
    Log To Console  2.4.7. Tableau récapitulatif affichant des points
    Select collection  portal_plonemeeting/meeting-config-college/searches/searches_items/searchmyitems
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_7_tableau_recapitulatif_de_mes_points.png  id=content

# partie 2.4.8. Evolution du point dans l'application
    Log To Console  2.4.8. Evolution du point dans l'application
    Click element  css=.state-created
    Wait Until Page Loaded
    Sleep  3
    Click element  css=.apButtonWF_freeze
    wait until element is visible  css=.apButtonWF_decide
    Wait Until Page Loaded
    Click element  css=.apButtonWF_decide
    Wait Until Page Loaded
    Click element  xpath=//*[@id="faceted-results"]/div/div[5]/table/tbody/tr[3]/td[3]/a

    wait until element is visible  css=.apButtonWF_delay
    Wait Until Page Loaded
    Click and Screenshot overlayForm  css=.apButtonWF_delay  doc/caracteristique-de-l-application/2-4_8_confirmation_transition.png  css=.pb-ajax

# partie 2.4.9. Interventions de plusieurs utilisateurs sur le même point
    Log To Console  2.4.9. Interventions de plusieurs utilisateurs sur le même point
    # Need update Demo profile (enable taken over by)

# partie 2.5.1. Création d'une séance
2.5.1. Création d'une séance
    ConnectAs  dgen  Meeting_12
    Wait Until Page Loaded
    Click link  id=newMeetingCreation
    wait until element is visible  id=portal-column-content  5
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-5_1_creation_seance.png  id=portal-column-content

# partie 2.5.2. Visualisation d'une séance par un gestionnaire de séance
2.5.2. Visualisation d'une séance par un gestionnaire de séance
    ConnectAs  dgen  Meeting_12
    Wait Until Page Loaded
    click element  css=.state-created
    Wait Until Page Loaded
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-5_2_visualisation_seance_gestionnaire.png  id=portal-column-content

# partie 2.5.3. Visualisation d'une séance par un créateur de point
2.5.3. Visualisation d'une séance par un créateur de point
    ConnectAs  agentPers  Meeting_12
    Wait Until Page Loaded
    click element  css=.state-created
    Wait Until Page Loaded
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-5_3_visualisation_seance_createur.png  id=portal-column-content

# partie 2.5.4. Modification des points d'une séance
2.5.4. Modification des points d'une séance
    ConnectAs  dgen  Meeting_12
    Wait Until Page Loaded
    click element  css=.state-created
    Wait Until Page Loaded
    Go To  ${PLONE_URL}/Members/dgen/mymeetings/meeting-config-college/copy4_of_recurringofficialreport1
    Wait Until Page Loaded
    wait until element is visible  css=.navigateItem
    Add pointer  css=.navigateItem  size=400
    Capture page screenshot  doc/caracteristique-de-l-application/2-5_4_navigation_widget.png
    reload page
    Wait Until Page Loaded
    wait until element is visible  css=#hook_description > fieldset:nth-child(2) > legend:nth-child(1) > img:nth-child(1)  2
    click element  css=#hook_description > fieldset:nth-child(2) > legend:nth-child(1) > img:nth-child(1)
    wait until element is visible  css=.cke_toolgroup  5
    Capture page screenshot  doc/caracteristique-de-l-application/2-5_4_edition_champ.png

# partie 2.5.5. Ajout d'un point "en urgence"

# partie 2.5.6. Gestion des assemblée et signatures par points en mode "zones de texte libre"
#    Debug

*** Keywords ***
Suite Setup
    Open test browser
    Set Window Size  1280  6000