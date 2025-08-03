# -*- coding=utf-8 -*-

# Modified: 2025-08-03 13:14:47
# This script calculates the value of x such that (2 * 10^i - 4) % 19 == 0
# for i in the range of 550, and prints the value of x and its digit_count

import math


def digit_count(n):
    """计算数字 n 的位数"""
    if n == 0:
        return 1
    return math.floor(math.log10(abs(n))) + 1


def double_digit_count(n):
    xlist = []
    """计算满足条件的 x 的值"""
    for i in range(n):
        x1 = (2 * 10**i - 4) % 19 == 0
        if x1:
            numerator = 2 * 10**i - 4  # 使用整数类型
            denominator = 19
            x = numerator // denominator  # 使用整数除法
            xlist.append(x)
    return xlist


def check_double_digit_count(n):
    """检查满足条件的 x 的数量"""
    digit_counts = digit_count(n)
    x1 = 2 * 10**digit_counts + n
    x2 = n * 10 + 2
    # print(f"{x1} == {x2 * 2}")
    return x1 == x2 * 2


if __name__ == "__main__":
    digits = 600
    xlist = double_digit_count(digits)
    # 计算 x 的位数
    if xlist is not None:
        for x in xlist:
            digit_counts = digit_count(x)
            # 打印 x 和其位数
            if check_double_digit_count(x):
                # print(f"{x} 满足条件")
                print(f"{x}", end="")
                print(f"\t位数: {digit_counts}")
            else:
                print(f"{x} 不满足条件")
                break
        print(f"{digits}位数总共有 {len(xlist)} 个满足条件的 x")
