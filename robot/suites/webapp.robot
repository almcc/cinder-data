*** Settings ***
Documentation  This is some basic tests to make sure the django webapp is work as expected.
Library         OperatingSystem
Library         RequestsLibrary

*** Variables ***
${WEBAPP}         http://server:8000

*** Test Cases ***
Can load root page of server
  [Documentation]  Make sure we can load the root of the api server
  [Tags]  smoke
  Create Session	webapp  ${WEBAPP}
  ${resp}=  Get Request  webapp  /api/v1
  Should Be Equal As Strings	${resp.status_code}  200

*** Keywords ***
