*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Resource  Products/PloneMeeting/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging
Library  Selenium2Screenshots

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Test cases ***

Caractéristiques de l'application
# partie 2.3 Interface générale
    Log in  dgen  Meeting_12
    Sleep  0.5
    Select collection  portal_plonemeeting/meeting-config-college/searches/searches_items/searchallitems
    Wait until element is visible  css=.th_header_pretty_link  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-3_interface_generale.png  css=.site-plone  id=portal-footer-wrapper

# partie 2.4.1 Création d'un point
    Click and Screenshot overlayForm  css=#newTemplateItemCreation  doc/caracteristique-de-l-application/2-4_1_creation_d_un_point.png  css=.overlay.overlay-ajax
    Click element  css=.fancytree-title
    Wait until element is visible  css=#cke_observations  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_1_creation_d_un_point-2.png  css=.site-plone  id=portal-footer-wrapper
    Click element  name=form.button.save

# partie 2.4.2 Visualisation d'un point
    Wait until element is visible  css=dl.portalMessage:nth-child(3)  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_2_interface_generale.png  css=.site-plone  id=portal-footer-wrapper
    Go to  ${PLONE_URL}/Members/dgen/mymeetings/meeting-config-college/recurringofficialreport1
    Click and Screenshot overlayForm  css=#content-history  doc/caracteristique-de-l-application/2-4_2_interface_generale-historique.png  css=.overlay.overlay-ajax

# partie 2.4.3. Ajout d'annexes
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Click element  css=#contentview-annexes_form
    Wait until element is visible  css=#annex_file  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_3_voir_les_anexes.png  css=.site-plone  id=portal-footer-wrapper

# partie 2.4.4. Gestion des avis
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Add pointer  css=.warn_delay_advice  size=200
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_4_voir_les_demandes_d_avis.png  css=.site-plone  id=portal-footer-wrapper
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Click and Screenshot overlayForm  css=.advices_of_type  doc/caracteristique-de-l-application/2-4_4_voir_les_demandes_d_avis2.png  css=.actionMenuContentAX.actionMenuContentAdvice
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Click and Screenshot overlayForm  css=.link-overlay-pm-advice.link-overlay  doc/caracteristique-de-l-application/2-4_4_ajout_d_avis.png  css=.overlay.overlay-ajax
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Click and Screenshot overlayForm  css=dl.actionMenuAX:nth-child(2) > dt:nth-child(1)  doc/caracteristique-de-l-application/2-4_4_avis_donne.png  css=dl.actionMenuAX:nth-child(2) > dd:nth-child(2)

# partie 2.4.5. Gestion des avis : ajout d'annexes
    Go to  ${PLONE_URL}/Members/agentCompta/mymeetings/meeting-config-college/template5
    Click element  css=dl.actionMenuAX:nth-child(2) > dt:nth-child(1)
    Sleep  0.5
    Add pointer  css=dl.actionMenuAX:nth-child(2) > dd:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > fieldset:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5)  size=50
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_5_avis_ajout_annexe.png  css=dl.actionMenuAX:nth-child(2) > dd:nth-child(2)
    Go to  ${PLONE_URL}/Members/agentCompta/mymeetings/meeting-config-college/template5
    Click element  css=dl.actionMenuAX:nth-child(2) > dt:nth-child(1)
    Click element  css=dl.actionMenuAX:nth-child(2) > dd:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > fieldset:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5)
    Wait until element is visible  id=annex_file  10
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_5_avis_ajout_annexe2.png  css=.site-plone  id=portal-footer-wrapper

# partie 2.4.6. Gestion des avis : avis avec délai
    Go to  ${PLONE_URL}/Members/agentCompta/mymeetings/meeting-config-college/template5
    Click element  id=contentview-edit
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_6_avis_avec_delais.png  id=optionalAdvisers
    Click element  name=form.button.cancel
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Click and Screenshot overlayForm  css=.advices_of_type  doc/caracteristique-de-l-application/2-4_6_voir_les_demandes_d_avis.png  css=.actionMenuContentAX.actionMenuContentAdvice
    Go to  ${PLONE_URL}/Members/agentPers/mymeetings/meeting-config-college/template3
    Mouse Over  css=.warn_delay_advice > img:nth-child(1)
    #L'info bulle n'est pas capturée dans le screenshot.
    #Sleep  1
    #Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_6_avis_help_icone.png  css=.itemAdvicesCell

# partie 2.4.7. Tableau récapitulatif affichant des points
    Select collection  portal_plonemeeting/meeting-config-college/searches/searches_items/searchmyitems
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-4_7_tableau_recapitulatif_de_mes_points.png  id=content
    Debug


*** Keywords ***
Suite Setup
    Open test browser
    Set Window Size  1280  800
