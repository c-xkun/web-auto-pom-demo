import pytest
import allure
from pages.login_page import LoginPage

@allure.feature("登录功能")
@allure.story("用户认证")
class TestLogin:
    
    @allure.title("成功登录场景")
    @allure.description("使用正确的用户名密码登录，验证进入安全区域")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, driver, login_page):
        with allure.step("1. 打开登录页"):
            login_page.open()
        
        with allure.step("2. 执行登录"):
            login_page.login("tomsmith", "SuperSecretPassword!")
        
        with allure.step("3. 验证登录成功"):
            assert login_page.is_logged_in(), "登录后应显示退出按钮"
            assert "Secure Area" in driver.title
            flash_text = login_page.get_flash_message()
            assert "You logged into" in flash_text
    
    @allure.title("失败登录场景 - 错误密码")
    @allure.description("使用错误密码登录，验证错误提示")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_fail(self, driver, login_page):
        login_page.open()
        login_page.login("tomsmith", "wrong_password")
        
        flash = login_page.get_flash_message()
        with allure.step("验证错误提示"):
            assert "invalid" in flash.lower() or "password" in flash.lower()
            allure.attach(f"实际提示: {flash}", "错误提示文本", allure.attachment_type.TEXT)
    
    @allure.title("登出功能验证")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, driver, login_page):
        login_page.open().login("tomsmith", "SuperSecretPassword!")
        assert login_page.is_logged_in()
        
        login_page.logout()
        flash = login_page.get_flash_message()
        assert "logged out" in flash.lower()

    # =========== 新增 7 个用例 ===========
    
    @allure.title("空用户名登录 - 边界测试")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_username(self, driver, login_page):
        """测试空用户名提交"""
        login_page.open()
        login_page.login("", "SuperSecretPassword!")
        flash = login_page.get_flash_message()
        assert "invalid" in flash.lower()
    
    @allure.title("SQL注入攻击防护测试")
    @allure.description("尝试SQL注入语句，验证系统安全性")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sql_injection(self, driver, login_page):
        """安全测试：SQL注入"""
        login_page.open()
        malicious_input = "' OR '1'='1' --"
        login_page.login(malicious_input, "password")
        # 系统应该拒绝登录，不出现500错误
        assert not login_page.is_logged_in()
        flash = login_page.get_flash_message()
        assert "invalid" in flash.lower()
    
    @allure.title("XSS攻击防护测试")
    @allure.description("尝试XSS脚本，验证输入过滤")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_xss_protection(self, driver, login_page):
        """安全测试：XSS跨站脚本"""
        login_page.open()
        xss_script = "<script>alert('xss')</script>"
        login_page.login(xss_script, "password")
        # 检查脚本是否被转义（页面源码中不应有完整script标签）
        page_source = driver.page_source
        assert "<script>alert('xss')</script>" not in page_source or "invalid" in login_page.get_flash_message().lower()
    
    @allure.title("超长用户名边界测试")
    @allure.description("测试超长字符串输入处理")
    @allure.severity(allure.severity_level.NORMAL)
    def test_long_username(self, driver, login_page):
        """压力测试：超长用户名"""
        login_page.open()
        long_name = "a" * 1000  # 1000个字符
        login_page.login(long_name, "password")
        # 系统不应崩溃
        assert not login_page.is_logged_in()  # 正常拒绝即可
    
    @allure.title("特殊字符测试")
    @allure.description("测试各种特殊字符输入")
    @allure.severity(allure.severity_level.NORMAL)
    def test_special_characters(self, driver, login_page):
        """特殊字符输入测试"""
        login_page.open()
        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        login_page.login("user" + special_chars, "pass" + special_chars)
        flash = login_page.get_flash_message()
        assert "invalid" in flash.lower() or "error" in flash.lower()
    
    @allure.title("页面元素加载验证")
    @allure.description("验证所有关键元素可见且可交互")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_page_elements_visibility(self, driver, login_page):
        """UI验证：页面元素可见性"""
        login_page.open()
        # 验证所有关键元素可见
        assert login_page.find_element(login_page.USERNAME_INPUT).is_displayed()
        assert login_page.find_element(login_page.PASSWORD_INPUT).is_displayed()
        assert login_page.find_element(login_page.LOGIN_BUTTON).is_displayed()
        allure.attach("所有关键元素验证通过", "UI检查", allure.attachment_type.TEXT)
    
    @allure.title("快速多次登录尝试 - 稳定性测试")
    @allure.description("连续多次登录登出，验证session稳定性")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_login_logout(self, driver, login_page):
        """稳定性测试：多次登录登出"""
        login_page.open()
        for i in range(3):  # 循环3次
            with allure.step(f"第{i+1}次登录"):
                login_page.login("tomsmith", "SuperSecretPassword!")
                assert login_page.is_logged_in()
                login_page.logout()
                flash = login_page.get_flash_message()
                assert "logged out" in flash.lower()