"""
Cookies登录测试工具（简单版）
功能：使用cookies登录，浏览器打开后等待您手动关闭
"""

import os
import time
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys; sys.path.insert(0, '..'); from pdd_login import PinduoduoLogin


def main():
    print("🧪 Cookies登录测试")
    print("=" * 50)
    
    # 检查cookies文件
    cookie_file = ".pdd_cookies.json"
    if not os.path.exists(cookie_file):
        print(f"❌ Cookie文件不存在: {cookie_file}")
        print("请先运行其他登录脚本生成cookies")
        return
    
    # 显示cookies信息
    import json
    with open(cookie_file, "r") as f:
        data = json.load(f)
    print(f"✅ 找到cookies文件")
    print(f"   保存时间: {data.get('timestamp', '未知')}")
    print(f"   cookies数量: {len(data.get('cookies', []))}")
    
    # 启动浏览器
    print("\n🚀 启动浏览器...")
    driver = Driver(
        browser="chrome",
        headless=False,
        uc=True,
        incognito=True,
    )
    driver.set_window_size(1280, 1920)
    
    try:
        # 打开拼多多
        print("📱 打开拼多多...")
        driver.get("https://mobile.pinduoduo.com")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 尝试cookies登录
        print("🔐 尝试cookies登录...")
        login = PinduoduoLogin(driver, cookie_file)
        
        if login.login_with_cookies():
            print("✅ Cookies登录成功！")
            driver.refresh()
            time.sleep(2)
            
            # 验证登录状态
            if 'login' not in driver.current_url.lower():
                print("✅ 登录状态确认")
                
                print("\n" + "=" * 50)
                print("🎉 登录成功！")
                print(f"📱 当前页面: {driver.current_url}")
                print("💡 您可以:")
                print("   - 浏览订单页面")
                print("   - 测试cookies是否正常工作")
                print("   - 完成后请手动关闭浏览器窗口")
                print("=" * 50)
                
                # 等待用户关闭浏览器
                print("\n⏳ 浏览器已打开，等待您手动关闭...")
                print("(关闭窗口即可退出程序)")
                
                while True:
                    try:
                        time.sleep(2)
                        _ = driver.title
                    except:
                        print("\n✅ 检测到浏览器已关闭")
                        break
        else:
            print("❌ Cookies登录失败")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    main()
