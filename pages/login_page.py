from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """本地登录页面对象"""
    
    # 改为本地地址
    URL = "http://localhost:8000/login.html"
    
    # 页面元素定位器（与线上版保持一致）
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[onclick='login()']")
    FLASH_MESSAGE = (By.ID, "flash")
    LOGOUT_BUTTON = (By.ID, "logoutBtn")

    def __init__(self, driver):
        super().__init__(driver, base_url=self.URL)
    
    def login(self, username: str, password: str):
        """执行登录操作"""
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self
    
    def get_flash_message(self) -> str:
        """获取提示信息"""
        return self.get_text(self.FLASH_MESSAGE)
    
    def is_logged_in(self) -> bool:
        """判断是否已登录（通过查找退出按钮是否可见）"""
        return self.find_element(self.LOGOUT_BUTTON).is_displayed()
    
    def logout(self):
        """登出"""
        if self.is_logged_in():
            self.click(self.LOGOUT_BUTTON)
        return self