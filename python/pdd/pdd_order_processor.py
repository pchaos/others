"""
Pinduoduo Order Processor - Extracted order processing logic.
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
from selenium.webdriver.common.keys import Keys


class PddOrderProcessor:
    """Handles order processing logic extracted from main scraper."""

    def __init__(self, driver):
        """Initialize processor with selenium driver."""
        self.driver = driver
        self.orders = []
        self.display_mode = "unknown"

    def smart_wait(self, seconds_range=(2, 4)):
        """Wait for random interval to avoid detection."""
        time.sleep(random.uniform(*seconds_range))

    def safe_find(self, xpath, timeout=15):
        """Safely find element with timeout."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            return None

    def extract_orders(self):
        orders = []

        # 🎯 使用推荐的选择器
        recommended_selector = ".U6SAh0Eo"  # 基于真实HTML结构的精确匹配

        print(f"🎯 使用推荐选择器: {recommended_selector}")

        # 重试机制
        max_retries = 3
        for retry in range(max_retries):
            try:
                print(f"\n📋 第{retry + 1}次尝试提取订单...")

                # 检查页面是否还正常
                current_url = self.driver.current_url
                print(f"📍 当前页面: {current_url}")

                # 获取页面元素
                elements = self.driver.find_elements(
                    By.CSS_SELECTOR, recommended_selector
                )
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
                                "交易成功",
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

    def parse_order(self, element):
        """Parse order information from DOM element"""
        try:
            text = element.text.strip()

            # 提取订单状态
            order_status = "未知状态"
            status_keywords = [
                "已签收",
                "已确认收货",
                "待收货",
                "待发货",
                "待付款",
                "交易已取消",
                "已取消",
                "交易成功",
                "已完成",
                "退款中",
                "退款处理中",
            ]
            for keyword in status_keywords:
                if keyword in text:
                    order_status = keyword
                    break

            # 提取价格 - 优先使用"实付"价格，其次使用"应付"价格，最后使用"￥"后面的价格
            goods_price = "0.00"

            # 方法1: 提取"实付:￥XX.XX"格式
            import re

            match = re.search(r"实付[:：]?￥?([\d.]+)", text)
            if match:
                goods_price = match.group(1)

            # 方法2: 如果没有实付，提取"应付:￥XX.XX"格式
            if goods_price == "0.00":
                match = re.search(r"应付[:：]?￥?([\d.]+)", text)
                if match:
                    goods_price = match.group(1)

            # 方法3: 提取"￥XX.XX"格式（商品价格）
            if goods_price == "0.00":
                match = re.search(r"￥([\d.]+)", text)
                if match:
                    goods_price = match.group(1)

            # 提取商品名称 - 跳过第一行(店铺名)，跳过状态行，找商品行
            lines = text.split("\n")
            store_keywords = [
                "旗舰店",
                "专卖店",
                "专营店",
                "官方",
                "小店",
                "旗舰店",
                "企业店",
            ]
            status_keywords_for_skip = [
                "待收货",
                "待发货",
                "待付款",
                "已签收",
                "已确认收货",
                "交易成功",
                "已完成",
                "确认收货",
                "评价",
            ]
            goods_name = "未知商品"

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # 跳过店铺名
                if any(sk in line for sk in store_keywords) and len(line) < 20:
                    continue
                # 跳过状态行
                if line in status_keywords_for_skip:
                    continue
                # 如果是价格行(￥开头)或数量行(×开头)，跳过
                if (
                    line.startswith("￥")
                    or line.startswith("×")
                    or line.startswith("x")
                ):
                    continue
                # 跳过保障、运费等说明行
                if any(
                    kw in line
                    for kw in ["运费", "退货", "保障", "包赔", "送货", "无理由", "免费"]
                ):
                    continue
                # 找到商品名称 (通常是较长的一行)
                if len(line) >= 5:
                    goods_name = line[:50]
                    break

            return {
                "goods_name": goods_name,
                "order_status": order_status,
                "goods_price": goods_price,
                "element_text": text,
            }
        except Exception as e:
            print(f"解析订单时出错: {e}")
            return None

    def scrape_orders(self, max_pages=10):
        """Scrape orders with page limit"""
        self.orders = []

        page = 0
        while page < max_pages:
            print(f"\n📄 正在爬取第 {page + 1} 页...")
            orders = self.extract_orders()

            if not orders:
                print("没有更多订单，停止爬取")
                break

            self.orders.extend(orders)
            page += 1

            # Try to go to next page
            if not self.go_to_next_page():
                print("没有下一页，停止爬取")
                break

            self.smart_wait()

        return self.orders

    def go_to_next_page(self):
        try:
            next_selectors = [
                "//*[contains(text(), '下一页')]",
                "//*[contains(text(), '加载更多')]",
                ".next-page",
                ".load-more",
            ]
            for selector in next_selectors:
                try:
                    btn = (
                        self.driver.find_element(By.XPATH, selector)
                        if "//" in selector
                        else self.driver.find_element(By.CSS_SELECTOR, selector)
                    )
                    if btn.is_displayed() and btn.is_enabled():
                        self.driver.execute_script("arguments[0].click();", btn)
                        return True
                except:
                    continue
            return False
        except:
            return False

    def save_orders(self):
        """Save orders to JSON file"""
        if not self.orders:
            print("没有订单数据可保存")
            return

        filename = f"pdd_valid_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # 🎯 过滤订单：只导出有效订单
        valid_orders = []
        excluded_orders = []

        for order in self.orders:
            status = order.get("order_status", "")

            # 排除已取消/退款的订单
            if any(
                exclude in status
                for exclude in ["交易已取消", "已退款", "退款处理中", "退款中"]
            ):
                excluded_orders.append(order)
                continue

            # 排除只有取消按钮的订单
            actions = order.get("available_actions", [])
            if len(actions) <= 2 and any(
                "取消" in action or "删除" in action for action in actions
            ):
                excluded_orders.append(order)
                continue

            valid_orders.extend(
                order for order in self.orders if (order not in excluded_orders)
            )

        # 过滤完成
        print(f"\n📊 订单过滤统计:")
        print(f"  ✅ 有效订单: {len(valid_orders)}")
        print(f"  ❌ 已排除订单: {len(excluded_orders)}")

        # 只保存有效订单
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(valid_orders, f, ensure_ascii=False, indent=2)

        # 可选：保存无效订单到单独文件
        if excluded_orders:
            invalid_filename = (
                f"pdd_excluded_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(invalid_filename, "w", encoding="utf-8") as f:
                json.dump(excluded_orders, f, ensure_ascii=False, indent=2)

            print(f"  ❌ 已排除订单已保存: {invalid_filename}")

        print(f"✅ 有效订单已保存: {filename}")
        return filename

    def generate_report(self):
        # 🎯过滤有效订单（排除已取消/退款的）
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

        # 优先使用 display_amount (JavaScript提取)，fallback到 goods_price (DOM提取)
        def get_price(order):
            return float(order.get("display_amount", 0)) or float(
                order.get("goods_price", 0)
            )

        spent = sum(get_price(o) for o in valid_orders)
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

            excluded_statuses = {}
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

            ratio = (
                excluded_count / (total + excluded_count) * 100
                if (total + excluded_count) > 0
                else 0
            )
            print(f"排除比例: {ratio:.1f}%")

        # 保存有效订单到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"pdd_valid_orders_{timestamp}.txt"

        try:
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(f"{'=' * 50}\n")
                f.write("📊 有效订单分析报告\n")
                f.write(f"📋 订单过滤: 已排除取消/退款订单\n")
                f.write(f"{'=' * 50}\n")
                f.write(f"总有效订单数: {total}\n")
                f.write(f"总消费额: ¥{spent:.2f}\n")
                if total > 0:
                    f.write(f"平均客单价: ¥{spent / total:.2f}\n")
                    f.write(f"已收货: {received} ({received / total * 100:.1f}%)\n")
                    f.write(
                        f"待收货: {total - received} ({(total - received) / total * 100:.1f}%)\n"
                    )

                # 写入无效订单统计
                if excluded_count > 0:
                    f.write(f"\n无效订单数: {excluded_count}\n")
                    for status, count in excluded_statuses.items():
                        f.write(f"{status}: {count} 个订单\n")

            print(f"📄 有效订单报告已保存: {report_file}")
        except Exception as e:
            print(f"保存报告失败: {e}")

        return report_file
