"""
快速测试版：验证登录后浏览器保持打开
"""

import os
import sys
import time

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdd_login import PinduoduoLogin

def main():
    print("🧪 快速测试：登录后保持浏览器打开")
    print("=" * 60)
    
    cookie_file = ".pdd_cookies.json"
    if not os.path.exists(cookie_file):
        print("❌ Cookie文件不存在")
        return
    
    print("✅ 找到cookies文件")
    
    # 启动浏览器
    driver = Driver(browser="chrome", headless=False, uc=True, incognito=True)
    driver.set_window_size(1280, 1920)
    
    try:
        # 打开拼多多
        print("📱 打开拼多多...")
        driver.get("https://mobile.pinduoduo.com")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # 登录
        print("🔐 登录中...")
        login = PinduoduoLogin(driver, cookie_file)
        
        if login.login_with_cookies():
            print("✅ 登录成功！")
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            
            if 'login' not in driver.current_url.lower():
                print("✅ 登录状态确认")
                print("\n" + "=" * 60)
                print("🎉 登录成功！")
                print(f"📱 页面: {driver.current_url}")
                print("\n💡 现在浏览器已打开，您可以：")
                print("   - 查看订单列表")
                print("   - 点击查看详情")
                print("   - 慢慢浏览")
                print("\n⚠️  请手动关闭浏览器窗口来退出程序")
                print("=" * 60)
                
                # 等待用户关闭浏览器（最多60秒演示）
                print("\n⏳ 等待浏览器关闭（演示60秒超时）...")
                start_time = time.time()
                while time.time() - start_time < 60:
                    try:
                        time.sleep(2)
                        _ = driver.current_url
                    except:
                        print("\n✅ 浏览器已关闭")
                        return
                print("\n⏰ 演示超时，关闭浏览器")
                return
        
        print("❌ 登录失败")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()
