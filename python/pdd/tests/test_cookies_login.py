"""
import time
测试Cookies登录脚本
功能：
1. 使用已保存的cookies尝试自动登录
2. 登录成功后等待用户手动关闭浏览器
3. 适合测试cookies是否有效
"""

import os
import sys
from datetime import datetime
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys; sys.path.insert(0, '..'); from pdd_login import PinduoduoLogin


def check_cookies_file():
    """检查cookies文件是否存在"""
    cookie_file = ".pdd_cookies.json"
    
    if not os.path.exists(cookie_file):
        print(f"❌ Cookie文件不存在: {cookie_file}")
        print("请先运行其他登录脚本生成cookies")
        return False
    
    try:
        import json
        with open(cookie_file, "r", encoding="utf-8") as f:
            cookie_data = json.load(f)
        
        cookies_count = len(cookie_data.get("cookies", []))
        save_time = cookie_data.get("timestamp", "未知")
        
        print(f"✅ Cookie文件存在")
        print(f"   文件: {cookie_file}")
        print(f"   cookies数量: {cookies_count}")
        print(f"   保存时间: {save_time}")
        
        return True
    except Exception as e:
        print(f"❌ 读取Cookie文件失败: {e}")
        return False


def test_cookies_login():
    """测试cookies登录"""
    print("=" * 60)
    print("🧪 测试Cookies登录")
    print("=" * 60)
    
    # 检查cookies文件
    if not check_cookies_file():
        print("\n💡 提示: 请先运行以下命令之一生成cookies:")
        print("   1. python test_qr_login_fix.py   # 扫码登录")
        print("   2. python pdd_order_scraper_optimized.py  # 主程序登录")
        return False
    
    print("\n🚀 启动浏览器...")
    
    # 启动浏览器（不是无头模式，方便查看）
    driver = Driver(
        browser="chrome",
        headless=False,  # 关闭无头模式，显示浏览器
        uc=True,
        incognito=True,  # 隐私模式
    )
    
    # 设置窗口大小
    driver.set_window_size(1280, 1920)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(10)
    
    try:
        # 导航到拼多多
        print("📱 打开拼多多移动端...")
        driver.get("https://mobile.pinduoduo.com")
        
        # 等待页面加载
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 初始化登录模块
        login = PinduoduoLogin(driver, ".pdd_cookies.json")
        
        print("\n🔐 尝试使用cookies登录...")
        
        # 尝试cookies登录
        if login.login_with_cookies():
            print("✅ Cookies登录成功！")
            
            # 刷新页面确保登录状态生效
            print("🔄 刷新页面...")
            driver.refresh()
            time.sleep(3)
            
            # 检查登录状态
            page_text = driver.page_source
            current_url = driver.current_url.lower()
            
            # 检测是否真的登录成功
            is_logged_in = False
            
            if "login" not in current_url:
                # 检查页面内容
                login_indicators = [
                    '我的订单', '个人中心', '我的拼多多', 'order-menu'
                ]
                
                found_indicators = [ind for ind in login_indicators if ind in page_text]
                
                if len(found_indicators) >= 2:
                    is_logged_in = True
                    print(f"✅ 登录状态确认: 检测到 {', '.join(found_indicators[:2])}")
            
            if is_logged_in:
                print("\n" + "=" * 60)
                print("🎉 登录成功！")
                print("=" * 60)
                print("📋 当前页面信息:")
                print(f"   URL: {driver.current_url}")
                print(f"   标题: {driver.title[:50] if driver.title else '无'}")
                
                # 显示登录后的关键元素
                print("\n🔍 检测到的页面元素:")
                
                # 检查订单相关元素
                order_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '订单')]")
                print(f"   📦 订单相关元素: {len(order_elements)} 个")
                
                # 检查个人中心
                profile_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '个人中心')]")
                print(f"   👤 个人中心元素: {len(profile_elements)} 个")
                
                print("\n" + "=" * 60)
                print("ℹ️  浏览器已打开，您可以:")
                print("   - 浏览订单页面")
                print("   - 检查cookies是否正常工作")
                print("   - 完成后请手动关闭浏览器")
                print("=" * 60)
                
                # 等待用户手动关闭
                print("\n⏳ 程序运行中，请手动关闭浏览器窗口退出...")
                print("(按 Ctrl+C 可强制退出)")
                
                # 保持浏览器打开直到用户关闭
                try:
                    # 定期检查浏览器是否还开着
                    while True:
                        time.sleep(5)
                        try:
                            # 尝试获取浏览器标题，如果失败说明浏览器已关闭
                            _ = driver.title
                        except:
                            print("\n✅ 检测到浏览器已关闭")
                            break
                            
                except KeyboardInterrupt:
                    print("\n\n⏹️ 用户中断，关闭浏览器...")
                    
                return True
            else:
                print("⚠️ Cookies可能已过期或无效")
                print("   登录状态未确认，请尝试重新登录")
                return False
        else:
            print("❌ Cookies登录失败")
            print("   可能是cookies已过期或文件损坏")
            return False
            
    except Exception as e:
        print(f"\n❌ 登录过程中出错: {e}")
        return False
    
    finally:
        # 关闭浏览器
        try:
            if driver:
                print("\n🔒 关闭浏览器...")
                driver.quit()
                print("✅ 浏览器已关闭")
        except:
            pass


def main():
    """主函数"""
    import time
    
    print("🧪 Cookies登录测试工具")
    print("=" * 60)
    print("功能: 使用保存的cookies自动登录，等待手动关闭浏览器")
    print()
    
    # 运行测试
    success = test_cookies_login()
    
    if success:
        print("\n✅ 测试完成")
    else:
        print("\n❌ 测试失败")
        print("💡 提示: 如果cookies无效，请先运行其他登录脚本:")
        print("   python test_qr_login_fix.py   # 扫码登录")


if __name__ == "__main__":
    main()
