# -*- coding=utf-8 -*-
"""
last Modified: 2025-04-26 17:34:03
https://mp.weixin.qq.com/s/UXaSZ5UnG0R9JDZhOxuF8g

"""
# 完整导入清单
import math  # 数学运算
import os
import tempfile
from statistics import mean  # 平均值计算

import akshare as ak  # 财经数据接口
import numpy as np  # 数值计算基础
import pandas as pd  # 数据处理核心
import xlsxwriter  # Excel报告生成
from hikyuu.interactive import *
from scipy import stats  # 统计计算


def get_temp_dir(ensure_exists=True):
    """获取系统临时目录，可选确保目录存在"""
    temp_path = tempfile.gettempdir()
    if ensure_exists:
        os.makedirs(temp_path, exist_ok=True)
    return temp_path


# 获取A股所有股票列表
try:
    stock_list = ak.stock_info_a_code_name()
    print(f"共获取到{len(stock_list)}只A股股票")

# 示例输出：共获取到4231只A股股票
except Exception as e:
    print(f"获取股票列表失败: {str(e)}")
    # 在实际应用中应添加重试逻辑或使用备用数据源


def get_stock_data(stock_code):
    """
    获取单只股票历史数据
    参数:
        stock_code: 股票代码(带市场前缀，如sh600000)
    返回:
        DataFrame: 包含日期、开盘价、收盘价等数据
        None: 获取失败时返回
    """
    try:
        # 获取近一年的日线数据
        # adjust参数设置为'hfq'获取后复权价格，更准确反映真实收益
        kdata = sm.get_stock(stock_code).get_kdata(Query(-900, recover_type=Query.BACKWARD))
        df = kdata.to_df()
        df.columns = ['开盘', '最高', '最低', '收盘', '成交额', '成交量']
        # df = ak.stock_zh_a_hist(
        #     symbol=stock_code, period="daily", start_date="20240701", end_date="20250331", adjust="hfq"
        # )
        return df
    except Exception as e:
        print(f"获取{stock_code}数据失败: {str(e)}")
    return None


def calculate_momentum(code, name, df):
    """
    计算各时间段的动量指标
    参数:
        df: 包含历史价格数据的DataFrame
    返回:
        dict: 包含各动量指标的计算结果
    """
    if df is None or len(df) < 2:
        return None
    latest_price = df['收盘'].iloc[-1]

    # for col in df.columns:
    #     print(f"{col}")
    # 计算不同时间段的收益率
    returns = {'code': code, 'name': name, 'price': latest_price}

    # 1个月收益率(20个交易日)
    if len(df) >= 20:
        returns['month1_return'] = (latest_price - df['收盘'].iloc[-20]) / df['收盘'].iloc[-20]

    # 3个月收益率(60个交易日)
    if len(df) >= 60:
        returns['month3_return'] = (latest_price - df['收盘'].iloc[-60]) / df['收盘'].iloc[-60]

    # 6个月收益率(120个交易日)
    if len(df) >= 120:
        returns['month6_return'] = (latest_price - df['收盘'].iloc[-120]) / df['收盘'].iloc[-120]

    # 1年收益率
    returns['year1_return'] = (latest_price - df['收盘'].iloc[0]) / df['收盘'].iloc[0]

    return returns


def portfolio_input(default_portfolio_size=0):
    """
    获取用户输入的投资金额并进行验证
    """
    global portfolio_size
    if default_portfolio_size > 0:
        protfolio_size = default_portfolio_size
        return float(default_portfolio_size)
    while True:
        portfolio_size = input("请输入您的投资组合金额(元): ")
        try:
            val = float(portfolio_size)
            if val <= 0:
                print("金额必须大于0")
                continue
            return val
        except ValueError:
            print("请输入有效数字!")


def get_temp_dir(ensure_exists=True):
    """获取系统临时目录，可选确保目录存在"""
    temp_path = os.path.join(tempfile.gettempdir(), "hikyuu_tmp")
    if ensure_exists:
        os.makedirs(temp_path, exist_ok=True)
    return temp_path


def main():
    # 初始化数据收集器
    momentum_data = []

    # 示例只处理前100只(实际应用应处理全市场)
    for i, row in stock_list.head(800).iterrows():
        # 根据股票代码首字符添加市场前缀
        market_prefix = {'6': 'sh', '0': 'sz', '3': 'sz', '8': 'bj, 9:' 'bj'}
        prefix = market_prefix.get(str(row['code'])[0], '')  # 首字符匹配映射表
        stock_code = f"{prefix}{row['code']}"
        print(f"正在处理 {i+1}/{len(stock_list)}: {stock_code}{row['name']}")

        # 获取数据并计算动量
        df = get_stock_data(stock_code)
        stock_momentum = calculate_momentum(stock_code, row['name'], df)

        # 有效数据才保存
        if stock_momentum and all(k in stock_momentum for k in ['month1_return', 'year1_return']):
            momentum_data.append(stock_momentum)

    # 转换为DataFrame
    momentum_df = pd.DataFrame(momentum_data)

    # 添加其他有用信息
    momentum_df['market'] = momentum_df['code'].apply(lambda x: '沪' if x.startswith('sh') else '深')

    # 定义分析的时间段
    time_periods = ['year1', 'month6', 'month3', 'month1']

    for period in time_periods:
        col_name = f'{period}_return'
        percentile_col = f'{period}_percentile'

        # 过滤有效数据
        valid_returns = momentum_df[col_name].dropna()

        # 计算百分位数(0-1范围)
        momentum_df[percentile_col] = momentum_df[col_name].apply(
            lambda x: stats.percentileofscore(valid_returns, x) / 100 if pd.notnull(x) else None
        )

    # 计算综合HQM得分(高质量动量)
    momentum_df['hqm_score'] = momentum_df[[f'{period}_percentile' for period in time_periods]].mean(axis=1)

    # 清理数据 - 删除含有缺失值的行
    momentum_df = momentum_df.dropna(subset=['hqm_score'])

    # 添加排名信息
    momentum_df['rank'] = momentum_df['hqm_score'].rank(ascending=False)

    # 选择前50名动量股
    top_count = 50
    top_momentum = momentum_df.sort_values('hqm_score', ascending=False).head(top_count)

    # 重置索引(保持整洁)
    top_momentum.reset_index(drop=True, inplace=True)

    # 添加选择理由
    top_momentum['selection_reason'] = "高质量动量股票"

    # 示例输出
    print(
        f"筛选出{len(top_momentum)}只动量股票，HQM得分范围: {top_momentum['hqm_score'].min():.2f}-{top_momentum['hqm_score'].max():.2f}"
    )

    # 获取投资金额
    print("=== 投资组合配置 ===")
    # portfolio_size = portfolio_input()
    portfolio_size = portfolio_input(default_portfolio_size=600000)

    # 计算每只股票分配金额
    position_size = float(portfolio_size) / len(top_momentum)
    print(f"每只股票分配金额: ¥{position_size:,.2f}")

    # 计算购买股数(考虑A股100股整数倍)
    top_momentum['shares_to_buy'] = (position_size / top_momentum['price']).apply(
        lambda x: math.floor(x / 100) * 100 if not pd.isna(x) else 0  # A股最小100股
    )

    # 计算实际投资金额
    top_momentum['actual_investment'] = top_momentum['shares_to_buy'] * top_momentum['price']

    # 显示汇总信息
    total_investment = top_momentum['actual_investment'].sum()
    cash_remaining = float(portfolio_size) - total_investment
    print(f"\n实际总投资: ¥{total_investment:,.2f}")
    print(f"剩余现金: ¥{cash_remaining:,.2f} ({cash_remaining/float(portfolio_size):.1%})")

    # 创建Excel写入器
    report_file = os.path.join(get_temp_dir(), 'A股动量策略投资组合.xlsx')
    writer = pd.ExcelWriter(report_file, engine='xlsxwriter')

    # 写入数据
    top_momentum.to_excel(writer, sheet_name='动量组合', index=False)

    # 获取工作簿和工作表对象
    workbook = writer.book
    worksheet = writer.sheets['动量组合']

    # 定义专业格式
    format_dict = {'font_name': '微软雅黑', 'border': 1}

    header_format = workbook.add_format(
        {
            **format_dict,
            'bold': True,
            'font_color': '#FFFFFF',
            'bg_color': '#1F497D',
            'align': 'center',
            'valign': 'vcenter',
        }
    )

    # 数字格式
    price_format = workbook.add_format({**format_dict, 'num_format': '¥#,##0.00', 'align': 'right'})

    percent_format = workbook.add_format({**format_dict, 'num_format': '0.0%', 'align': 'right'})

    int_format = workbook.add_format({**format_dict, 'num_format': '#,##0', 'align': 'right'})

    # 设置列宽和格式
    columns_config = [
        ('代码', 10, header_format),
        ('名称', 16, header_format),
        ('价格', 12, price_format),
        ('分配股数', 12, int_format),
        ('1年收益率', 12, percent_format),
        ('1年百分位', 12, percent_format),
        ('6月收益率', 12, percent_format),
        ('6月百分位', 12, percent_format),
        ('3月收益率', 12, percent_format),
        ('3月百分位', 12, percent_format),
        ('1月收益率', 12, percent_format),
        ('1月百分位', 12, percent_format),
        ('HQM得分', 12, percent_format),
        ('实际投资额', 14, price_format),
    ]

    for idx, (col_name, width, fmt) in enumerate(columns_config):
        # 设置列宽
        worksheet.set_column(idx, idx, width, fmt)
        # 重写标题(中文)
        worksheet.write(0, idx, col_name, header_format)

    # 添加摘要信息
    summary_text = [
        f"报告生成日期: {pd.Timestamp.now().strftime('%Y-%m-%d')}",
        f"投资组合总金额: ¥{float(portfolio_size):,.2f}",
        f"实际投资金额: ¥{total_investment:,.2f}",
        f"现金余额: ¥{cash_remaining:,.2f}",
        f"包含股票数量: {len(top_momentum)}只",
    ]

    for row, text in enumerate(summary_text, start=len(top_momentum) + 3):
        worksheet.write(row, 0, text)

    # 保存Excel文件
    writer.close()
    # writer.save()
    print(f"\n投资组合报告已生成: {report_file}")


if __name__ == "__main__":
    main()
