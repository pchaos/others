"""
拼多多个人订单爬取工具 v4.2
新增功能：
1. Chrome窗口设置为1280x1920
2. 检测订单显示模式（概览模式 vs 完整列表模式）
3. 根据显示模式调整点击策略
"""

import os
import json
import time
import random
import re
from datetime import datetime
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdd_login import PinduoduoLogin


class PinduoduoOrderScraper:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.orders = []
        self.is_already_on_orders_page = False
        self.display_mode = "unknown"  # unknown, overview, full_list
        self.login_module = None  # 登录模块实例

    def start_browser(self):
        print("启动浏览器...")
        self.driver = Driver(
            browser="chrome",
            headless=self.headless,
            uc=True,
            incognito=True,
        )
        self.driver.set_page_load_timeout(60)
        self.driver.implicitly_wait(10)

        # ⭐ Chrome窗口设置为1280x1920 (移动端优化)
        self.driver.set_window_size(1280, 1920)  # 宽度1280，高度1920
        # 初始化登录模块
        self.login_module = PinduoduoLogin(self.driver, ".pdd_cookies.json")
        print("浏览器启动成功 (1280x1920 移动端优化)")
        return self

    def smart_wait(self, seconds_range=(2, 4)):
        time.sleep(random.uniform(*seconds_range))

    def detect_display_mode(self, page_text):
        """
        检测订单显示模式

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
                    print("✅ 短信登录完成，等待后续分析...")
                    time.sleep(2)
                    return True
        return False

    def login_qr(self):
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
        print("✅ 扫码登录完成，等待后续分析...")
        time.sleep(2)
        return True

    def safe_find(self, xpath, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            return None

    def check_login_status_fast(self):
        """快速检测登录状态"""
        print("快速检测登录状态...")
        for i in range(2):  # 只检查2次
            time.sleep(2)
            page_text = self.driver.page_source
            current_url = self.driver.current_url
            if "验证码" in page_text and "滑动" in page_text:
                print("⚠️ 需要滑动验证码...")
                input("请在浏览器中完成验证，按回车继续...")
                continue
            # 检测登录成功
            if self.is_logged_in_success_fast(page_text, current_url):
                print("✅ 登录成功！")
                return True
            print(f"⏳ 等待登录中... ({i + 1}/2)")
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

    def click_view_all_orders_by_mode(self):
        """
        根据显示模式点击查看全部
        """
        print(f"检测到订单显示模式: {self.display_mode}")

        if self.display_mode == "overview":
            print("✅ 订单概览模式 - 点击'查看全部'进入完整列表")
            return self.click_view_all_orders_overview()
        elif self.display_mode == "full_list":
            print("✅ 完整订单列表模式 - 无需点击，直接开始爬取")
            return True
        else:
            print("⚠️ 未检测到订单页面")
            return False

    def click_view_all_orders_overview(self):
        """概览模式下点击查看全部"""
        print("在概览模式，点击查看全部...")
        try:
            # 方法1: 通过CSS选择器直接定位
            view_all_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.others")
            print(f"找到 {len(view_all_elements)} 个 div.others 元素")
            for i, elem in enumerate(view_all_elements):
                try:
                    text = elem.text.strip()
                    print(f"  第{i + 1}个: '{text}'")
                    if "查看全部" in text:
                        print(f"✅ 找到查看全部（第{i + 1}个）")
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView(true);", elem
                        )
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", elem)
                        self.smart_wait((3, 5))
                        print("✅ 已点击查看全部，等待跳转...")
                        time.sleep(5)  # 等待页面跳转
                        return True
                except:
                    continue
        except Exception as e:
            print(f"方法1失败: {e}")

        # 方法2: 备用XPATH查找
        try:
            text_elements = self.driver.find_elements(
                By.XPATH, "//*[contains(text(), '查看全部')]"
            )
            print(f"找到 {len(text_elements)} 个包含'查看全部'的元素")
            for i, elem in enumerate(text_elements):
                try:
                    print(f"  第{i + 1}个元素，点击...")
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", elem
                    )
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", elem)
                    print("✅ 通过XPATH找到查看全部")
                    self.smart_wait((3, 5))
                    return True
                except:
                    continue
        except Exception as e:
            print(f"方法2失败: {e}")

        print("❌ 未找到查看全部按钮")
        return False

    def click_view_all_orders(self):
        """点击查看全部按钮 - 通用版"""
        print("查找查看全部按钮...")

        # 方法1: 通过CSS选择器直接定位
        try:
            view_all_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.others")
            print(f"找到 {len(view_all_elements)} 个 div.others 元素")
            for i, elem in enumerate(view_all_elements):
                try:
                    text = elem.text.strip()
                    print(f"  第{i + 1}个: '{text}'")
                    if "查看全部" in text:
                        print(f"✅ 找到查看全部（第{i + 1}个）")
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView(true);", elem
                        )
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", elem)
                        self.smart_wait((3, 5))
                        return True
                except:
                    continue
        except Exception as e:
            print(f"方法1失败: {e}")

        # 方法2: 通过XPATH查找
        try:
            text_elements = self.driver.find_elements(
                By.XPATH, "//*[contains(text(), '查看全部')]"
            )
            print(f"找到 {len(text_elements)} 个包含'查看全部'的元素")
            for i, elem in enumerate(text_elements):
                try:
                    print(f"  第{i + 1}个元素，点击...")
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", elem
                    )
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", elem)
                    return True
                except:
                    continue
        except Exception as e:
            print(f"方法2失败: {e}")

        print("❌ 未找到查看全部按钮")
        return False

    def check_display_mode_and_click(self, page_text):
        """检测显示模式并点击查看全部"""
        self.display_mode = self.detect_display_mode(page_text)
        print(f"✅ 检测到显示模式: {self.display_mode}")

        if self.display_mode == "overview":
            print("订单概览模式 - 需要点击'查看全部'")
            if self.click_view_all_orders_overview():
                print("✅ 已点击查看全部")
                return True
        elif self.display_mode == "full_list":
            print("完整列表模式 - 直接开始爬取")
            return True
        else:
            print("⚠️ 未检测到标准订单页面")
            return False

        """通过个人中心入口登录 - 使用登录模块"""
        success = self.login_module.login_via_personal_center(phone, login_type)
        if success:
            # 同步登录状态到主类
            self.is_already_on_orders_page = self.login_module.is_already_on_orders_page
            self.display_mode = self.login_module.display_mode
            print("✅ 登录成功")
        return success
        print("❌ 登录失败")
        return False

    def login_via_personal_center(self, phone, login_type="sms"):
        """通过个人中心入口登录 - 使用登录模块"""
        success = self.login_module.login_via_personal_center(phone, login_type)
        if success:
            # 同步登录状态到主类
            self.is_already_on_orders_page = self.login_module.is_already_on_orders_page
            self.display_mode = self.login_module.display_mode
            print("✅ 登录成功")
        return success

    def login_sms(self, phone):
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
                    print("✅ 登录完成，等待后续分析...")
                    time.sleep(2)
                    return True
        return False

    def login_qr(self):
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
        print("✅ 扫码登录完成，等待后续分析...")
        time.sleep(2)
        return True

    def safe_find(self, xpath, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            return None

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
        """快速检测登录成功"""
        page_text_lower = page_text.lower()
        current_url_lower = current_url.lower()
        if "login" in current_url_lower:
            return False

        # ⭐ 检测显示模式
        self.display_mode = self.detect_display_mode(page_text)

        # 检测用户提供的HTML结构（最快）
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
                print(f"   ✓ 显示模式: {self.display_mode}")
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
            print(f"   ✓ 显示模式: {self.display_mode}")
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

    def navigate_to_orders(self):
        try:
            if self.is_already_on_orders_page:
                print("✅ 已在订单页面，不进行自动跳转...")
                print("📋 当前页面包含订单信息，可以直接分析")
                return True
            print("前往订单页面...")
            self.driver.get("https://mobile.pinduoduo.com/orders")
            self.smart_wait((3, 5))
            if "login" in self.driver.current_url.lower():
                print("需要登录")
                return False
            page_text = self.driver.page_source
            if self.check_display_mode_and_click(page_text):
                return True
            print("✅ 订单页面加载完成")
            return True
        except Exception as e:
            print(f"导航失败: {e}")
            return False

    def search_order_links_on_current_page(self):
        """在当前页面搜索所有订单相关的跳转链接"""
        print("\n在当前页面搜索订单跳转链接...")

        page_source = self.driver.page_source
        current_url = self.driver.current_url
        print(f"当前页面: {current_url}")

        # 查找所有可能的订单相关链接
        import re

        # 简单的链接搜索
        order_link_patterns = [
            r'href="([^"]*order[^"]*)',
            r'href="([^"]*orders[^"]*)',
            r'data-href="([^"]*order[^"]*)',
        ]

        found_links = set()
        print("\n搜索订单相关链接:")
        for pattern in order_link_patterns:
            try:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    if match and len(match) > 3:
                        found_links.add(match)
            except:
                continue

        # 查找可点击的订单相关元素
        clickable_elements = []
        order_keywords = ["订单", "查看全部", "详情", "order", "orders"]

        for keyword in order_keywords:
            try:
                elements = self.driver.find_elements(
                    By.XPATH, f"//*[contains(text(), '{keyword}')]"
                )
                for elem in elements:
                    try:
                        tag_name = elem.tag_name.lower()
                        if tag_name in ["a", "button", "div"]:
                            href = elem.get_attribute("href") or elem.get_attribute(
                                "data-href"
                            )
                            text = elem.text.strip()

                            if text and len(text) > 0:
                                clickable_elements.append(
                                    {
                                        "element": elem,
                                        "text": text,
                                        "tag": tag_name,
                                        "href": href,
                                        "class": elem.get_attribute("class"),
                                    }
                                )
                    except:
                        continue
            except:
                continue

        print(f"\n找到 {len(found_links)} 个订单相关链接:")
        for i, link in enumerate(found_links, 1):
            print(f"  {i}. {link}")

        print(f"\n找到 {len(clickable_elements)} 个可点击的订单元素:")
        for i, elem_info in enumerate(clickable_elements, 1):
            print(f"  {i}. <{elem_info['tag']}> {elem_info['text'][:50]}...")
            if elem_info["href"]:
                print(f"     链接: {elem_info['href'][:100]}...")
            if elem_info["class"]:
                print(f"     类名: {elem_info['class']}")

        # 特别关注"查看全部"按钮
        view_all_elements = []
        for elem_info in clickable_elements:
            if "查看全部" in elem_info["text"]:
                view_all_elements.append(elem_info)

        if view_all_elements:
            print(f"\n找到 {len(view_all_elements)} 个'查看全部'元素:")
            for i, elem_info in enumerate(view_all_elements, 1):
                print(f"  {i}. 类名: {elem_info['class']}, 文本: '{elem_info['text']}'")

        # 保存搜索结果
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        search_result_file = f"order_links_search_{timestamp}.txt"

        try:
            with open(search_result_file, "w", encoding="utf-8") as f:
                f.write(f"订单链接搜索结果\\n")
                f.write(f"时间: {datetime.now()}\\n")
                f.write(f"当前页面: {current_url}\\n\\n")

                f.write(f"\\n=== 找到的订单链接 ({len(found_links)}个) ===\\n")
                for link in found_links:
                    f.write(f"{link}\\n")

                f.write(f"\\n=== 可点击的订单元素 ({len(clickable_elements)}个) ===\\n")
                for i, elem_info in enumerate(clickable_elements, 1):
                    f.write(f"{i}. <{elem_info['tag']}> {elem_info['text']}\\n")
                    if elem_info["href"]:
                        f.write(f"   链接: {elem_info['href']}\\n")
                    if elem_info["class"]:
                        f.write(f"   类名: {elem_info['class']}\\n")
                    f.write("\\n")

            print(f"\\n搜索结果已保存: {search_result_file}")
        except Exception as e:
            print(f"\\n保存文件失败: {e}")

        return found_links, clickable_elements

    def close(self):
        if self.driver:
            self.driver.quit()


def main():
    print("拼多多订单爬取工具 v4.2")
    print("=" * 50)
    print("✨ 新增功能:")
    print("   - Chrome窗口设置为1280x1920")
    print("   - 检测订单显示模式（概览/完整列表）")
    print("   - 智能点击'查看全部'策略")
    print("   - 登录检测进一步优化（仅需4秒）")
    print()

    # 加载配置
    config_file = "pdd_config.json"
    config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        except:
            config = {}

    # 获取手机号
    phone = os.getenv("PDD_PHONE") or config.get("phone")
    if not phone:
        phone = input("请输入手机号: ").strip()
        # 保存手机号到配置
        config["phone"] = phone
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"✅ 手机号已保存到 {config_file}，下次运行将自动使用")
        except Exception as e:
            print(f"⚠️ 保存手机号失败: {e}")

    login_type = os.getenv("PDD_LOGIN_TYPE") or config.get("login_type", "qr")
    if login_type not in ["sms", "qr"]:
        login_type = "qr"

    scraper = PinduoduoOrderScraper()

    try:
        scraper.start_browser()

        success = scraper.login_via_personal_center(phone, login_type)

        if success:
            print("✅ 登录成功！")
            print(f"✅ 显示模式: {scraper.display_mode}")

            # 🔍 在当前页面搜索订单链接（不跳转）
            print("\n" + "=" * 60)
            print("🔍 开始在当前页面搜索订单跳转链接...")
            print("=" * 60 + "\n")

            found_links, clickable_elements = (
                scraper.search_order_links_on_current_page()
            )

            # 自动点击"查看全部"进入完整订单列表
            print("\n🎯 自动点击查看全部进入完整订单列表...")

            try:
                # 查找并点击'查看全部'元素
                view_all_elements = scraper.driver.find_elements(
                    By.CSS_SELECTOR, "div.others"
                )
                clicked = False

                for i, elem in enumerate(view_all_elements):
                    text = elem.text.strip()
                    if "查看全部" in text:
                        print(
                            f"✅ 找到'查看全部'按钮（第{i + 1}个），类名: {elem.get_attribute('class')}"
                        )

                        # 滚动到元素位置
                        scraper.driver.execute_script(
                            "arguments[0].scrollIntoView(true);", elem
                        )
                        time.sleep(1)

                        # 点击元素
                        scraper.driver.execute_script("arguments[0].click();", elem)
                        print("✅ 已点击'查看全部'，等待页面跳转...")
                        clicked = True
                        break

                if not clicked:
                    print("❌ 未找到'查看全部'按钮")

                # 等待页面跳转
                time.sleep(3)

                # 检查页面是否跳转
                new_url = scraper.driver.current_url
                new_page_source = scraper.driver.page_source

                print(f"📍 跳转后URL: {new_url}")

                # 🚨 处理可能的弹窗
                try:
                    # 等待一下看是否有弹窗出现
                    time.sleep(2)

                    # 尝试关闭可能的外部打开文件弹窗
                    # 方法1: 查找关闭按钮
                    close_selectors = [
                        "//*[contains(text(), '取消')]",
                        "//*[contains(text(), '关闭')]",
                        "//*[contains(text(), '稍后')]",
                        "//*[contains(text(), '不再提醒')]",
                        ".close-btn",
                        ".cancel-btn",
                        "[class*='close']",
                    ]

                    for selector in close_selectors:
                        try:
                            if selector.startswith("//"):
                                elements = scraper.driver.find_elements(
                                    By.XPATH, selector
                                )
                            else:
                                elements = scraper.driver.find_elements(
                                    By.CSS_SELECTOR, selector
                                )

                            for elem in elements:
                                if elem.is_displayed():
                                    elem_text = elem.text.strip()
                                    print(
                                        f"  🔧 找到可能的弹窗按钮: '{elem_text}' ({selector})"
                                    )
                                    scraper.driver.execute_script(
                                        "arguments[0].click();", elem
                                    )
                                    time.sleep(1)
                                    print("  ✅ 已点击关闭弹窗")
                                    break
                        except:
                            continue

                except Exception as e:
                    print(f"  ⚠️ 处理弹窗时出错: {e}")

                # 再次等待页面稳定
                time.sleep(3)
                new_page_source = scraper.driver.page_source

                # 分析跳转后的页面
                if 'class="order-menu"' not in new_page_source:
                    print("✅ 页面已跳转，不再显示概览页面")
                    scraper.display_mode = "full_orders_list"

                    # 保存跳转后的页面
                    from datetime import datetime

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    full_orders_file = f"pdd_full_orders_{timestamp}.html"
                    with open(full_orders_file, "w", encoding="utf-8") as f:
                        f.write(new_page_source)
                    print(f"💾 完整订单页面已保存: {full_orders_file}")

                    # 分析完整订单页面
                    print("\n🔍 分析完整订单页面...")

                    # 测试订单选择器
                    test_selectors = [
                        ".order-item",
                        ".goods-item",
                        "[class*='order']",
                        "div[class*='item']",
                    ]

                    best_selector = None
                    max_elements = 0

                    for selector in test_selectors:
                        try:
                            elements = scraper.driver.find_elements(
                                By.CSS_SELECTOR, selector
                            )
                            if elements:
                                print(f"  {selector}: {len(elements)} 个元素")

                                if len(elements) > max_elements:
                                    max_elements = len(elements)
                                    best_selector = selector

                                # 显示前2个元素的预览
                                for j, elem in enumerate(elements[:2]):
                                    try:
                                        text = elem.text.strip()
                                        if len(text) > 20:
                                            preview = text[:80].replace("\n", " | ")
                                            print(f"    [{j + 1}] {preview}...")
                                    except:
                                        continue
                        except:
                            continue

                    if best_selector:
                        print(f"\n🎯 完整订单页面分析完成！")
                        print(
                            f"🏆 推荐的订单选择器: {best_selector} (找到 {max_elements} 个元素)"
                        )
                        print(f"\n💡 可以用这个选择器优化订单提取逻辑")
                    else:
                        print("\n⚠️ 完整订单页面未找到明确的订单选择器")
                else:
                    print("⚠️ 页面可能未完全跳转，仍显示概览页面")

            except Exception as e:
                print(f"❌ 点击'查看全部'失败: {e}")

            # 设置标志，表示已经在订单相关页面
            scraper.is_already_on_orders_page = True

        if scraper.navigate_to_orders():
            max_pages = input("请输入最大页数 (默认10): ").strip()
            max_pages = int(max_pages) if max_pages else 10
            orders = scraper.order_processor.scrape_orders(max_pages=max_pages)
            print(f"\n共获取 {len(orders)} 个订单")
            scraper.save_orders()
            scraper.order_processor.generate_report()

    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
