import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #wait=WebDriverWait(driver,10)
    driver.maximize_window()
    driver.get("https://www.yatra.com")
    request.cls.driver=driver
    #request.cls.wait=wait
    yield
    driver.close()


