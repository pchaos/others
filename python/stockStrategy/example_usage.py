# -*- coding=utf-8 -*-

# Modified: 2025-10-07 12:43:02

from data_provider import DataProviderFactory
from ma_strategy import MovingAverageStrategy
import pandas as pd


def example_akshare():
    """使用Akshare数据源示例"""
    print("=== 使用Akshare数据源分析创业板ETF ===")

    # 创建数据提供者
    data_provider = DataProviderFactory.create_provider('akshare')

    # 创建策略实例
    strategy = MovingAverageStrategy(data_provider, initial_capital=100000)

    # 运行完整策略
    strategy.load_data('159915', '20230101', '20231231')
    strategy.calculate_technical_indicators()
    strategy.calculate_ma_scores()
    strategy.generate_trading_signals()
    strategy.run_backtest()

    # 显示结果
    performance = strategy.get_formatted_performance()
    print("\n策略绩效:")
    for key, value in performance.items():
        print(f"{key}: {value}")

    current_signal = strategy.get_current_signal()
    print(f"\n最新信号: {current_signal}")

    return strategy


def example_mock_data():
    """使用模拟数据示例"""
    print("\n=== 使用模拟数据测试策略 ===")

    # 创建模拟数据提供者
    data_provider = DataProviderFactory.create_provider('mock')

    # 创建策略实例
    strategy = MovingAverageStrategy(data_provider, initial_capital=100000)

    # 运行策略
    strategy.load_data('TEST001', '20230101', '20231231')
    strategy.calculate_technical_indicators()
    strategy.calculate_ma_scores()
    strategy.generate_trading_signals()
    strategy.run_backtest()

    # 显示结果
    performance = strategy.get_formatted_performance()
    print("\n模拟数据策略绩效:")
    for key, value in performance.items():
        print(f"{key}: {value}")

    return strategy


def example_multiple_etfs():
    """多ETF对比分析示例"""
    print("\n=== 多ETF对比分析 ===")

    etf_codes = ['159915', '510300', '512880']  # 创业板, 沪深300, 证券
    results = {}

    data_provider = DataProviderFactory.create_provider('akshare')

    for code in etf_codes:
        print(f"\n分析 ETF{code}...")

        try:
            strategy = MovingAverageStrategy(data_provider)
            strategy.load_data(code, '20230101', '20231231')
            strategy.calculate_technical_indicators()
            strategy.calculate_ma_scores()
            strategy.generate_trading_signals()
            strategy.run_backtest()

            performance = strategy.get_formatted_performance()
            results[code] = performance

        except Exception as e:
            print(f"分析 {code} 失败: {e}")
            results[code] = None

    # 显示对比结果
    print("\n=== ETF对比结果 ===")
    comparison_df = pd.DataFrame(results).T
    print(comparison_df)

    return results


if __name__ == "__main__":
    # 运行示例
    example_akshare()
    example_mock_data()
    example_multiple_etfs()
