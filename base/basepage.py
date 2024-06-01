import utilities.custom_logger as cl
from playwright.sync_api import Page
import pyodbc

class BasePage:
    log = cl.custom_logger()

    def __init__(self, page:Page):
        self.page = page
        
    def find_locator(self , selector , selector_method = 'locator',*args,**kwargs):
        self.page.wait_for_load_state()
        try:
            selector_function = getattr(self.page , selector_method)
            element = selector_function(selector,*args,**kwargs)
            if element:
                return element
        except Exception as e:
            self.log.info(f'Element cannot be found at {selector}'+str(e))
            return
        return None     

    def click_element(self, selector , selector_method = 'locator',*args,**kwargs):
        """
        method to click an element
        """
        element = None
        try:
            element = self.find_locator(selector , selector_method ,*args,**kwargs)
            element.click()
            self.log.info(f"Clicked on  element with given value {selector}")
        except Exception as e:
            self.log.info(f"Element cannot be clicked at {selector}: "+ str(e))
            assert False

    def send_text(self, text ,selector , selector_method = 'locator',*args,**kwargs):
        """
        method to write text into the element
        """
        element = None
        try:
          
            element = self.find_locator(selector , selector_method ,*args,**kwargs)
            element.fill(text)
            self.log.info(f"Send text to element with given value {selector}")
        except Exception as e:
            self.log.info(f"Unable to send text to element with given value {selector} "+ str(e))
            assert False

    def get_dropdown_values_db(self,table):
        connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER=IB-PUNE-LAP-148\MSSQLSERVER2019;DATABASE=automationResults;UID=sa;PWD=server.123'
        self.conn = pyodbc.connect(connection_string)
        print("Connected to SQL Server successfully!")
        try:
            with self.conn.cursor() as connect:
                connect.execute(f"select * from {table}")
                list_value= connect.fetchall()
                dd_val = [item[0] for item in list_value]
                return dd_val                
        except:
            pass
        finally:
            self.conn.close()
