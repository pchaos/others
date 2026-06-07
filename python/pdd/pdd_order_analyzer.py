"""
拼多多订单分析脚本 — 按店铺/品类汇总
用法: python3 pdd_order_analyzer.py [-f <json文件>]
"""

import json
import os
import re
import glob
from datetime import datetime
from collections import defaultdict


def find_latest_json(pattern):
    files = sorted(glob.glob(pattern))
    return files[-1] if files else None


def extract_shop(element_text):
    """店铺名: element_text 第一行"""
    if not element_text:
        return "未知店铺"
    return element_text.split("\n")[0].strip() or "未知店铺"


def classify_category(goods_name, shop_name):
    """关键词分类"""
    name = (goods_name or "") + " " + (shop_name or "")

    checks = [
        ("洗护", ["香皂", "洗发水", "花露水", "沐浴", "牙膏", "牙刷",
                  "洗面", "护肤", "霜", "乳", "皂"]),
        ("药品/保健品", ["药", "胶囊", "片 ", "片/", "丸", "颗粒", "消渴",
                         "OTC", "处方药", "维生素", "钙", "益生菌", "阿胶",
                         "人参", "枸杞", "滴耳油", "十全大补", "归脾"]),
        ("日用品", ["袜子", "短袖", "上衣", "T恤", "帐篷", "龙头", "阀芯",
                    "灯", "雨衣", "绷带", "弹性", "配件", "维修", "五金",
                    "水龙头", "密封", "阀门", "开关"]),
        ("食品/生鲜", ["面粉", "大米", "米 ", "米/", "水果", "蜜瓜", "甜瓜",
                       "蔬菜", "牛奶", "鲜奶", "肉 ", "鱼 ", "虾", "蛋 ",
                       "挂面", "拉面", "拉条子", "新鲜","产地直发",
                       "生鲜", "紫甘蓝", "黄须菜", "薄荷", "吊干杏",
                       "莴笋", "姜 ", "大泥鳅", "鲟龙鱼", "莲子芯", "莲心"]),
    ]

    for cat, keywords in checks:
        if any(kw in name for kw in keywords):
            return cat
    return "其他"


def fmt_price(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def make_separator(widths):
    parts = []
    for w in widths:
        parts.append("─" * (w + 2))
    return "├" + "┼".join(parts) + "┤"


def make_header(widths, texts):
    parts = []
    for w, t in zip(widths, texts):
        parts.append(" " + t.ljust(w))
    return "│" + "│".join(parts) + "│"


def make_row(widths, texts):
    parts = []
    for w, t in zip(widths, texts):
        s = str(t)
        if len(s) > w:
            s = s[:w - 1] + "…"
        parts.append(" " + s.ljust(w))
    return "│" + "│".join(parts) + "│"


def build_table(headers, rows, widths=None):
    if widths is None:
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(str(cell)))
        widths = [min(w + 1, 40) for w in widths]

    top = "┌" + "┬".join("─" * (w + 2) for w in widths) + "┐"
    sep = make_separator(widths)
    bot = "└" + "┴".join("─" * (w + 2) for w in widths) + "┘"

    lines = [top, make_header(widths, headers), sep]
    for row in rows:
        lines.append(make_row(widths, row))
    lines.append(bot)
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="PDD订单分析工具")
    parser.add_argument("-f", "--file", help="指定valid_orders JSON文件")
    args = parser.parse_args()

    # 检测文件
    if args.file:
        valid_file = args.file
        excluded_file = args.file.replace("valid_orders", "excluded_orders")
        if excluded_file == args.file:
            excluded_file = None
    else:
        valid_file = find_latest_json("pdd_valid_orders_*.json")
        excluded_file = find_latest_json("pdd_excluded_orders_*.json")

    if not valid_file:
        print("❌ 未找到 pdd_valid_orders_*.json 文件")
        return

    # 读取数据
    valid_orders = json.load(open(valid_file, encoding="utf-8"))
    excluded_orders = json.load(open(excluded_file, encoding="utf-8")) if excluded_file and os.path.exists(excluded_file) else []
    all_orders = valid_orders + excluded_orders

    # 解析每条订单
    def parse_order(o, source="valid"):
        shop = extract_shop(o.get("element_text", ""))
        goods = o.get("goods_name", "未知商品")
        price = fmt_price(o.get("goods_price", 0))
        status = o.get("order_status", "未知")
        cat = classify_category(goods, shop)
        return {"shop": shop, "goods": goods, "price": price,
                "status": status, "category": cat, "source": source}

    parsed = [parse_order(o, "valid") for o in valid_orders]
    parsed_excluded = [parse_order(o, "excluded") for o in excluded_orders]
    parsed_all = parsed + parsed_excluded

    # === 计算 ===
    # 按店铺（有效）
    shop_valid = defaultdict(lambda: {"count": 0, "total": 0.0})
    for o in parsed:
        shop_valid[o["shop"]]["count"] += 1
        shop_valid[o["shop"]]["total"] += o["price"]

    # 按店铺（全部）
    shop_all = defaultdict(lambda: {"count": 0, "total": 0.0, "cancelled": 0})
    for o in parsed_all:
        shop_all[o["shop"]]["count"] += 1
        shop_all[o["shop"]]["total"] += o["price"]
        if o["source"] == "excluded":
            shop_all[o["shop"]]["cancelled"] += 1

    # 按品类（有效）
    cat_valid = defaultdict(lambda: {"count": 0, "total": 0.0})
    for o in parsed:
        cat_valid[o["category"]]["count"] += 1
        cat_valid[o["category"]]["total"] += o["price"]

    # 取消订单店铺分布
    cancel_by_shop = defaultdict(lambda: {"count": 0, "total": 0.0})
    for o in parsed_excluded:
        cancel_by_shop[o["shop"]]["count"] += 1
        cancel_by_shop[o["shop"]]["total"] += o["price"]

    total_valid_spent = sum(float(o["price"]) for o in parsed)
    total_all_spent = sum(float(o["price"]) for o in parsed_all)
    total_cancel_spent = sum(float(o["price"]) for o in parsed_excluded)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    lines = []

    def pln(s=""):
        lines.append(s)
        print(s)

    pln("=" * 55)
    pln("📊 拼多多订单分析报告 — 按店铺/品类汇总")
    pln("=" * 55)

    pln(f"\n📈 整体概览")
    pln(f"  总订单数: {len(parsed_all)} 个 "
        f"(有效 {len(parsed)} + 已取消/退款 {len(parsed_excluded)})")
    pln(f"  有效消费: ¥{total_valid_spent:.2f}")
    pln(f"  总消费(含取消): ¥{total_all_spent:.2f}")
    if parsed:
        pln(f"  平均客单价: ¥{total_valid_spent / len(parsed):.2f}")

    # 按店铺（有效）
    pln(f"\n📦 按店铺汇总 (有效订单)")
    rows = sorted(shop_valid.items(), key=lambda x: -x[1]["total"])
    table_rows = []
    for shop, data in rows:
        avg = data["total"] / data["count"] if data["count"] else 0
        table_rows.append((shop[:20], str(data["count"]),
                           f"¥{data['total']:.2f}", f"¥{avg:.2f}"))
    pln(build_table(["店铺", "订单数", "消费额", "均价"],
                    table_rows, [22, 7, 12, 10]))

    # 按店铺（全部）
    pln(f"\n📦 按店铺汇总 (含已取消)")
    rows_all = sorted(shop_all.items(), key=lambda x: -x[1]["total"])
    table_rows_all = []
    for shop, data in rows_all:
        table_rows_all.append((shop[:18], str(data["count"]),
                               str(data["cancelled"]),
                               f"¥{data['total']:.2f}"))
    pln(build_table(["店铺", "总订单", "已取消", "总金额"],
                    table_rows_all, [20, 7, 7, 12]))

    # 按品类（有效）
    pln(f"\n🏷️ 按品类汇总 (有效订单)")
    cat_total = sum(d["total"] for d in cat_valid.values()) or 1
    rows_cat = sorted(cat_valid.items(), key=lambda x: -x[1]["total"])
    table_cat = []
    for cat, data in rows_cat:
        pct = data["total"] / cat_total * 100
        table_cat.append((cat, str(data["count"]),
                          f"¥{data['total']:.2f}", f"{pct:.1f}%"))
    pln(build_table(["品类", "订单数", "消费额", "占比"],
                    table_cat, [14, 7, 12, 7]))

    # 取消订单Top店铺
    if cancel_by_shop:
        pln(f"\n❌ 已取消订单 — 店铺分布 (Top 10)")
        rows_cancel = sorted(cancel_by_shop.items(),
                             key=lambda x: -x[1]["count"])[:10]
        table_cancel = []
        for shop, data in rows_cancel:
            table_cancel.append((shop[:20], str(data["count"]),
                                 f"¥{data['total']:.2f}"))
        pln(build_table(["店铺", "取消数", "取消金额"],
                        table_cancel, [22, 7, 12]))

    # 全量订单清单
    pln(f"\n📋 全量订单清单 ({len(parsed_all)} 条)")
    sep_line = "─" * 75
    pln(sep_line)
    pln(f"{'#':>3} | {'店铺':<16} | {'商品名':<28} | {'金额':>6} | {'状态':<8} | {'品类':<8}")
    pln(sep_line)
    for i, o in enumerate(parsed_all, 1):
        shop = o["shop"][:16]
        goods = o["goods"][:28]
        price = f"¥{o['price']:.2f}"
        status = o["status"][:8]
        cat = o["category"][:8]
        pln(f"{i:>3} | {shop:<16} | {goods:<28} | {price:>6} | {status:<8} | {cat:<8}")
    pln(sep_line)

    # 保存
    report_file = f"pdd_analysis_report_{ts}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n📄 分析报告已保存: {report_file}")


if __name__ == "__main__":
    main()
