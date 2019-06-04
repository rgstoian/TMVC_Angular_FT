from selenium import webdriver

from pages.ToDoMVCPage import ToDoPage


def before_all(context):
    # context.browser = webdriver.Firefox()
    context.browser = webdriver.Chrome()
    context.browser.set_page_load_timeout(10)
    context.browser.implicitly_wait(10)
    context.browser.maximize_window()
    context.todo = ToDoPage(context.browser)


def after_all(context):
    context.browser.quit()
