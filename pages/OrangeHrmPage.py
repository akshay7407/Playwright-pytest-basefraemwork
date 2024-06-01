from base.basepage import BasePage
from utilities.read_properties import *
from utilities.read_properties import read_properties as cp 
from playwright.sync_api import Page


class OrangeHrmPage(BasePage):

    def __init__(self, page:Page):
        super().__init__(page)
        self.page = page

    tfUserName_xpath = "//input[@name='username']"
    tfPassword_xpath = "//input[@name='password']"
    login_role = "Login"
    
    def loginToHomePage(self):
        self.log.info("Enter userName and password")
        self.log.info(f"Enter username :"+ cp('USERNAME'))
        self.send_text(cp('USERNAME'),self.tfUserName_xpath )
        self.log.info(f"Enter password :"+ cp('PASS'))
        self.send_text(cp('PASS'),self.tfPassword_xpath)
        self.click_element('button', 'get_by_role',name=self.login_role)
