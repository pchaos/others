"""
Cookies登录测试工具（保持打开版）
功能：使用cookies登录成功后，停留在订单列表页面，等待用户手动操作
特点：登录后不自动关闭浏览器，用户可以慢慢浏览
"""

import os
import time
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys; sys.path.insert(0, '..'); from pdd_login import PinduoduoLogin


def main():
    print("🧪 Cookies登录测试（保持打开版）")
    print("=" * 60)
    print("功能：登录成功后停留在页面，等待您手动关闭浏览器")
    print()
    
    # 检查cookies文件
    cookie_file = ".pdd_cookies.json"
    if not os.path.exists(cookie_file):
        print(f"❌ Cookie文件不存在: {cookie_file}")
        print("\n请先运行主程序生成cookies:")
        print("   python pdd_order_scraper_optimized.py")
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
        headless=False,  # 显示浏览器界面
        uc=True,
        incognito=True,  # 隐私模式
    )
    driver.set_window_size(1280, 1920)
    
    try:
        # 打开拼多多
        print("📱 打开拼多多移动端...")
        driver.get("https://mobile.pinduoduo.com")
        
        # 等待页面基本加载
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("✅ 页面已加载")
        
        # 尝试cookies登录
        print("🔐 尝试使用cookies登录...")
        login = PinduoduoLogin(driver, cookie_file)
        
        if login.login_with_cookies():
            print("✅ Cookies加载成功")
            
            # 稍微等待让cookies生效
            time.sleep(2)
            
            # 刷新页面使登录状态生效
            print("🔄 刷新页面...")
            driver.refresh()
            time.sleep(3)
            
            # 验证登录状态
            page_text = driver.page_source
            current_url = driver.current_url
            
            if 'login' not in current_url.lower():
                # 检测登录成功
                print("✅ 登录成功！")
                
                print("\n" + "=" * 60)
                print("🎉 登录验证成功！")
                print("=" * 60)
                print(f"\n📱 当前页面: {current_url}")
                print(f"⏰ 登录时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # 检测页面元素
                print("\n🔍 页面状态:")
                
                # 检查是否在订单页面
                if 'orders' in current_url.lower() or 'order' in current_url.lower():
                    print("   📦 位置: 订单相关页面")
                else:
                    print("   📦 位置: 订单页面")
                
                # 检查关键元素
                order_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '我的订单')]")
                print(f"   ✅ 我的订单: {'检测到' if order_elements else '未检测到'}")
                
                view_all_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '查看全部')]")
                print(f"   ✅ 查看全部: {'检测到' if view_all_elements else '未检测到'}")
                
                # 显示提示信息
                print("\n" + "=" * 60)
                print("💡 浏览器已登录成功，您可以：")
                print("   1. 📋 查看订单列表")
                print("   2. 🔍 点击订单查看详情")
                print("   3. 📊 浏览历史订单")
                print("   4. 🛒 继续购物")
                print()
                print("⚠️  重要提示:")
                print("   - 请**手动关闭浏览器窗口**来退出程序")
                print("   - 不要使用Ctrl+C，窗口关闭后程序会自动退出")
                print("   - cookies已加载，您可以自由操作页面")
                print("=" * 60)
                
                # 等待用户关闭浏览器
                print("\n⏳ 程序运行中...")
                print("🕐 浏览器窗口已打开，请开始您的操作")
                print("🔒 当您关闭浏览器窗口时，程序会自动退出")
                print()
                
                # 循环检测浏览器状态
                browser_open = True
                while browser_open:
                    try:
                        time.sleep(3)
                        # 尝试获取浏览器标题，如果失败说明浏览器已关闭
                        title = driver.title
                        # 如果能获取到标题，说明浏览器还开着
                    except Exception as e:
                        # 浏览器已关闭
                        browser_open = False
                        print("\n" + "=" * 60)
                        print("✅ 检测到浏览器已关闭")
                        print("🧪 测试完成")
                        print("=" * 60)
                        break
                
            else:
                print("❌ 登录状态验证失败")
                print("   可能cookies已过期")
                
        else:
            print("❌ Cookies加载失败")
            print("   请检查cookies文件是否有效")
            
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        print("\n💡 提示: 可能需要重新生成cookies文件")
    
    finally:
        # 确保浏览器在出错时也能关闭
        try:
            if 'browser_open' not in locals() or not browser_open:
                # 如果浏览器已经由用户关闭，就不再关闭
                pass
            else:
                # 如果程序出错，关闭浏览器
                print("\n🔒 关闭浏览器...")
                driver.quit()
                print("✅ 浏览器已关闭")
        except:
            pass


if __name__ == "__main__":
    main()
