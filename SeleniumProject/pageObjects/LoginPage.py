class Login:
    textbox_username_xpath="//input[@name='userName']"
    text_password_xpath = "//input[@name='password']"
    button_Submit_xpath="//input[@name='submit']"

    def __init__(self, driver):
        self.driver = driver


    def set_user_name(self,username):
        self.driver.implicitly_wait(20)
        self.driver.find_element("xpath",self.textbox_username_xpath).clear()
        self.driver.find_element("xpath",self.textbox_username_xpath).send_keys(username)

    def set_password(self,password):
        self.driver.implicitly_wait(5)
        self.driver.find_element("xpath",self.text_password_xpath).clear()
        self.driver.find_element("xpath",self.text_password_xpath).send_keys(password)

    def click_submit(self):
        self.driver.find_element("xpath", self.button_Submit_xpath).click()
        self.driver.implicitly_wait(20)
