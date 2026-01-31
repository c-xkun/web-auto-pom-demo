import pytest
import allure
import os
from utils.webdriver_factory import get_driver

@pytest.fixture(scope="function")
def driver(request):
    """测试级 fixture：每个测试方法启动一个浏览器实例"""
    browser = os.getenv("BROWSER", "edge")
    driver_path = os.getenv("DRIVER_PATH", None)
    
    driver = get_driver(browser=browser, driver_path=driver_path)
    driver.maximize_window()
    
    yield driver
    
    # 测试结束后：如果失败则截图
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="失败截图",
            attachment_type=allure.attachment_type.PNG
        )
        # 也保存页面源码方便调试
        allure.attach(
            driver.page_source,
            name="页面源码",
            attachment_type=allure.attachment_type.HTML
        )
    
    driver.quit()

@pytest.fixture
def login_page(driver):
    """页面对象 fixture"""
    from pages.login_page import LoginPage
    return LoginPage(driver)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """钩子：捕获测试结果状态"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)