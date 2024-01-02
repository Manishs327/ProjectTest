import time

from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BaseDriver:

    def __init__(self,driver):
        self.driver=driver



    def page_scroll(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while(True):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def wait_for_all_elements(self, locator_type, locator):
        wait = WebDriverWait(self.driver,10)
        return wait.until(expected_conditions.presence_of_all_elements_located((locator_type,locator)))

    def wait_until_element_clickable(self, locator_type, locator):
        wait = WebDriverWait(self.driver,10)
        return wait.until(EC.element_to_be_clickable((locator_type,locator)))
