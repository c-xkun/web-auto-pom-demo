from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure

class BasePage:
    """所有 Page 类的基类，封装通用操作"""
    
    def __init__(self, driver: WebDriver, base_url: str = None):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)
    
    def open(self, url: str = None):
        """打开页面"""
        target_url = url or self.base_url
        if target_url:
            with allure.step(f"打开页面: {target_url}"):
                self.driver.get(target_url)
        return self
    
    def find_element(self, locator, timeout=10) -> WebElement:
        """显式等待查找元素"""
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            allure.attach(f"定位器: {locator}", "元素查找失败", allure.attachment_type.TEXT)
            raise NoSuchElementException(f"无法找到元素: {locator}")
    
    def click(self, locator, timeout=10):
        """点击元素"""
        with allure.step(f"点击元素: {locator}"):
            element = self.find_element(locator, timeout)
            element.click()
        return self
    
    def send_keys(self, locator, text: str, clear=True, timeout=10):
        """输入文本"""
        with allure.step(f"在 {locator} 输入: {text}"):
            element = self.find_element(locator, timeout)
            if clear:
                element.clear()
            element.send_keys(text)
        return self
    
    def get_text(self, locator, timeout=10) -> str:
        """获取元素文本"""
        return self.find_element(locator, timeout).text
    
    def is_element_visible(self, locator, timeout=5) -> bool:
        """判断元素是否可见"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, name="screenshot"):
        """截图并添加到 Allure 报告"""
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
    
    def wait_for_element_visible(self, locator, timeout=10):
        """等待元素可见"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))