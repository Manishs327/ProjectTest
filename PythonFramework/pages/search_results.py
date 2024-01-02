import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from base.basedriver import BaseDriver


class SearchResults(BaseDriver):
    all_stops1=0
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def filter_flights(self):
        self.driver.find_element(By.XPATH,"//p[text()='1']").click()
        time.sleep(1)
        return self.wait_for_all_elements(By.XPATH, "//span[@class='dotted-borderbtm']")



