# Created by Radu at 04/06/2019

Feature: Test the ToDoMVC Angular web application

  Scenario: Check Default interface
    Given the app is open
    Then The title is visible
    And The new todo item field is visible
    And The footer is visible
    And A single list is visible


  Scenario Outline: Add a new ToDo item
    Given the app is open
    When I input: <task> in the new todo item field
    And Press the Enter Key
    Then The <task> is created as a to-do item
    And The remaining task counter increases

    Examples:
      | task            |
      | Delete Facebook |
      | Lawyer Up       |
      | Hit the Gym     |
      | Stay in School  |
      | Eat your Greens |


  Scenario Outline: Mark an item as done
    Given the app is open
    When I mark the task: "<tasktocheck>" as done via its checkbox
    Then The task: "<tasktocheck>" is marked as done
    And The task: "<tasktocheck>" becomes grey and crossed-through
    And The remaining task counter decreases

    Examples:
      | tasktocheck |
      | Lawyer Up   |
      | Hit the Gym |
