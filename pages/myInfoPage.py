
from base.basepage import BasePage
from utilities.read_properties import *
from playwright.sync_api import Page


class MyInfoPage(BasePage):
    
    def __init__(self, page:Page):
        super().__init__(page)
        self.page =page

    dashboard_elements_xpath = "//ul[@class='oxd-main-menu']/li/a/span"
    requirement_role_link = "Recruitment"  
        # page.get_by_role("link", name="").click()
        
    def get_myinfo_sidebar_elements(self):
        self.log.info("Get sidebar info elements")
        return  self.find_locator(self.dashboard_elements_xpath)
    
    def click_on_requirement_role(self):
        self.click_element('link','get_by_role',name=self.requirement_role_link) 
        
    
 