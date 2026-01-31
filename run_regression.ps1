# 设置 UTF-8 编码（避免所有中文警告）
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"

Write-Host "🧹 清理历史数据..." -ForegroundColor Yellow
Remove-Item -Recurse -Force allure-results -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Name allure-results | Out-Null

$total = 3
$allPass = $true

for ($i=1; $i -le $total; $i++) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  第 $i / $total 次回归测试" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    python -X utf8 -m pytest tests/test_login.py -v `
        --alluredir=./allure-results `
        --tb=line `
        -p no:warnings `
        --capture=no
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 第 $i 次失败！" -ForegroundColor Red
        $allPass = $false
        break
    } else {
        Write-Host "✅ 第 $i 次通过！" -ForegroundColor Green
    }
    
    Start-Sleep -Seconds 1
}

Write-Host "`n========================================" -ForegroundColor Magenta
if ($allPass) {
    Write-Host "🎉 3次回归测试全部通过！" -ForegroundColor Green
    Write-Host "生成 Allure 报告..." -ForegroundColor Cyan
    
    # 生成报告（使用 UTF-8 模式）
    python -X utf8 -c "from allure_combine import combine_allure; combine_allure('./allure-results', './allure-report-html')"
    
    if (Test-Path ./allure-report-html/index.html) {
        Write-Host "`n📊 报告已生成：allure-report-html/index.html" -ForegroundColor Green
        Start-Process ./allure-report-html/index.html
    } else {
        Write-Host "⚠️  allure-combine 失败，尝试备选方案..." -ForegroundColor Yellow
        # 备选：直接用浏览器打开结果文件夹（需要安装 allure 命令行）
        Write-Host "请安装 Allure CLI 后运行：allure serve allure-results" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ 回归测试未全部通过，请检查代码" -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Magenta
