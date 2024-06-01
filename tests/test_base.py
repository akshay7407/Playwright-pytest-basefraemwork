
import pytest
from pages.OrangeHrmPage import OrangeHrmPage
from pages.myInfoPage import MyInfoPage

class TestBase:

    @pytest.fixture(autouse="true")
    def class_objects(self,setup_test):
        page =setup_test
        self.myInfoPage_obj = MyInfoPage(page)
        self.orangeHrm_obj = OrangeHrmPage(page)