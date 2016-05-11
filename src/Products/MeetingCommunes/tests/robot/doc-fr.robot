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
    Debug
    Capture and crop page screenshot  doc/caracteristique-de-l-application/2-3_interface_generale.png  css=.site-plone  id=portal-footer-wrapper 

*** Keywords ***
Suite Setup
    Open test browser
    Set Window Size  1280  800

