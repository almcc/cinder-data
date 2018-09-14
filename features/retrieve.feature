Feature: cinder data retieve features

  Scenario: find an item
     Given we have setup a store for http://localhost:8001 api/v1
      When we request Car 1
      Then we have a "Model T"
