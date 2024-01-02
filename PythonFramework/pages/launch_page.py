import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from base.basedriver import BaseDriver


class LaunchPage(BaseDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


    def departfrom(self,departlocation):
        depart_from = self.wait_until_element_clickable(By.ID,"BE_flight_origin_city")
        time.sleep(1)
        depart_from.click()
        time.sleep(1)
        depart_from.send_keys(departlocation)
        time.sleep(1)
        depart_from.send_keys(Keys.ENTER)
        time.sleep(1)

    def goingto(self, goingtolocation):
        going_to=self.wait_until_element_clickable(By.ID,"BE_flight_arrival_city")
        time.sleep(1)
        going_to.click()
        time.sleep(1)
        going_to.send_keys(goingtolocation)
        time.sleep(1)
        going_to.send_keys(Keys.ENTER)
        time.sleep(1)

    def selectdate(self, departuredate):
        origin_date=self.wait_until_element_clickable(By.NAME,"flight_origin_date")
        origin_date.click()
        all_date=self.wait_until_element_clickable(By.XPATH,"//tr/td")
        all_date=self.driver.find_elements(By.XPATH,"//tr/td")
        for ele in all_date:
            if(ele.get_attribute("id")==departuredate):
                ele.click()
                break

    def clicksearch(self):
        ele=self.wait_until_element_clickable(By.ID,"BE_flight_flsearch_btn")
        #ele.click()
        self.driver.execute_script("arguments[0].click();",ele)
        time.sleep(10)
        


