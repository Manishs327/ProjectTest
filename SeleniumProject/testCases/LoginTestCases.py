import pytest
from selenium import webdriver

from Utilities.readFiles import ReadConfig
from pageObjects.LoginPage import Login
from webdriver_manager.chrome import ChromeDriverManager
from Utilities.customlogger import LogGen
import time

class Test_001_login:
    baseURL= ReadConfig.get_app_url()
    username= ReadConfig.get_username()
    password= ReadConfig.get_password()
    expected_title_welcome="Welcome: Mercury Tours"
    expected_title_login="Login: Mercury Tours"
    logger=LogGen.loggen()
    def test_home_page_title(self, setUp):
        self.logger.info("*************** Test_001_Login *****************")
        self.driver=setUp
        self.driver.get(self.baseURL)
        self.logger.info("The URL entered is ")
        actual_title=self.driver.title
        self.logger.info("The title of the home page is ")
        if(actual_title==self.expected_title_welcome):
            self.logger.info("The home page title test is passed")
            assert True
        else:
            self.logger.info("The home page title test is failed")
            assert False

    def test_login(self, setUp):
        self.driver=setUp
        self.driver.get(self.baseURL)
        self.login = Login(self.driver)
        self.login.set_user_name(self.username)
        self.login.set_password(self.password)
        self.login.click_submit()
        self.driver.implicitly_wait(20)
        actual_title_login = self.driver.title
        print(actual_title_login)
        if(actual_title_login==self.expected_title_login):
            self.logger.info("The Login Test Case is passed")
            assert True
        else:
            self.logger.info("The Login Test Case is failed")
            self.driver.save_screenshot(".//Screenshots//failure.png")
            self.driver.close()
            assert False



