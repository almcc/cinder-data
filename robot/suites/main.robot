*** Settings ***
Documentation  This is some basic tests to make sure the django webapp is work as expected.
Library         OperatingSystem
Library         RequestsLibrary
Library         ../libs/CinderDataLibrary.py

*** Variables ***
${WEBAPP}         http://server:8000

*** Test Cases ***
Can load root page of server
  [Documentation]  Make sure we can load the root of the api server.
  [Tags]  smoke
  Create Session	webapp  ${WEBAPP}
  ${resp}=  Get Request  webapp  /api/v1
  Should Be Equal As Strings	${resp.status_code}  200

Can get car model
  [Documentation]  Making sure that you can grab the car with id=1 and it is a Ka.
  ${car}=  get model  Car  1
  Should Be Equal As Strings	${car.name}  Ka

Can get first page of car models
  [Documentation]  Making sure that you can the first page of car models.
  ${cars}=  get models  Car
  Length Should Be  ${cars}  10

Can get seconds page of car models
  [Documentation]  Making sure that you can the second page of car models.
  ${cars}=  get models  Car  2
  Length Should Be  ${cars}  9

Making sure there are no cached models
  [Documentation]  Making sure there are no cached models when starting.
  ${cars}=  peek models  Car
  Length Should Be  ${cars}  0

Can get all cachced models
  [Documentation]  Making sure there are cached model after some gets.
  get model  Car  1
  get models  Car
  get models  Car  2
  ${cars}=  peek models  Car
  Length Should Be  ${cars}  19
