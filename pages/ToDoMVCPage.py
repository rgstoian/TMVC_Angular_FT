from page_objects import PageObject, PageElement
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class ToDoPage(PageObject):
    title: WebElement = PageElement(css='header.header>h1')
    new_item_input: WebElement = PageElement(css='input.new-todo')
    footer: WebElement = PageElement(css='footer.info')
    todo_list: WebElement = PageElement(css='ul.todo-list')
    remaining_item_counter: WebElement = PageElement(css='span.todo-count>strong')

    def list_item(self, text):
        result: WebElement = self.todo_list
        return result.find_element(By.XPATH, ".//li[descendant::div/label[text()='" + text + "']]")

    def list_item_label(self, text):
        return self.list_item(text).find_element(By.XPATH, ".//label")

    def list_item_checkbox(self, text):
        result: WebElement = self.list_item(text)
        return result.find_element(By.XPATH, ".//input[@type='checkbox']")
