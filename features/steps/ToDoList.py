import time

from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

use_step_matcher("parse")

created_tasks = 0
completed_tasks = 0
created_tasks_temp = 0


@step("The {element} is visible")
def step_impl(context, element):
    # Used a dictionary to account for various cases in the feature file
    target: dict = {
        "title": context.todo.title,
        "new todo item field": context.todo.new_item_input,
        "footer": context.todo.footer
    }
    if element in target:
        assert target[element].is_displayed()
    else:
        raise Exception('Element not in list: ' + str(target.keys()))


@given("the app is open")
def step_impl(context):
    global created_tasks_temp
    context.browser.get('http://todomvc.com/examples/angularjs/#/')
    # The remaining item counter cannot be parsed from zero,
    # So we initialize it manually
    if context.todo.remaining_item_counter.is_displayed():
        created_tasks_temp = int(context.todo.remaining_item_counter.text)
    else:
        created_tasks_temp = 0


@step("I input: {task} in the new todo item field")
def step_impl(context, task):
    global created_tasks
    created_tasks += 1
    context.todo.new_item_input.send_keys(task)


@step("Press the Enter Key")
def step_impl(context):
    context.todo.new_item_input.send_keys(Keys.ENTER)


@then("The {task} is created as a to-do item")
def step_impl(context, task):
    assert context.todo.list_item(task).is_displayed()


@step('The task: "{task}" is marked as done')
def step_impl(context, task):
    item: WebElement = context.todo.list_item(task)
    # The item is marked with the class 'completed' when done
    class_string: str = item.get_attribute("class")
    assert "completed" in class_string


@step('I mark the task: "{tasktocheck}" as done via its checkbox')
def step_impl(context, tasktocheck):
    global completed_tasks
    context.todo.list_item_checkbox(tasktocheck).click()
    completed_tasks += 1


@step("The remaining task counter {counter_state}")
def step_impl(context, counter_state):
    global created_tasks
    global created_tasks_temp
    global completed_tasks
    result: int = (created_tasks - completed_tasks) - created_tasks_temp
    if counter_state == 'increases':
        assert result == 1
    elif counter_state == 'decreases':
        assert result == -1
    else:
        raise Exception('used verbs for the task counter are: increases, decreases')


@step('The task: "{tasktocheck}" becomes grey and crossed-through')
def step_impl(context, tasktocheck):
    # Marking an item as done has a transition from black to grey
    # With no markers in the DOM for the transition end, so we wait on it
    time.sleep(.5)

    target: WebElement = context.todo.list_item_label(tasktocheck)
    color: str = target.value_of_css_property('color')
    text_dec: str = target.value_of_css_property('text-decoration')

    browser_name: str = context.browser.capabilities['browserName']
    # Firefox and Chrome handle CSS properties differently
    # Firefox uses RGB for color and no info on text-decoration
    # Chrome uses RGBA for color and separate color info on text-decoration
    # So we assert the common parts
    if browser_name == 'firefox' or browser_name == 'chrome':
        assert '217, 217, 217' in color
        assert 'rgb' in color
        assert 'line-through' in text_dec
    else:
        # Only tested on FF and Chrome
        raise Exception('Browser ' + browser_name + ' not supported.')


@step("A single list is visible")
def step_impl(context):
    result = context.browser.find_elements(By.CSS_SELECTOR, 'section.todoapp')
    assert len(result) == 1
