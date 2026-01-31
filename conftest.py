import pytest
import allure
import os
import warnings
from utils.webdriver_factory import get_driver

# 忽略 urllib3 警告
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

@pytest.fixture(scope="function")
def driver(request):
    browser = os.getenv("BROWSER", "edge")
    driver_path = os.getenv("DRIVER_PATH", None)
    
    driver = get_driver(browser=browser, driver_path=driver_path)
    driver.maximize_window()
    
    yield driver
    
    # 失败截图
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="失败截图",
                attachment_type=allure.attachment_type.PNG
            )
        except:
            pass
    
    # 确保干净关闭（避免资源警告）
    try:
        driver.quit()
    except:
        pass

@pytest.fixture
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)