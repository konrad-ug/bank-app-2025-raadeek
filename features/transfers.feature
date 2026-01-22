Feature: Account transfers
  
  Scenario: User is able to perform incoming transfer
    Given Account registry is empty
    And I create an account using name: "john", last name: "doe", pesel: "85010112345"
    When I perform incoming transfer of "100" to account with pesel "85010112345"
    Then Account with pesel "85010112345" has balance equal to "150.0"

  Scenario: User is able to perform outgoing transfer with sufficient balance
    Given Account registry is empty
    And I create an account using name: "jane", last name: "smith", pesel: "90010112345"
    And I perform incoming transfer of "200" to account with pesel "90010112345"
    When I perform outgoing transfer of "100" from account with pesel "90010112345"
    Then Account with pesel "90010112345" has balance equal to "250.0"

  Scenario: User cannot perform outgoing transfer with insufficient balance
    Given Account registry is empty
    And I create an account using name: "bob", last name: "builder", pesel: "88010112345"
    When I try to perform outgoing transfer of "500" from account with pesel "88010112345"
    Then Transfer should fail with status code "422"
    And Account with pesel "88010112345" has balance equal to "0.0"

  Scenario: User is able to perform express transfer
    Given Account registry is empty
    And I create an account using name: "alice", last name: "wonderland", pesel: "92010112345"
    And I perform incoming transfer of "300" to account with pesel "92010112345"
    When I perform express transfer of "100" from account with pesel "92010112345"
    Then Account with pesel "92010112345" has balance equal to "198.0"
