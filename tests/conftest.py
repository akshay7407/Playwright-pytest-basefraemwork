import os
import pytest
from playwright.sync_api import Playwright, expect

from utilities.read_properties import read_properties as cp

page = None

@pytest.fixture(scope='function', autouse=True)
def setup_test(request, playwright: Playwright):
    global page
    headless_mode = request.config.getoption("--headless")
    print("Headless Mode:", headless_mode)
    environment = request.config.getoption("--environment")
    args = []

    if headless_mode:
        args.append("--window-size=1920,1080")

    browser = playwright.chromium.launch(channel="chrome", headless=headless_mode, args=['--start_maximized', *args])
    context = browser.new_context(no_viewport=False)
    page = context.new_page()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    if environment == "qa":
        base_url = cp('BASE_URL')
    elif environment == "dev":
        base_url = cp('TEST_URL')
    else:
        raise ValueError("Invalid environment")

    page.goto(base_url)
    # 10 seconds wait for expect condition satisfy
    expect.set_options(timeout=10000)
    #  10 seconds wait for get element from dom
    page.set_default_timeout(10000)

    # If you are using `request.cls` to assign page to class
    if request.cls is not None:
        request.cls.page = page
    yield page
    # Stopping tracing and handling failed tests
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.failed:
            trace_path = os.path.join(os.getcwd(), 'reports', 'trace_failure', f'trace-failure-{request.node.name}.zip')
            context.tracing.stop(path=trace_path)
        else:
            context.tracing.stop()
    else:
        pass        
    page.close()
    context.close()
    browser.close()

def pytest_addoption(parser):
    parser.addoption("--browser_name", default="chrome", help="browser name")
    parser.addoption("--environment", action="store", default="dev", help="Specify the test environment (dev, staging, production).")
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")

def take_screenshot(name):
    page.screenshot(path=name)

def pytest_html_report_title(report):
    # set project title to display in report
    report.title = "Akshay Gaikwad Project"    

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            index =file_name.index("test_")
            file_name = file_name[index:]
            file_path = "./reports/"+file_name
            take_screenshot(file_path)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra