Feature: Shopping cart
  As a shopper
  I want to add products to my cart
  So that I can review the price before checkout

  Background:
    Given I am on the home page

  Scenario Outline: Cart calculates each line and the order total
    When I open the product "<product>"
    And I add it to the cart with quantity <quantity>
    And I view the shopping cart
    Then the cart contains "<product>" with quantity <quantity>
    And its line price equals unit price times quantity <quantity>
    And the cart total equals the sum of line prices

    Examples:
      | product             | quantity |
      | Combination Pliers  | 1        |
      | Claw Hammer         | 3        |
