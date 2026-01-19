"""
拼多多登录模块 v1.0
从主爬虫中拆分出来的登录功能
支持短信登录和二维码登录
"""

import time
import json
import os
import random
import re
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PinduoduoLogin:
    def __init__(self, driver, cookie_file="pdd_cookies.json"):
        """
        初始化登录模块

        Args:
            driver: Selenium WebDriver实例
            cookie_file (str): Cookie文件路径，默认为"pdd_cookies.json"
        """
        self.driver = driver
        self.cookie_file = cookie_file
        self.display_mode = "unknown"
        self.is_already_on_orders_page = False

    def smart_wait(self, seconds_range=(2, 4)):
        """智能等待随机时间"""
        time.sleep(random.uniform(*seconds_range))

    def safe_find(self, xpath, timeout=15):
        """安全查找元素"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            return None

    def save_cookies(self):
        """
        保存当前cookies到文件
        
        Returns:
            bool: 保存是否成功
        """
        try:
            cookies = self.driver.get_cookies()
            cookie_data = {
                "cookies": cookies,
                "timestamp": datetime.now().isoformat(),
                "url": self.driver.current_url
            }
            with open(self.cookie_file, "w", encoding="utf-8") as f:
                json.dump(cookie_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Cookies已保存到 {self.cookie_file}")
            return True
        except Exception as e:
            print(f"❌ 保存cookies失败: {e}")
            return False

    def load_cookies(self):
        """
        从文件加载cookies
        
        Returns:
            dict or None: 包含cookies数据的字典，失败返回None
        """
        if not os.path.exists(self.cookie_file):
            print(f"Cookie文件不存在: {self.cookie_file}")
            return None
        
        try:
            with open(self.cookie_file, "r", encoding="utf-8") as f:
                cookie_data = json.load(f)
            print(f"✅ Cookies已从 {self.cookie_file} 加载")
            return cookie_data
        except Exception as e:
            print(f"❌ 加载cookies失败: {e}")
            return None

    def login_with_cookies(self):
        """
        使用保存的cookies尝试登录
        
        Returns:
            bool: 登录是否成功
        """
        print("尝试使用保存的cookies登录...")
        cookie_data = self.load_cookies()
        if not cookie_data:
            return False
        
        try:
            # 先访问主页
            self.driver.get("https://mobile.pinduoduo.com")
            self.smart_wait((2, 4))
            
            # 添加cookies
            for cookie in cookie_data["cookies"]:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    print(f"添加cookie失败: {e}")
                    continue
            
            # 再次访问个人中心页面
            self.driver.get("https://mobile.pinduoduo.com")
            self.smart_wait((3, 5))
            
            # 检查登录状态
            if self.check_login_status_fast():
                print("✅ Cookie登录成功！")
                return True
            else:
                print("❌ Cookie登录失败，需要重新认证")
                return False
                
        except Exception as e:
            print(f"❌ Cookie登录过程中出错: {e}")
            return False

    def click_personal_center_exact(self):
        """精确点击个人中心"""
        print("查找个人中心...")
        try:
            footer_items = self.driver.find_elements(By.CSS_SELECTOR, "div.footer-item")
            print(f"找到 {len(footer_items)} 个 footer-item 元素")
            for i, item in enumerate(footer_items):
                try:
                    text_elem = item.find_element(
                        By.CSS_SELECTOR, "div.footer-item-text"
                    )
                    text = text_elem.text
                    print(f"  第{i + 1}个: {text}")
                    if "个人中心" in text:
                        print(f"✅ 找到个人中心（第{i + 1}个）")
                        self.driver.execute_script("arguments[0].click();", item)
                        self.smart_wait((2, 3))
                        return True
                except:
                    continue
        except Exception as e:
            print(f"方法失败: {e}")
        print("\n提示：请手动点击底部的个人中心图标，然后按回车继续...")
        input()
        return True

    def login_sms(self, phone):
        """
        短信验证码登录

        Args:
            phone (str): 手机号码

        Returns:
            bool: 登录是否成功
        """
        print(f"使用短信登录: {phone[:3]}****{phone[-4:]}")
        print("查找短信登录选项...")
        sms_selectors = [
            "//*[contains(text(), '短信登录')]",
            "//*[contains(text(), '验证码登录')]",
        ]

        for selector in sms_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for elem in elements:
                    if elem.is_displayed():
                        print(f"✅ 找到短信登录选项")
                        self.driver.execute_script("arguments[0].click();", elem)
                        self.smart_wait((2, 4))
                        break
                else:
                    continue
                break
            except:
                continue

        print("输入手机号...")
        phone_input = self.safe_find("//input[@type='tel']")
        if not phone_input:
            phone_input = self.safe_find("//input[contains(@placeholder, '手机')]")

        if phone_input:
            phone_input.clear()
            for digit in phone:
                phone_input.send_keys(digit)
                time.sleep(random.uniform(0.2, 0.5))
        else:
            print("❌ 未找到手机号输入框")
            return False

        print("请求验证码...")
        code_btn = self.safe_find("//button[contains(text(), '获取验证码')]")
        if code_btn and code_btn.is_enabled():
            self.driver.execute_script("arguments[0].click();", code_btn)
            print("验证码已发送，请查收短信...")
            self.smart_wait((5, 10))
            code = input("请输入收到的验证码（6位数字）: ").strip()

            print("输入验证码...")
            code_input = self.safe_find(
                "//input[@type='tel' and contains(@placeholder, '验证码')]"
            )
            if not code_input:
                all_inputs = self.driver.find_elements(By.XPATH, "//input[@type='tel']")
                if len(all_inputs) >= 2:
                    code_input = all_inputs[1]

            if code_input:
                code_input.clear()
                for digit in code:
                    code_input.send_keys(digit)
                    time.sleep(random.uniform(0.3, 0.6))

                print("提交登录...")
                submit_btn = self.safe_find("//button[contains(text(), '登录')]")
                if submit_btn:
                    self.driver.execute_script("arguments[0].click();", submit_btn)
                    print("等待登录验证...")
                    time.sleep(5)
                    print("✅ 短信登录完成")
                    time.sleep(2)
                    return True
        return False

    def login_qr(self):
        """
        二维码登录

        Returns:
            bool: 登录是否成功
        """
        print("使用扫码登录...")
        print("查找扫码登录选项...")
        qr_selectors = [
            "//*[contains(text(), '扫码登录')]",
            "//*[contains(text(), '二维码登录')]",
        ]

        for selector in qr_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for elem in elements:
                    if elem.is_displayed():
                        self.driver.execute_script("arguments[0].click();", elem)
                        print("✅ 找到扫码登录选项")
                        break
            except:
                continue

        self.smart_wait((3, 5))
        print("等待二维码加载...")
        time.sleep(8)

        print("\n" + "=" * 50)
        print("请使用拼多多APP扫描屏幕上的二维码")
        print("=" * 50 + "\n")
        input("APP确认登录后，按回车继续...")

        print("验证登录状态...")
        # 验证登录是否真的成功
        if self.check_login_status_fast():
            print("✅ 扫码登录完成")
            time.sleep(2)
            return True
        else:
            print("❌ 扫码登录失败，未能检测到登录状态")
            return False

    def login_via_personal_center(self, phone=None, login_type="sms"):
        """
        通过个人中心入口登录

        Args:
            phone (str, optional): 手机号码（短信登录时必需）
            login_type (str): 登录类型，"sms" 或 "qr"

        Returns:
            bool: 登录是否成功
        """
        print("通过个人中心入口登录...")
        # 先尝试cookie登录
        if self.login_with_cookies():
            print("✅ 使用cookies成功登录")
            print("📋 登录流程完成，等待后续页面分析...")
            time.sleep(2)
            
            # 检测显示模式
            page_text = self.driver.page_source
            self.display_mode = self.detect_display_mode(page_text)
            print(f"📍 检测到显示模式: {self.display_mode}")
            
            return True
        
        print("Cookie登录失败，尝试手动登录...")
        print("访问拼多多首页...")
        self.driver.get("https://mobile.pinduoduo.com")
        self.smart_wait((4, 6))

        print("滚动到底部...")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        print("点击个人中心...")
        if not self.click_personal_center_exact():
            return False

        self.smart_wait((3, 5))

        if login_type == "sms":
            if not phone:
                print("❌ 短信登录需要提供手机号码")
                return False
            success = self.login_sms(phone)
        elif login_type == "qr":
            success = self.login_qr()
        else:
            print("❌ 不支持的登录类型")
            return False

        if success:
            # 保存cookies供下次使用
            self.save_cookies()
            print("✅ 登录成功！")
            print("📋 登录流程完成，等待后续页面分析...")
            time.sleep(2)

            # 检测显示模式
            page_text = self.driver.page_source
            self.display_mode = self.detect_display_mode(page_text)
            print(f"📍 检测到显示模式: {self.display_mode}")

            return True
        else:
            print("❌ 登录失败")
            return False

    def detect_display_mode(self, page_text):
        """
        检测订单显示模式

        Args:
            page_text (str): 页面文本内容

        Returns:
            str: 'overview', 'full_list', or 'unknown'
        """
        page_text_lower = page_text.lower()

        # ⭐ 检测是否为完整订单列表模式
        # 特征：有具体订单项（商品、金额、状态等）
        full_list_indicators = [
            # 检查是否有订单相关元素
            "order-item" in page_text_lower,
            "goods-item" in page_text_lower,
            "list-item" in page_text_lower,
            # 检查是否有多个订单状态
            page_text_lower.count("待付款")
            + page_text_lower.count("待发货")
            + page_text_lower.count("待收货")
            >= 3,
            # 检查是否有价格信息
            page_text_lower.count("¥") >= 5,
            # 检查是否有订单号
            bool(re.search(r"\d{10,20}", page_text)),
            # 检查是否有商品信息
            any(
                keyword in page_text_lower
                for keyword in ["商品", "购买", "购买记录", "订单详情"]
            ),
        ]

        if sum(full_list_indicators) >= 3:
            return "full_list"

        # ⭐ 检测是否为订单概览模式
        overview_indicators = [
            # 基本结构检测
            'class="order-menu"' in page_text,
            'class="order-title"' in page_text,
            'class="top-menu-wrapper"' in page_text,
            'class="top-menu"' in page_text,
            # 关键元素检测
            "我的订单" in page_text,
            "查看全部" in page_text,
            # 状态统计
            "待付款" in page_text,
            "待发货" in page_text,
            "待收货" in page_text,
            # 数字标签
            "long-number-tag" in page_text,
        ]

        if sum(overview_indicators) >= 4:
            return "overview"

        return "unknown"

    def check_login_status_fast(self):
        """快速检测登录状态 - 4.2优化版"""
        print("快速检测登录状态...")
        page_text = self.driver.page_source

        # 检测URL和基本状态
        current_url = self.driver.current_url.lower()
        if "login" in current_url:
            return False

        # 检测登录成功
        if self.is_logged_in_success_fast(page_text, current_url):
            print("✅ 登录检测成功！")
            return True

        return False

    def is_logged_in_success_fast(self, page_text, current_url):
        """快速检测登录成功 - 优化版"""
        page_text_lower = page_text.lower()
        current_url_lower = current_url.lower()

        if "login" in current_url_lower:
            return False

        # ⭐ 检测显示模式
        self.display_mode = self.detect_display_mode(page_text)

        # 优先检测用户提供的HTML结构（最快）
        if 'class="order-menu"' in page_text and 'class="order-title"' in page_text:
            print(f"   ✓ 检测到订单菜单结构")
            order_indicators = [
                'class="my-orders"',
                'class="others"',
                'class="top-menu-wrapper"',
                'class="top-menu"',
            ]
            found = [ind for ind in order_indicators if ind in page_text]
            if len(found) >= 3:
                print(f"   ✓ 订单结构匹配: {', '.join(found[:3])}")
                # 🎯 基于你提供的精确HTML结构检测登录成功
            if '<div class="order-menu"><div class="order-title">' in page_text:
                print("   ✓ 检测到完整的订单菜单结构")

                # 精确匹配你提供的HTML结构
                required_structure = [
                    '<div class="my-orders">我的订单</div>',
                    '<div class="others">查看全部</div>',
                    '<div class="top-menu-wrapper"',
                    '<div class="top-menu"',
                    "待付款",
                    "待分享",
                    "待发货",
                    "待收货",
                    "评价",
                ]

                found_count = sum(1 for elem in required_structure if elem in page_text)
                match_rate = found_count / len(required_structure)
                print(
                    f"   ✓ 结构匹配度: {found_count}/{len(required_structure)} ({match_rate * 100:.0f}%)"
                )

                if match_rate >= 0.8:  # 80%以上匹配度
                    print("   ✓ 🎯 确认登录成功！这是包含订单信息的页面")
                    print("   ✓ 检测到订单状态和'查看全部'按钮")
                    self.display_mode = "orders_overview"
                    self.is_already_on_orders_page = True
                    return True
                else:
                    print(f"   ⚠️ 结构匹配度不足: {match_rate * 100:.0f}%")

            return True

        # 检测关键文字
        key_indicators = [
            "我的订单",
            "查看全部",
            "待付款",
            "待发货",
            "待收货",
            "评价",
            "待分享",
            "order-menu",
            "order-title",
            "top-menu-wrapper",
            "top-menu",
        ]
        found = [ind for ind in key_indicators if ind in page_text]
        if len(found) >= 5:
            print(f"   ✓ 关键词匹配: {', '.join(found[:5])}")
            print(f"   ✓ 检测到显示模式: {self.display_mode}")
            return True

        # 检测其他登录成功标志
        success_indicators = [
            "我的拼多多",
            "个人中心",
            "订单管理",
            "退出登录",
            "我的钱包",
            "我的优惠券",
        ]
        for indicator in success_indicators:
            if indicator in page_text:
                print(f"   ✓ 检测到登录标志: {indicator}")
                return True

        return False

    def get_login_info(self):
        """
        获取登录信息

        Returns:
            dict: 包含登录状态的字典
        """
        return {
            "is_logged_in": self.check_login_status_fast(),
            "display_mode": self.display_mode,
            "is_already_on_orders_page": self.is_already_on_orders_page,
        }
