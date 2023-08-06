# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.calltoaction -t test_example.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.calltoaction.testing.COLLECTIVE_CALLTOACTION_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/calltoaction/tests/robot/test_example.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a visitor I do not want to see the overlay initially
  Given I am on the home page
   Then I do not see the overlay

Scenario: As a visitor I want to see the overlay after a while
  Given I am on the home page
   When I wait a short time
   Then I do see the overlay

Scenario: As a visitor I do not want to see the overlay a second time
  Given I am on the home page
   When I wait a short time
   And I do see the overlay
   And I reload the page
   And I wait a short time
   Then I do not see the overlay


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

I am on the home page
  Go To  ${PLONE_URL}
  Wait until page contains  Home

a login form
  Go To  ${PLONE_URL}/login_form
  Wait until page contains  Login Name
  Wait until page contains  Password


# --- WHEN -------------------------------------------------------------------

I enter valid credentials
  Input Text  __ac_name  admin
  Input Text  __ac_password  secret
  Click Button  Log in

I wait a short time
  Sleep  1.5

I reload the page
  Reload Page


# --- THEN -------------------------------------------------------------------

I am logged in
  Wait until page contains  You are now logged in
  Page should contain  You are now logged in

I do not see the overlay
  Element Should Not Be Visible  css=.portletCallToAction

I do see the overlay
  Element Should Be Visible  css=.portletCallToAction
  Page should contain  My overlay header
  Page should contain  My overlay text
