"""
Cookies登录测试工具（手动关闭版）
最简单的版本：登录成功后不做任何操作，等待用户手动关闭浏览器
"""

import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdd_login import PinduoduoLogin


def main():
    print("🧪 Cookies登录测试（手动关闭版）")
    print("=" * 60)
    
    # 检查cookies
    cookie_file = ".pdd_cookies.json"
    if not os.path.exists(cookie_file):
        print("❌ Cookie文件不存在")
        print("请先运行: python pdd_order_scraper_optimized.py")
        return
    
    # 读取cookies信息
    import json
    with open(cookie_file, "r") as f:
        data = json.load(f)
    print(f"✅ 找到cookies")
    print(f"   时间: {data.get('timestamp', '未知')}")
    print(f"   数量: {len(data.get('cookies', []))}")
    
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
        
        # 登录
        print("🔐 登录中...")
        login = PinduoduoLogin(driver, cookie_file)
        
        if login.login_with_cookies():
            print("✅ 登录成功！")
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            
            # 确认登录
            if 'login' not in driver.current_url.lower():
                print("✅ 登录状态确认")
                
                print("\n" + "=" * 60)
                print("🎉 登录成功！")
                print(f"📱 页面: {driver.current_url}")
                print()
                print("💡 现在您可以：")
                print("   - 查看订单列表")
                print("   - 点击查看详情")
                print("   - 慢慢浏览页面")
                print()
                print("⚠️  重要：请手动关闭浏览器窗口来退出程序")
                print("=" * 60)
                
                # 保持程序运行，直到浏览器被关闭
                while True:
                    time.sleep(5)
                    try:
                        # 尝试获取当前URL，如果失败说明浏览器关了
                        _ = driver.current_url
                    except:
                        print("\n✅ 检测到浏览器已关闭")
                        break
                
                print("🧪 测试完成")
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
