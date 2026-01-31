import os
import shutil
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService

def get_driver(browser="edge", driver_path=None):
    """
    获取 WebDriver 实例
    优先级：1.指定路径 2.系统PATH 3.自动下载(webdriver-manager)
    """
    browser = browser.lower()
    
    if browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        
        service = None
        
        # 优先级1: 指定路径
        if driver_path and os.path.exists(driver_path):
            service = EdgeService(executable_path=driver_path)
            print(f"✅ 使用指定驱动: {driver_path}")
        
        # 优先级2: 系统 PATH 查找
        elif shutil.which("msedgedriver"):
            # 不传参数，让 Selenium 自动去 PATH 中找
            service = EdgeService()
            print("✅ 使用系统 PATH 中的 msedgedriver")
        
        # 优先级3: 尝试自动下载（需网络）
        else:
            try:
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                service = EdgeService(EdgeChromiumDriverManager().install())
                print("⚠️ 正在自动下载驱动...")
            except Exception as e:
                raise Exception("❌ 找不到 Edge 驱动！请确保 msedgedriver.exe 在 PATH 中或指定路径") from e
        
        return webdriver.Edge(service=service, options=options)
    
    elif browser == "chrome":
        # 类似逻辑...
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        
        if driver_path and os.path.exists(driver_path):
            service = ChromeService(executable_path=driver_path)
        elif shutil.which("chromedriver"):
            service = ChromeService()
        else:
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
            except Exception as e:
                raise Exception("❌ 找不到 Chrome 驱动！") from e
        
        return webdriver.Chrome(service=service, options=options)
    
    else:
        raise ValueError(f"不支持的浏览器: {browser}")