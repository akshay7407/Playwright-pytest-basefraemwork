import xml.etree.ElementTree as ET
from pprint import pprint
import pyodbc
from datetime import datetime

class TestResultsDb():
    def __init__(self, server, database, username, password):
        connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.conn = pyodbc.connect(connection_string)
        print("Connected to SQL Server successfully!")
        self.cursor = self.conn.cursor()
    
    def create_table(self, table_name):
        self.cursor.execute(f'''
            CREATE TABLE [{table_name}] (
                status VARCHAR(50),
                testcase_name VARCHAR(255),
                fail_message VARCHAR(MAX),
                time VARCHAR(255),
                run_count INT,
                datetime DATETIME,
        
            )
        ''')
        self.conn.commit()

    def insert_results(self, table_name, testcase_name, time, status, fail_message):
        current_date = datetime.now() # Get current date

        # Format the current_datetime as a string to insert into the database
        formatted_datetime= current_date.strftime('%Y-%m-%d %H:%M:%S')


        # Query the current run_count for the test case
        self.cursor.execute(f'''
            SELECT COALESCE(MAX(run_count), 0) + 1
            FROM {table_name}
            WHERE testcase_name = ?;
        ''', (testcase_name,))

        run_count = self.cursor.fetchone()[0]  # Fetch the current run_count

        # Use INSERT statement to add a new row for each run
        self.cursor.execute(f'''
            INSERT INTO {table_name} (testcase_name, time, status, fail_message, run_count,datetime,label)
            VALUES (?, ?, ?, ?, ?, ?,?);
        ''', (testcase_name, time, status, fail_message, run_count,formatted_datetime,"Playwright"))

        self.conn.commit()

    def close_connection(self):
        self.conn.close()    
    
        
    
    def insert_test_report_data_to_db():
        tree = ET.parse('D:/Pytest-Base-Framework/reports/report.xml')
        root = tree.getroot()
        output_dict = {}

        # Create TestResultsDatabaseMS instance
        results_db = TestResultsDb(r"IB-PUNE-LAP-148\MSSQLSERVER2019", "automationResults", "sa", "server.123")

        #  Create a new table for each run
        # results_db.create_table("TestResult")

        for testcase in root.iter("testcase"):
            testcase_name = testcase.get("name")
            testcase_time = testcase.get("time")
            failure_element = testcase.find("failure")
            if failure_element is not None :
                failure_message = failure_element.get("message")
                status = "Fail"
            else :
                failure_message = None
                status = "Pass"

            # Insert data into the table
            results_db.insert_results("TestResult", testcase_name, testcase_time, status, failure_message)    

            testcase_dict = {"time": testcase_time, "status": status, "fail message": failure_message}
            output_dict[testcase_name] = testcase_dict

        # Print the output dictionary
        # pprint(output_dict)
        results_db.close_connection()

if __name__ =="__main__":
    TestResultsDb.insert_test_report_data_to_db()


