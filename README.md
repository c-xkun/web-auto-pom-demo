# Web-Auto-POM-Demo
Selenium + PageObject + pytest + Allure + GitHub Actions

![Python](https://img.shields.io/badge/Python-3.10-blue)
![pytest](https://img.shields.io/badge/pytest-7.4-green)
![Selenium](https://img.shields.io/badge/Selenium-4.15-orange)
![CI](https://github.com/c-xkun/web-auto-pom-demo/workflows/WebAuto-POM/badge.svg)

## 测试覆盖

✅ 功能测试：登录/登出流程  
✅ 边界测试：空值/超长字符串  
✅ 安全测试：SQL注入/XSS防护  
✅ UI测试：元素可见性验证  
✅ 稳定性测试：多次登录循环  

## 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动本地服务器（窗口1）
cd test_server && python -m http.server 8000

# 3. 运行测试（窗口2）
python -X utf8 -m pytest tests/test_login.py -v --html=report.html

# 4. 查看报告
start report.html