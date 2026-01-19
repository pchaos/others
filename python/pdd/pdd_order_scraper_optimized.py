"""
拼多多个人订单爬取工具 v4.2
新增功能：
1. Chrome窗口高度设置为1500
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

        # ⭐ Chrome窗口设置为1080x1920 (移动端优化)
        self.driver.set_window_size(1080, 1920)  # 宽度1080, 高度1920
        print("浏览器启动成功 (1080x1920 移动端优化)")

        # 初始化登录模块
        self.login_module = PinduoduoLogin(self.driver, ".pdd_cookies.json")

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
        """精确点击个人中心 - 使用登录模块"""
        return self.login_module.click_personal_center_exact()

    def login_via_personal_center(self, phone, login_type="sms"):
        """通过个人中心入口登录 - 使用登录模块"""
        success = self.login_module.login_via_personal_center(phone, login_type)
        if success:
            # 同步登录状态到主类
            self.is_already_on_orders_page = self.login_module.is_already_on_orders_page
            self.display_mode = self.login_module.display_mode
            print("✅ 登录成功，已在订单页面")
        return success

    def login_sms(self, phone):
        """短信登录 - 使用登录模块"""
        return self.login_module.login_sms(phone)

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

    def scrape_orders(self, max_pages=10):
        all_orders = []
        print("开始爬取订单...")
        self.smart_wait((3, 5))

        for page_num in range(1, max_pages + 1):
            print(f"第 {page_num} 页...")
            self.smart_wait((3, 5))
            orders = self.extract_orders()
            all_orders.extend(orders)
            print(f"第 {page_num} 页: {len(orders)} 个订单")
            if not self.go_to_next_page():
                break
        self.orders = all_orders
        return all_orders

    def extract_orders(self):
        orders = []

        # 🎯 使用推荐的选择器
        # 🎯 使用多个选择器确保获取所有订单
        selectors_to_try = [
            ".U6SAh0Eo",  # 精确匹配
            "[class*='order']",  # 包含order的类
            ".order-item",  # 订单项
            ".order-card",  # 订单卡片
            "[data-test*='order']",  # 包含order的data-test属性
            "div[class*='item'][class*='order']",  # 组合选择器
            ".order-list-item",  # 订单列表项
            "[class*='container'][class*='order']",  # 宽泛选择器
            ".order-entry",  # 订单条目
            ".order-info",  # 订单信息
            "*[class*='order'][class*='item']",  # 任何包含order和item的元素
        ]

        print(f"🎯 将尝试 {len(selectors_to_try)} 个选择器来获取所有订单...")

        # 重试机制
        max_retries = 3
        for retry in range(max_retries):
            try:
                print(f"\n📋 第{retry + 1}次尝试提取订单...")

                # 检查页面是否还正常
                current_url = self.driver.current_url
                print(f"📍 当前页面: {current_url}")

                # 获取页面元素
                # 尝试所有选择器
                all_elements = []
                for selector in selectors_to_try:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        print(f"  选择器 {selector}: 找到 {len(elements)} 个元素")
                        all_elements.extend(elements)
                    except Exception as e:
                        print(f"  选择器 {selector}: 错误 - {e}")

                # 去重（避免重复元素）
                unique_elements = []
                seen_texts = set()
                for elem in all_elements:
                    try:
                        text = elem.text.strip()
                        if text and text not in seen_texts and len(text) > 20:
                            unique_elements.append(elem)
                            seen_texts.add(text)
                    except:
                        continue

                elements = unique_elements
                print(f"🔍 找到 {len(elements)} 个订单元素")

                if len(elements) == 0:
                    print("⚠️ 未找到订单元素，尝试刷新页面...")
                    self.driver.refresh()
                    time.sleep(3)
                    continue

                # 提取每个订单
                valid_orders_count = 0
                for i, elem in enumerate(elements):
                    try:
                        text = elem.text.strip()

                        # 验证订单内容
                        if len(text) > 20 and len(text) < 2000:
                            # 检查是否包含订单特征
                            order_features = [
                                "¥",
                                "x",
                                "待",
                                "已",
                                "订单",
                                "商品",
                                "购买",
                            ]
                            has_features = sum(
                                1 for feature in order_features if feature in text
                            )

                            if has_features >= 2:  # 至少包含2个订单特征
                                print(
                                    f"  📦 订单{i + 1}: {text[:50].replace(chr(10), ' | ')}..."
                                )

                                order = self.parse_order(elem)
                                if order and order.get("goods_name"):
                                    orders.append(order)
                                    valid_orders_count += 1
                                else:
                                    print(f"    ❌ 解析订单失败")
                            else:
                                print(
                                    f"    ⚠️ 订单{i + 1}: 特征不足 ({has_features}/2) - {text[:30]}..."
                                )
                        else:
                            print(f"    ⚠️ 订单{i + 1}: 长度异常 ({len(text)}字符)")

                    except Exception as e:
                        print(f"    ❌ 处理订单{i + 1}时出错: {e}")
                        continue

                print(
                    f"\n✅ 第{retry + 1}次尝试完成，提取到 {valid_orders_count} 个有效订单"
                )

                if valid_orders_count > 0:
                    print(f"🎉 成功提取订单，停止重试")
                    break
                else:
                    print(f"⚠️ 第{retry + 1}次尝试未找到有效订单")

            except Exception as e:
                print(f"❌ 第{retry + 1}次尝试失败: {e}")

                # 如果是连接错误，尝试重新加载
                if "Connection aborted" in str(e) or "RemoteDisconnected" in str(e):
                    print("🔄 检测到连接错误，尝试重新加载页面...")
                    time.sleep(2)
                    try:
                        self.driver.refresh()
                        time.sleep(3)
                    except:
                        print("❌ 页面重新加载失败")

        print(f"\n📊 最终提取到 {len(orders)} 个订单")

        # 显示提取的订单摘要
        if orders:
            print("\n📋 订单摘要:")
            for i, order in enumerate(orders[:5]):  # 只显示前5个
                print(
                    f"  {i + 1}. {order.get('goods_name', '未知商品')} - {order.get('order_status', '未知状态')} - ¥{order.get('goods_price', '0')}"
                )
            if len(orders) > 5:
                print(f"  ... 还有 {len(orders) - 5} 个订单")

        return orders

    def search_order_links_on_current_page(self):
        """在当前页面搜索所有订单相关的跳转链接"""
        print("\n🔍 在当前页面搜索订单跳转链接...")

        page_source = self.driver.page_source
        current_url = self.driver.current_url
        print(f"📍 当前页面: {current_url}")

        # 查找所有可能的订单相关链接
        import re

        # 简单的链接搜索
        order_link_patterns = [
            r'href="([^"]*order[^"]*)"',
            r'href="([^"]*orders[^"]*)"',
            r'data-href="([^"]*order[^"]*)"',
        ]

        found_links = set()
        print("\n🔗 搜索订单相关链接:")
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

        print(f"\n📋 找到 {len(found_links)} 个订单相关链接:")
        for i, link in enumerate(found_links, 1):
            print(f"  {i}. {link}")

        print(f"\n🖱️  找到 {len(clickable_elements)} 个可点击的订单元素:")
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
            print(f"\n🎯 找到 {len(view_all_elements)} 个'查看全部'元素:")
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

            print(f"\n💾 搜索结果已保存: {search_result_file}")
        except Exception as e:
            print(f"\n⚠️ 保存文件失败: {e}")

        return found_links, clickable_elements

    def analyze_page_structure_simple(self):
        """基于你提供的HTML结构进行分析"""
        print("\n🔍 基于真实HTML结构分析页面...")

        page_source = self.driver.page_source

        # 检查是否是概览页面（你提供的结构）
        if '<div class="order-menu">' in page_source:
            print("✅ 检测到概览页面结构")
            print("📋 已识别的元素:")
            print("  - order-menu: 订单菜单容器")
            print("  - my-orders: '我的订单'标题")
            print("  - others: '查看全部'按钮")
            print("  - top-menu-wrapper: 状态菜单")

            # 提取状态数字
            import re

            status_tags = re.findall(
                r'<div class="long-number-tag[^>]*">(\d+)</div>', page_source
            )
            if status_tags:
                print(f"  - 状态数量: {status_tags}")

            print("\n💡 建议点击'查看全部'查看完整订单列表")

            # 保存当前页面
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            overview_file = f"pdd_overview_page_{timestamp}.html"
            with open(overview_file, "w", encoding="utf-8") as f:
                f.write(page_source)
            print(f"💾 概览页面已保存: {overview_file}")

            return "overview"

        # 检查是否是完整订单页面
        order_indicators = ["订单号", "¥", "x", "待", "已"]
        found_orders = sum(
            1 for indicator in order_indicators if indicator in page_source
        )

        if found_orders >= 3:
            print("✅ 检测到完整订单页面")

            # 测试订单选择器
            selectors = [".order-item", ".goods-item", "[class*='order']"]
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"🎯 {selector}: {len(elements)} 个元素")
                        return selector
                except:
                    continue

        return "unknown"

    def parse_order(self, element):
        """基于真实HTML结构解析订单信息"""
        try:
            order = {"scrape_time": datetime.now().isoformat()}

            # 🎯 基于真实HTML结构的精确提取
            try:
                # 1. 店铺名称
                shop_name_elem = element.find_element(
                    By.CSS_SELECTOR, "span[data-test='店铺名称']"
                )
                order["shop_name"] = shop_name_elem.text.strip()
            except:
                pass

            # 2. 订单状态
            try:
                status_elem = element.find_element(
                    By.CSS_SELECTOR, "p[data-test='订单状态']"
                )
                status_text = status_elem.text.strip()
                # 清理状态文本
                order["order_status"] = (
                    status_text.replace(" ", "").replace("	", "").strip()
                )
            except:
                pass

            # 3. 商品名称
            try:
                goods_name_elem = element.find_element(
                    By.CSS_SELECTOR, "span[data-test='商品名称']"
                )
                order["goods_name"] = goods_name_elem.text.strip()
            except:
                pass

            # 4. 商品规格（第二行）
            try:
                goods_spec_elem = element.find_element(By.CSS_SELECTOR, ".bJrhQPD0")
                goods_spec = goods_spec_elem.text.strip()
                if goods_spec:
                    order["goods_spec"] = goods_spec
            except:
                pass

            # 5. 商品价格
            try:
                price_elem = element.find_element(
                    By.CSS_SELECTOR, "span[data-test='商品价格']"
                )
                order["goods_price"] = price_elem.text.strip()
            except:
                pass

            # 6. 购买数量
            try:
                quantity_elem = element.find_element(By.CSS_SELECTOR, ".r6qvgq4W")
                quantity_text = quantity_elem.text.strip()
                # 提取数字，如 "×1" -> "1"
                import re

                qty_match = re.search(r"(\d+)", quantity_text)
                if qty_match:
                    order["quantity"] = int(qty_match.group(1))
            except:
                pass

            # 7. 实付金额
            try:
                actual_pay_elem = element.find_element(By.CSS_SELECTOR, ".pdcOje4N")
                actual_pay_text = actual_pay_elem.text.strip()
                # 提取价格，如 "￥13.89" -> "13.89"
                import re

                pay_match = re.search(r"[\¥￥]?\s*(\d+\.?\d*)", actual_pay_text)
                if pay_match:
                    order["actual_pay"] = pay_match.group(1)
            except:
                pass

            # 8. 物流信息
            try:
                logistics_elem = element.find_element(By.CSS_SELECTOR, ".f2_mZxnQ p")
                logistics_text = logistics_elem.text.strip()
                if logistics_text and len(logistics_text) > 10:
                    order["logistics_info"] = logistics_text
            except:
                pass

            # 9. 操作按钮信息
            try:
                action_buttons = element.find_elements(By.CSS_SELECTOR, ".KBkhFO8F a")
                actions = []
                for btn in action_buttons:
                    btn_text = btn.text.strip()
                    if btn_text:
                        actions.append(btn_text)
                if actions:
                    order["available_actions"] = actions
            except:
                pass

            # 10. 订单号（后备提取）
            if not order.get("order_sn"):
                text = element.text
                sn_match = re.search(r"(\d{10,20})", text)
                if sn_match:
                    order["order_sn"] = sn_match.group(1)

            # 11. 后备方案：如果某些字段缺失，使用text方法作为后备
            if not order.get("goods_name"):
                text = element.text
                lines = text.split("\n")
                for line in lines:
                    line = line.strip()
                    if (
                        5 < len(line) < 100
                        and "¥" not in line
                        and "实付" not in line
                        and "店铺" not in line
                        and "状态" not in line
                    ):
                        if not order.get("goods_name"):
                            order["goods_name"] = line
                            break

            return order

        except Exception as e:
            print(f"解析订单时出错: {e}")
            return None

    def go_to_next_page(self):
        try:
            # 🔄 优先使用PageDown键翻页（根据用户反馈更有效）
            print("🔄 尝试使用PageDown键翻页...")
            try:
                # 多次按PageDown确保翻页
                from selenium.webdriver.common.keys import Keys

                for i in range(3):
                    self.driver.find_element(By.TAG_NAME, "body").send_keys(
                        Keys.PAGE_DOWN
                    )
                    time.sleep(1)
                print("✅ 已执行PageDown翻页")
                time.sleep(2)  # 等待新订单加载
                return True
            except Exception as e:
                print(f"❌ PageDown翻页失败: {e}，尝试按钮点击...")

            # 备用方案：尝试点击翻页按钮
            next_selectors = [
                "//*[contains(text(), '下一页')]",
                "//*[contains(text(), '加载更多')]",
                ".next-page",
                ".load-more",
            ]
            print(f"🔍 尝试翻页按钮，共{len(next_selectors)}个选择器...")
            for selector in next_selectors:
                try:
                    btn = (
                        self.driver.find_element(By.XPATH, selector)
                        if "//" in selector
                        else self.driver.find_element(By.CSS_SELECTOR, selector)
                    )
                    if btn.is_displayed() and btn.is_enabled():
                        self.driver.execute_script("arguments[0].click();", btn)
                        print(f"✅ 找到翻页按钮: {selector}")
                        return True
                except:
                    continue
            print(f"❌ 未找到可用的翻页按钮")
            return False
        except:
            return False

    def generate_report(self):
        # 🎯过滤有效订单（排除已取消/退款的）

        valid_orders = []

        excluded_orders = []

        for order in self.orders:
            status = order.get("order_status", "")

            # 排除已取消/退款的订单

            if any(
                exclude in status
                for exclude in ["交易已取消", "已退款", "退款中", "退款处理中"]
            ):
                excluded_orders.append(order)

                continue

            # 排除只有取消按钮的订单

            actions = order.get("available_actions", [])

            if (
                actions
                and len(actions) <= 2
                and all(action in ["再次拼单", "删除订单"] for action in actions)
            ):
                excluded_orders.append(order)

                continue

            valid_orders.append(order)

        # 更新self.orders为只包含有效订单

        self.orders = valid_orders

        if not self.orders:
            print("暂无订单数据")
            return

        # 过滤有效订单（排除已取消/退款的）
        valid_orders = []
        excluded_orders = []

        for order in self.orders:
            status = order.get("order_status", "")

            if any(
                exclude in status
                for exclude in ["交易已取消", "已退款", "退款中", "退款处理中"]
            ):
                excluded_orders.append(order)
                continue

            valid_orders.append(order)

        total = len(valid_orders)
        if total == 0:
            print("暂无有效订单数据")
            return

        spent = sum(float(o.get("goods_price", 0)) for o in valid_orders)
        received = len(
            [
                o
                for o in valid_orders
                if "已签收" in o.get("order_status", "")
                or "已确认收货" in o.get("order_status", "")
            ]
        )

        print(f"\n{'=' * 50}")
        print("📊 有效订单分析报告")
        print(f"📋 订单过滤: 已排除取消/退款订单")
        print(f"{'=' * 50}")
        print(f"总有效订单数: {total}")
        print(f"总消费额: ¥{spent:.2f}")

        if total > 0:
            print(f"平均客单价: ¥{spent / total:.2f}")
            print(f"已收货: {received} ({received / total * 100:.1f}%)")
            print(
                f"待收货: {total - received} ({(total - received) / total * 100:.1f}%)"
            )

        # 统计无效订单
        excluded_count = len(self.orders) - total
        if excluded_count > 0:
            print(f"\n📈 无效订单统计:")
            print(f"已排除订单数: {excluded_count}")

        excluded_statuses = {}  # 初始化变量避免作用域错误
        for order in self.orders:
            status = order.get("order_status", "")
            if any(
                exclude in status
                for exclude in ["交易已取消", "已退款", "退款中", "退款处理中"]
            ):
                if status not in excluded_statuses:
                    excluded_statuses[status] = 0
                excluded_statuses[status] += 1

        print("排除原因统计:")
        for status, count in excluded_statuses.items():
            print(f"  {status}: {count} 个订单")

            exclusion_rate = excluded_count / (total + excluded_count) * 100
            print(f"排除比例: {exclusion_rate:.1f}%")

        report_file = (
            f"valid_order_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"拼多多有效订单分析报告\n")
            f.write(f"生成时间: {datetime.now()}\n\n")
            f.write(f"订单过滤: 已排除取消/退款订单\n\n")
            f.write(f"总有效订单数: {total}\n")
            f.write(f"总消费额: ¥{spent:.2f}\n")
            if total > 0:
                f.write(f"平均客单价: ¥{spent / total:.2f}\n")
                f.write(f"已收货: {received} ({received / total * 100:.1f}%)\n")
                f.write(
                    f"待收货: {total - received} ({(total - received) / total * 100:.1f}%)\n"
                )

            f.write(f"无效订单数: {excluded_count}\n")
            for status, count in excluded_statuses.items():
                f.write(f"{status}: {count} 个订单\n")

        print(f"📄 有效订单报告已保存: {report_file}")
        return report_file

    def close(self):
        if self.driver:
            self.driver.quit()


def main():
    print("拼多多订单爬取工具 v4.2")
    print("=" * 50)
    print("✨ 新增功能:")
    print("   - Chrome窗口高度设置为1500px")
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
    
    # 获取登录类型偏好
    login_type = input("请选择登录方式 (1=短信, 2=扫码, 默认2): ").strip()
    login_type = "sms" if login_type == "1" else "qr"

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

            # 询问用户是否继续
            print("\n" + "=" * 60)
            # 自动点击"查看全部"
            print("\n🎯 自动开始点击'查看全部'...")
            # 自动设置user_input为"click"，无需等待用户输入
            user_input = "click"

            if user_input.lower() == "click":
                print("\n🎯 开始点击'查看全部'...")

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
                    time.sleep(1)

                    # 检查页面是否跳转
                    new_url = scraper.driver.current_url
                    new_page_source = scraper.driver.page_source

                    print(f"📍 跳转后URL: {new_url}")

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
            orders = scraper.scrape_orders(max_pages=max_pages)
            print(f"\n共获取 {len(orders)} 个订单")
            scraper.generate_report()

    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
