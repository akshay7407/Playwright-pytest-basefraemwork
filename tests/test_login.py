
from os import name
import pytest
import utilities.custom_logger as cl
from tests.test_base import TestBase
from utilities.read_properties import read_json
from playwright.sync_api import expect


class TestLogin(TestBase):

    log = cl.custom_logger()

    @pytest.mark.smoke      
    def test_Validate_title(self):
        self.log.info("Verify the orange HTM site title ")
        self.orangeHrm_obj.loginToHomePage()
        expect(self.page).to_have_title('OrangeHRM')
  
    @pytest.mark.regression    
    def test_validate_sidebar_elements(self):
        self.log.info("Verify the orange HTM side bar elements")
        data =read_json('jsonData')['boardElements']
        self.orangeHrm_obj.loginToHomePage()
        elements = self.myInfoPage_obj.get_myinfo_sidebar_elements()
        # get elements of lits can be validated with contain text as well 
        expect(elements).to_have_text(data)
        self.myInfoPage_obj.click_on_requirement_role()
        # wait for 10 seconds 
        self.page.wait_for_timeout(10000)
        assert False

    @pytest.mark.smoke 
    def test_db_val(self):
        self.log.info("Verify the db values")
        values = self.orangeHrm_obj.get_dropdown_values_db("TestResult")
        print(values)
        print(len(values))

    @pytest.mark.smoke 
    def test_verify_json_file(self):
        self.log.info("Verify the json file values ")
        data =read_json('jsonData')['credential']
        print(data['username'])
        print(data['password'])
    
