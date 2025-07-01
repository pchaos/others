# -*- coding=utf-8 -*-
# Modified: 2025-07-01 17:13:48
try:
    import pywencai
except Exception as e:
    print(e.args)
    print("pywencai not found. Please install it:\n pip install pywencai")

# (node:795752) [DEP0040] DeprecationWarning: The `punycode` module is deprecated. Please use a userland alternative instead.


def select_stocks():
    """选股主函数，返回符合以下条件的股票：
    1. 最近5日有过涨停
    2. 最近5日没有跌停
    3. 今日成交量 > 5日平均成交量
    4. 今日集合竞价涨幅在2%-3%之间
    5. 排除北交所、科创板、创业板、ST股票
    返回:
        list: 符合条件的股票代码列表（如['000001.SZ']），如果没有符合条件的股票则返回空列表
    """
    try:
        # 构造查询语句
        query = (
            "最近5日有过涨停，"
            "最近5日没有跌停，"
            "今日成交量＞5日平均成交量，"
            "2＜今日集合竞价涨幅＜3，"
            "非北交所非科创板非创业板非ST"
        )
        # 调用 pywencai 获取数据
        df = pywencai.get(query=query, sort_key='成交金额', sort_order='desc')
        if df is None or df.empty:
            print("[Stock Selector] 未找到符合条件的股票。")
            return []
        # 返回股票代码列表
        if '股票代码' in df.columns:
            return df['股票代码'].tolist()
        elif '代码' in df.columns:
            return df['代码'].tolist()
        else:
            print("[Stock Selector] 错误：数据框中找不到股票代码列。")
            return []
    except Exception as e:
        print(f"[Stock Selector] 查询时发生错误:{e}")
        return []


if __name__ == "__main__":
    selected_stocks = select_stocks()
    print("符合条件的股票：", selected_stocks)
